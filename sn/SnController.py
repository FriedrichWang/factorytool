__author__ = 'friedrich'

import json

from workflow.BaseController import BaseController
from sn.SnAction import SnAction as Action
from setting import Setting as Env


class SnController(BaseController):

    def __init__(self):
        BaseController.__init__(self)
        self.action = Action()

    def __init__(self, _id, _stamp, _listener):
        BaseController.__init__(self, _id, _stamp, _listener)
        self.action = Action()

    def handle_action(self, _request_code, _input_bundle):
        _result = self.action.on_action(_request_code, _input_bundle, self.stamp)
        #self.web_service.reload_url(Env.BASE_STEP_URL.
        #                            format(_input_bundle.params[Env.STEP], _input_bundle.params[Env.ID], _result))
        if _result == Env.RESULT_OK:
            _body = self.web_service.make_request(self.stamp.params, json.dumps(self.stamp.params["snNumber"]))
            _smt_body = json.loads(_body, encoding='utf-8')
            self.stamp.params[Env.ID] = _smt_body[u'id']
            _input_bundle.params[Env.ID] = _smt_body[u'id']
            _input_bundle.params[Env.STEP] = _smt_body[u'step']

        if self.listener is not None:
            self.listener.on_result(self.id, _result, self.stamp)
        return _result

    def handle_successful(self, request_code, stamp_bundle):
        pass

    def handle_failure(self, request_code, stamp_bundle):
        pass

    def report_failure(self):
        return Env.RESULT_FAILED