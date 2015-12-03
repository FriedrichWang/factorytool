__author__ = 'friedrich'

from os import listdir
from workflow.BaseAction import BaseAction
from adjust.AdjustService import AdjustService as Service
from setting import Setting

class AdjustAction(BaseAction):
    def __init__(self):
        BaseAction.__init__(self)
        self.service = Service()

    def on_action(self, _request_code, _params_bundle, _stamp_bundle):

        _sn_number = _params_bundle.params[Setting.ID]
        self.service.package_to_tar(_sn_number)
        self.service.add_files(listdir(Setting.DEFAULT_FILE))
        _stamp_bundle.params['adjust'] = self.service.get_zip().filename

        return Setting.RESULT_OK
