__author__ = 'friedrich'

from workflow.BaseController import BaseController
from adjust.AdjustAction import AdjustAction as Action
from workflow.WebService import WebService

ADJUST = "adjust"

class AdjustController(BaseController):
    def __init__(self, _id, _stamp, _listener):
        BaseController.__init__(self, _id, _stamp, _listener)
        self.action = Action()
        self.web_service = WebService()
        self.stamp = _stamp

    def handle_action(self, request_code, _input_bundle):
        _result = self.action.on_action(request_code, _input_bundle, self.stamp)
        #if _result == Env.RESULT_OK:
            #self.web_service.reload_url(Env.ADJUST_URL.format(_input_bundle.params[Env.ID]))
            #_body = self.web_service.upload_request(self.stamp.params[ADJUST])
            #_smt_body = json.loads(_body, encoding='utf-8')
            #self.stamp.params[Env.ID] = _smt_body[u'id']
            #_input_bundle.params[Env.ID] = _smt_body[u'id']
            #_input_bundle.params[Env.STEP] = _smt_body[u'step']
        return _result

    def handle_successful(self, request_code, _stamp_bundle):
        pass

    def handle_failure(self, request_code, _stamp_bundle):
        pass
