#encoding=utf8
__author__ = 'friedrich'

from workflow.BaseController import BaseController
from adb.AdbAction import AdbAction as Action
from setting import Setting

class AdbController(BaseController):
    def __init__(self, _id, _stamp, _listener):
        BaseController.__init__(self, _id, _stamp, _listener)
        self.action = Action()
        self.__subprocess = 0
        self.SMT_TEST_SUB_PROCESS = []
        self.SMT_TEST_SUB_PROCESS.append({'label': u'wifi测试',
                                          'debug_ret': Setting.RESULT_OK})
        self.SMT_TEST_SUB_PROCESS.append({'label': u'屏幕测试',
                                          'debug_ret': Setting.RESULT_OK})
        self.SMT_TEST_SUB_PROCESS.append({'label': u'背光测试',
                                          'debug_ret': Setting.RESULT_OK})
        self.SMT_TEST_SUB_PROCESS.append({'label': u'传感器测试',
                                          'debug_ret': Setting.RESULT_OK})
        self.SMT_TEST_SUB_PROCESS.append({'label': u'音频测试',
                                          'debug_ret': Setting.RESULT_CONTINUE})
        self.SMT_TEST_SUB_PROCESS.append({'label': u'录音测试',
                                          'debug_ret': Setting.RESULT_OK})
        self.SMT_TEST_SUB_PROCESS.append({'label': u'上传报告',
                                          'debug_ret': Setting.RESULT_OK})
        self.name = 'Empty'
        self.stamp.params['product_test'] = {}

    def handle_action(self, _request_code, _input_bundle):
        result = None

        while (self.__subprocess < len(self.SMT_TEST_SUB_PROCESS)):
            self.name = self.SMT_TEST_SUB_PROCESS[self.__subprocess]['label']
            self.listener.onInitUI(self)
            if Setting.DEBUG:
                result = self.SMT_TEST_SUB_PROCESS[self.__subprocess]['debug_ret']
            else:
                result = self.action.on_action(_request_code, _input_bundle, self.stamp, self.__subprocess)
            self.__subprocess += 1
            if result == Setting.RESULT_CONTINUE:
                self.listener.onContinue(self)
                break
        if result != Setting.RESULT_CONTINUE and self.__subprocess == len(self.SMT_TEST_SUB_PROCESS):
            url = Setting.BASE_STEP_URL.format(_input_bundle.params[Setting.STEP], _input_bundle.params[Setting.ID], result)
            if not Setting.DEBUG:
                self.stamp.params["product_test"]["state"] = self.action.is_passed()
            self.stamp.params[Setting.STEP] = _input_bundle.params[Setting.STEP]
            self.stamp.params[Setting.ID] = _input_bundle.params[Setting.ID]
            resp = self.web_service.make_request(url, self.stamp.params, self.stamp.params["product_test"])
            self.__subprocess = 0
            self.action.clear()
            return resp['ret']
        return result

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
