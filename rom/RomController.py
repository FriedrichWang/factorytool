__author__ = 'friedrich'

from workflow.BaseController import BaseController
from rom.RomAction import RomAction as Action
from setting import Setting as Env

ROM = "rom"


class RomController(BaseController):

    def __init__(self):
        BaseController.__init__(self)

    def __init__(self, _id, _stamp, _listener):
        BaseController.__init__(self, _id, _stamp, _listener)
        self.action = Action()

    def handle_action(self, request_code, input_bundle):
        _result = BaseController.handle_action(self, request_code, input_bundle)
        return _result

    def handle_successful(self, request_code, stamp_bundle):
        self.stamp.params[ROM] = Env.RESULT_OK

    def handle_failure(self, request_code, stamp_bundle):
        self.stamp.params[ROM] = Env.RESULT_FAILED
