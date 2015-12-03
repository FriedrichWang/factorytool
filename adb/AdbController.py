#encoding=utf8
__author__ = 'friedrich'

import json
from workflow.BaseController import BaseController
from adb.AdbAction import AdbAction as Action
from setting import Setting

class AdbController(BaseController):
    def __init__(self, _id, _stamp, _listener):
        BaseController.__init__(self, _id, _stamp, _listener)
        self.action = Action()
        self.__subprocess = 0
        self.SMT_TEST_SUB_PROCESS = [u'wifi测试', u'屏幕测试', u'背光测试', u'传感器测试', u'音频测试', u'录音测试', u'上传报告']
    
    def get_label(self):
        return self.name

    def handle_action(self, _request_code, _input_bundle):
        result = None

        while (self.__subprocess <= len(self.SMT_TEST_SUB_PROCESS)):
            self.name = self.SMT_TEST_SUB_PROCESS[self.__subprocess - 1]
            result = self.action.on_action(_request_code, _input_bundle, self.stamp, self.__subprocess)
            self.__subprocess += 1
            if result == Setting.RESULT_CONTINUE:
                self.listener.onContinue(self)
                break
        if result != Setting.RESULT_CONTINUE and self.__subprocess > len(self.SMT_TEST_SUB_PROCESS):
            url = Setting.BASE_STEP_URL.format(_input_bundle.params[Setting.STEP], _input_bundle.params[Setting.ID], result)
            self.stamp.params["product_test"]["state"] = self.action.is_passed()
            resp = self.web_service.make_request(url, self.stamp.params, json.dumps(self.stamp.params["product_test"]))
            self.__subprocess = 0
            self.action.clear()
            return resp['ret']

    def report_failure(self):
        if self.__subprocess == 1:
            self.stamp.params["product_test"]["wifi"] = 0
        elif self.__subprocess == 2:
            self.stamp.params["product_test"]["power"] = 0
        elif self.__subprocess == 3:
            self.stamp.params["product_test"]["backlight"] = 0
        elif self.__subprocess == 4:
            self.stamp.params["product_test"]["sensor"] = 0
        elif self.__subprocess == 5:
            self.stamp.params["product_test"]["audio"] = 0
        elif self.__subprocess == 6:
            self.stamp.params["product_test"]["record"] = 0
        self.action.mark_failed()
        return Setting.RESULT_NONSTOP_FAILED
