import traceback
__author__ = 'friedrich'

from json import loads as jloads
from workflow.Controller import IController
from workflow.WebService import WebService as WebService
from setting import Setting

class BaseController(IController):
    def __init__(self, _step, _stamp_bundle, _listener):
        self.step = _step
        self.stamp = _stamp_bundle
        self.listener = _listener
        self.web_service = WebService()
        self.sub_process = -1
        self.name = ''
        
    def get_name(self):
        return self.name
        
    def init(self):
        self.listener.onInitUI(self)
        
    def web_commit(self, _input_bundle, _result):
        url = Setting.BASE_STEP_URL.format(_input_bundle.params[Setting.STEP],
                                       _input_bundle.params[Setting.ID], _result)
        _body = self.web_service.make_request(url, self.stamp.params, _input_bundle.params)
        _smt_body = self.jsonloads(_body)
        return _smt_body
        
    def checkstep(self):
        url = Setting.BASE_CHECKSTEP_URL % {'step': self.step, 'sn': self.stamp[Setting.ID]}
        resp = self.jsonloads(self.web_service.make_request(url))
        return resp

    def handle_action(self, _request_code, _input_bundle):
        resp = self.checkstep()
        if not resp['ret']:
            self.listener.onFailed(self, resp)
            return

        _result = self.action.on_action(_request_code, _input_bundle, self.stamp)
        resp = self.web_commit(_input_bundle, _result)

        if self.listener is not None:
            self.listener.onResponse(self, resp)
        return _result
