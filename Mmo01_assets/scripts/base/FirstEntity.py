# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from ROOM_INFO import TRoomInfo, TRoomList
from ROLE_INFO import TRoleInfo, TRoleList

class FirstEntity(KBEngine.Proxy):

    def __init__(self):
        KBEngine.Entity.__init__(self)
        self.ActiveRole = None

        if len(self.RoleList) == 0:
            self.CreateRole("Ashe")
            self.CreateRole("Anivia")

    def onClientEnabled(self):
        """
        该entity被正式激活为可使用
        :return:
        """
        # 客户端一旦连接，就把它放入FirstSpace空间
        #first_space = KBEngine.globalData["FirstSpace"]
        #self.createCellEntity(first_space.cell)
        pass

    def OnAccountCreateRoom(self, Succeed, RoomId, Name):
        """
        创建房间回调函数
        :param Succeed:
        :param RoomId:
        :param Name:
        :return:
        """
        pass

    def ReqRoomList(self):
        """
        请求房间列表
        :return:
        """
        RoomList = KBEngine.globalData["RoomMgr"].GetRoomList()
        DEBUG_MSG("Account[%i]::ReqRoomList = %s" % (self.id, RoomList.asDict()))
        self.client.OnReqRoomList(RoomList)

    def SelectRoom(self, RoomId):
        """
        选择房间
        :param RoomId:
        :return:
        """
        DEBUG_MSG("Account[%i]::SelectRoom, RoomId = %i" % (self.id, RoomId))
        self.LastSelRoom = RoomId
        self.client.OnSelectRoom()

    def ReqRoleList(self):
        """
        请求角色列表
        :return:
        """
        DEBUG_MSG("Account[%i]::ReqRoleList: size=%i, roleList=%s" % (self.id, len(self.RoleList), self.RoleList))
        if self.ActiveRole is not None:
            self.ActiveRole.destroy()
            self.ActiveRole = None

        self.client.OnReqRoleList(self.RoleList)

    def ReqSelectRole(self, Dbid):
        """
        请求选择角色
        :param Dbid:
        :return:
        """
        if Dbid in self.RoleList:
            self.client.OnSelectRole(0, Dbid)
        else:
            self.client.OnSelectRole(1, Dbid)

        DEBUG_MSG("ExAccount[%i].ReqSelectRole: RoomId = %i , RoleId = %i" % (self.id, self.LastSelRoom, Dbid))
        KBEngine.createEntityFromDBID("Role", Dbid, self._OnRoleCreated)

    def _OnRoleCreated(self, BaseRef, Dbid, WasActive):
        """
        从数据库创建选中的角色的回调函数
        :param BaseRef:
        :param Dbid:
        :param WasActive:
        :return:
        """
        if WasActive:
            ERROR_MSG("ExAccount[%i]::_OnRoleCreated: this role is in world" % self.id)
            return

        if BaseRef is None:
            ERROR_MSG("ExAccount[%i]::_OnRoleCreated: this role create from DB is not Exit" % self.id)
            return

        # 获取角色实体
        Hero = KBEngine.entities.get(BaseRef.id)
        if Hero is None:
            ERROR_MSG("ExAccount[%i]::_OnRoleCreated: when role was created, it died as well!" % self.id)
            return

        if self.isDestroyed:
            ERROR_MSG("ExAccount::_OnRoleCreated:(%i): i dead, will the destroy of role!" % (self.id))
            Hero.destroy()
            return

        DEBUG_MSG('ExAccount::_OnRoleCreated:(%i) enter room game:  %s, %i' % (self.id, Hero.cellData["Name"], Hero.databaseID))
        self.ActiveRole = Hero
        self.giveClientTo(Hero)
        Hero.AccountEntity = self
        KBEngine.globalData["RoomMgr"].enterRoom(self.LastSelRoom, Hero)

    def CreateRole(self, Name):
        """
        创建角色
        :param Name: 角色名字
        :return:
        """
        Props = {
            "Name" : Name
        }
        Hero = KBEngine.createEntityLocally("Role", Props)
        if Hero:
            Hero.writeToDB(self._OnHeroSaved)

    def _OnHeroSaved(self, Success, Hero):
        """
        将角色写入数据库的回调函数
        :param Success:
        :param Hero:
        :return:
        """
        if self.isDestroyed:
            if Hero:
                Hero.destroy(True)
            return

        RoleInfo = TRoleInfo()
        RoleInfo.extend([0, ""])
        if Hero:
            # cellData可以获取未生成cell实体时cell作用域的变量
            RoleInfo[1] = Hero.cellData["Name"]
            if Success:
                RoleInfo[0] = Hero.databaseID
                self.RoleList[Hero.databaseID] = RoleInfo
                self.writeToDB()

            Hero.destroy()


    def onClientDeath(self):
        """
        客户端对应实体已经销毁
        :return:
        """
        self.destroy()