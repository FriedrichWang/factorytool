__author__ = 'friedrich'

import json
from workflow.BaseAction import BaseAction
from SnService import SnService as Service
from workflow.WebService import WebService
from setting import Setting
import Crypto

class SnAction(BaseAction):
    def __init__(self):
        BaseAction.__init__(self)
        self.service = Service()

    def on_action(self, _request_code, _params_bundle, _stamp_bundle):
        store_sn = _params_bundle.params[Setting.ID]
        _stamp_bundle.params[Setting.ID] = store_sn
        return self.service.store_sn_num(store_sn)
