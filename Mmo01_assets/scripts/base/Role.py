# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
#from interfaces

class Role(KBEngine.Proxy):
    def __init__(self):
        KBEngine.Proxy.__init__(self)
        self.AccountEntity = None