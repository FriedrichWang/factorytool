__author__ = 'friedrich'

from workflow.BaseAction import BaseAction
from rom.RomService import RomService


class RomAction(BaseAction):

    def __init__(self):
        BaseAction.__init__(self)
        self.service = RomService()

    def on_action(self, _request_code, _params_bundle, _stamp_bundle):
        _result = self.service.on_transaction()
        return _result
