# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class SRoom(KBEngine.Space):
    def __init__(self):
        KBEngine.Space.__init__(self)
        self.playerDic = {}

    def enter(self, EntityCall):
        """
        进入房间
        :param EntityCall:
        :return:
        """
        EntityCall.createCellEntity(self.cell)
        self.playerDic[EntityCall.id] = EntityCall

    def leave(self, EntityId):
        """
        离开房间
        :param EntityId:
        :return:
        """
        playerEntity = self.playerDic[EntityId]
        del self.playerDic[EntityId]
        # 销毁目标实体关联的cell实体
        if playerEntity is not None:
            if playerEntity.cell is not None:
                playerEntity.destroyCellEntity()

    def onGetCell(self):
        """
        entity的cell部分被创建成功
        :return:
        """
        DEBUG_MSG("Room::onGetCell: id=%i" % self.id)

        KBEngine.globalData["RoomMgr"].onRoomGetCell(self)

    def onLoseCell(self):
        """
        entity的cell部分实体丢失
        :return:
        """
        DEBUG_MSG("Room::onLoseCell: id=%i" % self.id)
        KBEngine.globalData["RoomMgr"].onRoomGetCell(self)
        self.destroy()
