# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class FirstEntity(KBEngine.Entity):

    def __init__(self):
        KBEngine.Entity.__init__(self)
        # 通知客户端，本实体已进入
        self.client.onEnter()

    def say(self, callerID, content):
        """
        实现CellMethods中的say方法
        :param callerID: 调用者ID
        :param content: say的内容
        :return:
        """
        INFO_MSG("FirstEntity::say")
        self.allClients.onSay("Entity: " + str(self.id) + " " + content)
