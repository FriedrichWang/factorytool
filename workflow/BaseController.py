__author__ = 'friedrich'

import json

from workflow.Controller import IController
from workflow.WebService import WebService as WebService
from setting import Setting as Env


class BaseController(IController):

    def __init__(self):
        self.id = 0
        self.action = None
        self.tag = ""
        self.stamp = None
        self.result = 0
        self.service = None
        self.listener = None
        self.sub_process = -1

    def __init__(self, _id, _stamp_bundle, _listener):
        self.id = _id
        self.stamp = _stamp_bundle
        self.listener = _listener
        self.web_service = WebService()
        self.sub_process = -1

    def handle_action(self, _request_code, _input_bundle):
        _result = self.action.on_action(_request_code, _input_bundle, self.stamp)
        self.web_service.reload_url(Env.BASE_STEP_URL.format(_input_bundle.params[Env.STEP],
                                                             _input_bundle.params[Env.ID], _result))
        if _result == Env.RESULT_OK:
            _body = self.web_service.make_request(self.stamp.params, _input_bundle.params)
            _smt_body = json.loads(_body, encoding='utf-8')
            self.stamp.params[Env.ID] = _smt_body[u'id']
            _input_bundle.params[Env.ID] = _smt_body[u'id']
            _input_bundle.params[Env.STEP] = _smt_body[u'step']

            if self.listener is not None:
                self.listener.on_result(self.id, _result, self.stamp)
        return _result

