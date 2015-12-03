__author__ = 'friedrich'
import json

from workflow.BaseAction import BaseAction
from adb.AdbService import AdbService as Service
from setting import Setting

PRODUCT_TEST = "product_test"

class AdbAction(BaseAction):
    def __init__(self):
        BaseAction.__init__(self)
        self.service = Service()

    def on_action(self, _request_code, _params_bundle, _stamp_bundle, sub_step):
        _retval = 2
        if sub_step == 0:
            self.service.find_all_device()
            self.service.setup_device()
            _retval = self.service.start_wifi_test()
        elif sub_step == 1:
            _retval = self.service.start_power_test()
            if _retval == Setting.RESULT_OK: return Setting.RESULT_CONTINUE
        elif sub_step == 2:
            _retval =  self.service.start_backlight_test()
        elif sub_step == 3:
            _retval = self.service.start_sensor_test()
        elif sub_step == 4:
            _retval = self.service.start_audio_test()
            if _retval == Setting.RESULT_OK: return Setting.RESULT_CONTINUE
        elif sub_step == 5:
            _retval = self.service.start_record_test()
        elif sub_step == 6:
            return Setting.RESULT_OK
        test_result = json.dumps(self.service.product_test)
        print test_result
        _stamp_bundle.params[PRODUCT_TEST] = self.service.product_test
        return _retval

    def mark_failed(self):
        self.service.mark_failed()

    def is_passed(self):
        return self.service.is_passed()

    def clear(self):
        self.service.clear()
