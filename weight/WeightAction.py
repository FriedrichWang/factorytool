__author__ = 'friedrich'

from workflow.BaseAction import BaseAction
from WeightService import WeightService as Service
from setting import Setting as Env


class WeightAction(BaseAction):

    def __init__(self):
        BaseAction.__init__(self)
        self.service = Service()

    def on_action(self, _request_code, _params_bundle, _stamp_bundle):
        return Env.RESULT_OK
