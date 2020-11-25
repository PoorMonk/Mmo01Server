# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class SRoom(KBEngine.Space):
    """
    SRoom的Cell部分
    """
    def __init__(self):
        KBEngine.Space.__init__(self)

        KBEngine.addSpaceGeometryMapping(self.spaceID, None, "spaces/MmoMapOne")

    def GetScriptName(self):
        return self.__class__.__name__

