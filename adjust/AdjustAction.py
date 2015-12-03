__author__ = 'friedrich'

from workflow.BaseAction import BaseAction
from adjust.AdjustService import AdjustService as Service
from setting import Setting as Env
from sn.SnAction import SN
import os


class AdjustAction(BaseAction):

    def __init__(self):
        BaseAction.__init__(self)
        self.service = Service()

    def on_action(self, _request_code, _params_bundle, _stamp_bundle):

        _sn_number = _params_bundle.params[SN]
        self.service.package_to_tar(_sn_number)
        self.service.add_files(os.listdir(Env.DEFAULT_FILE))
        _stamp_bundle.params['adjust'] = self.service.get_zip().filename

        return Env.RESULT_OK
