__author__ = 'friedrich'
from workflow.Service import Service
from adb.Adb import ADB
from setting import Setting as Env

class SnService(Service):
    def __init__(self):
        self.adb = ADB(Env.ADB_PATH)

    def store_sn_num(self, sn_number):
        ret = self.adb.store_sn_data(sn_number)
        return ret
