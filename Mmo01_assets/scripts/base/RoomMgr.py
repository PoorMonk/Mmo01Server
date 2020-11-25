# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from ROOM_INFO import TRoomInfo, TRoomList
from SRoom import SRoom

class RoomMgr(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)

        # 房间列表，保存所有房间，key:房间Id，value:房间cell实体
        self.roomList = {}
        # 存储创建中的房间字典，key:房间名，value:Account
        self.DemandAccount = {}

        KBEngine.globalData["RoomMgr"] = self

        self.CreateRoom("卡拉曼达", None)
        self.CreateRoom("皮尔特沃夫", None)

    def CreateRoom(self, Name, Account):
        """
        创建房间
        :param Name:
        :param Account:
        :return:
        """
        for RoomId, Room in self.roomList.items():
            if Room.Name == Name:
                if Account is not None:
                    Account.OnAccountCreateRoom(False, 0, Name)
                return

        if Name in self.DemandAccount:
            Account.OnAccountCreateRoom(False, 0, Name)
            return

        if Account is not None:
            self.DemandAccount[Name] = Account

        # 创建房间
        Props = {
            "Name" : Name,
            "Count" : 10
        }
        KBEngine.createEntityLocally("SRoom", Props)

    def GetRoomList(self):
        RoomList = TRoomList()
        for RoomId, Room in self.roomList.items():
            Props = {"RoomId" : RoomId, "Name" : Room.Name}
            RoomList[RoomId] = TRoomInfo().createFromDict(Props)
        return RoomList

    def enterRoom(self, RoomId, EntityCall):
        """
        进入指定房间
        :param RoomId: 房间Id
        :param EntityCall: 请求进入房间对象
        """
        room = self.roomList[RoomId]
        if room is None:
            ERROR_MSG("RoomMgr::enterRoom: roomId %s is none" % RoomId)
            return

        room.enter(EntityCall)

    def leaveRoom(self, RoomId, EntityId):
        """
        请求离开房间
        :param RoomId:
        :param EntityId:
        :return:
        """
        room = self.roomList[RoomId]
        if room is None:
            ERROR_MSG("RoomMgr::enterRoom: roomId %s is none" % RoomId)
            return

        room.leave(EntityId)

    def onRoomGetCell(self, Room):
        """
        房间cell实体创建成功后调用
        :param EntityCall:
        :return:
        """
        DEBUG_MSG("RoomMgr::onRoomGetCell: roomName=%s" % Room.Name)
        self.roomList[Room.id] = Room

        for Name, Account in self.DemandAccount.items():
            if Name == Room.Name:
                Account.OnAccountCreateRoom(True, Room.id, Room.Name)
                del self.DemandAccount[Name]
                return

    def onRoomLoseCell(self, EntityCall):
        """
        房间cell实体销毁后调用
        :param EntityCall:
        :return:
        """
        DEBUG_MSG("RoomMgr::onRoomLoseCell: roomName=%s" % EntityCall.Name)
        del self.roomList[EntityCall.id]
