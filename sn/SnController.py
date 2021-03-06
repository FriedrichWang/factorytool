#encoding=utf8
__author__ = 'friedrich'

import json

from workflow.BaseController import BaseController
from sn.SnAction import SnAction as Action
from setting import Setting as Env

class SnController(BaseController):
    def __init__(self, _id, _stamp, _listener):
        BaseController.__init__(self, _id, _stamp, _listener)
        self.action = Action()
        self.entry = 'SN: '
        self.name = '写入SN'

    def checkstep(self):
        # Special step, not to check with server
        return {'ret': 1, 'desc': 'First Step'}

    def handle_successful(self, request_code, stamp_bundle):
        pass

    def handle_failure(self, request_code, stamp_bundle):
        pass

    def report_failure(self):
        return Env.RESULT_FAILED
