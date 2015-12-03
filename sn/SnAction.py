__author__ = 'friedrich'

import json

from workflow.BaseAction import BaseAction
from SnService import SnService as Service
from workflow.WebService import WebService
from setting import Setting as Env
import Crypto

SN = "snNumber"


class SnAction(BaseAction):

    def __init__(self):
        BaseAction.__init__(self)
        self.service = Service()
        self.web_service = WebService()

    def on_action(self, _request_code, _params_bundle, _stamp_bundle):
        self.web_service.reload_url(Env.SN_URL.format(_params_bundle.params['id']))
        body = dict()
        body['pcsId'] = _params_bundle.params['id']
        body['productCode'] = "C1"
        body['hardwareCode'] = "Y1"
        body_str = json.dumps(body)
        sn = self.web_service.make_request(_params_bundle.params, body_str)
        sn_en_crypto = Crypto.de_csn(body['productCode'], body['hardwareCode'], sn)
        store_sn = _params_bundle.params['sn_number']
        body['sn'] = sn
        _params_bundle.params[SN] = sn
        _stamp_bundle.params[SN] = body
        return self.service.store_sn_num(store_sn)
