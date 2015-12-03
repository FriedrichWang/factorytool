__author__ = 'friedrich'
import json

from workflow.BaseController import BaseController
from adb.AdbAction import AdbAction as Action
from setting import Setting as Env


class AdbController(BaseController):
    def __init__(self, _id, _stamp, _listener):
        BaseController.__init__(self, _id, _stamp, _listener)
        self.action = Action()
        self.__subprocess = 0

    def handle_action(self, _request_code, _input_bundle):
        if self.__subprocess != 6:
            _result = self.action.on_action(_request_code, _input_bundle, self.stamp, self.__subprocess)
            self.__subprocess += 1
            if self.listener is not None:
                self.listener.on_result(self.id, _result, self.stamp, self.__subprocess)
            return _result
        else:
            self.web_service.reload_url(Env.BASE_STEP_URL.format(_input_bundle.params[Env.STEP],
                                                                 _input_bundle.params[Env.ID], Env.RESULT_OK))
            self.stamp.params["product_test"]["state"] = self.action.is_passed()
            _body = self.web_service.make_request(self.stamp.params, json.dumps(self.stamp.params["product_test"]))
            _smt_body = json.loads(_body, encoding='utf-8')
            self.stamp.params[Env.ID] = _smt_body[u'id']
            _input_bundle.params[Env.ID] = _smt_body[u'id']
            _input_bundle.params[Env.STEP] = _smt_body[u'step']

            if self.listener is not None:
                self.listener.on_result(self.id, Env.RESULT_FINISH, self.stamp, self.__subprocess)
                self.__subprocess = 0
                self.action.clear()
            return Env.RESULT_FINISH

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
        return Env.RESULT_NONSTOP_FAILED

    def handle_successful(self, request_code, stamp_bundle):
        pass

    def handle_failure(self, request_code, stamp_bundle):
        pass