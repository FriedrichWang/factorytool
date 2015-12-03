__author__ = 'friedrich'
from workflow.Service import Service
from Adb import ADB
from setting import Setting as Env


class AdbService(Service):

    def __init__(self):
        self.adb = ADB(Env.ADB_PATH)
        self.device_num = Env.DEVICE_SERIAL
        self.product_test = dict()
        self.__result = 0

    def find_all_device(self):
        if self.adb.check_path():
            self.adb.get_devices()

    def setup_device(self):
        if self.adb.check_path():
            self.adb.set_target_device(self.device_num)

    def start_test(self):
        self.adb.kill_server()
        self.adb.start_server()
        #self.adb.test_wifi_state()
        self.product_test['wifi'] = 1
        self.product_test['power'] = self.adb.test_power()
        #self.adb.test_sensor()
        self.product_test['sensor'] = 1
        self.product_test['backlight'] = self.adb.test_back_light()
        self.adb.test_audio()
        self.product_test['audio'] = 1
        self.product_test['record'] = self.adb.test_record()
        self.product_test['state'] = 1

    def start_wifi_test(self):
        self.adb.kill_server()
        self.adb.start_server()
        _retval = self.adb.test_wifi_state()
        self.product_test['wifi'] = _retval
        self.__result = _retval
        return _retval

    def start_power_test(self):
        self.adb.kill_server()
        self.adb.start_server()
        _retval = self.adb.test_power()
        self.product_test['power'] = _retval
        self.__result = _retval
        return _retval

    def start_sensor_test(self):
        self.adb.kill_server()
        self.adb.start_server()
        _retval = self.adb.test_sensor()
        self.product_test['sensor'] = _retval
        self.__result = _retval
        return _retval

    def start_backlight_test(self):
        self.adb.kill_server()
        self.adb.start_server()
        _retval = self.adb.test_back_light()
        self.product_test['backlight'] = _retval
        self.__result = _retval
        return _retval

    def start_audio_test(self):
        self.adb.kill_server()
        self.adb.start_server()
        _retval = self.adb.test_audio()
        self.product_test['audio'] = _retval
        self.__result = _retval
        return _retval

    def start_record_test(self):
        self.adb.kill_server()
        self.adb.start_server()
        _retval = self.adb.test_record()
        self.product_test['record'] = _retval
        self.__result = _retval
        return _retval

    def clear(self):
        self.product_test.clear()

    def mark_failed(self):
        self.__result = 0

    def is_passed(self):
        return self.__result

