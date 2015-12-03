__author__ = 'friedrich'

from workflow.Service import Service
from setting import Setting as Env


class RomService(Service):

    def __init__(self):
        pass

    def on_transaction(self):
        """
        to fix it in windows
        _ret = os.system("D:\mfgtools\mfgtools\MfgTool2.exe -noui")
        """
        _ret = 0
        if _ret == 0:
            return Env.RESULT_OK
        else:
            return Env.RESULT_FAILED
