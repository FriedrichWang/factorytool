__author__ = 'friedrich'

from workflow.BaseController import BaseController
from smt.SmtAction import SmtAction as Action
from smt.SmtService import SmtService as Service
from setting import Setting as Env

SMT = "mark"


class SmtController(BaseController):

    def __init__(self, _id, _stamp, _listener):
        BaseController.__init__(self, _id, _stamp, _listener)
        self.action = Action()
        self.service = Service()

    def handle_action(self, request_code, input_bundle):
        _result = BaseController.handle_action(self, request_code, input_bundle)
        return _result

    def handle_successful(self, request_code, stamp_bundle):
        self.stamp.params[SMT] = Env.RESULT_OK

    def handle_failure(self, request_code, stamp_bundle):
        self.stamp.params[SMT] = Env.RESULT_FAILED