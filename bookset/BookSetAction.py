__author__ = 'friedrich'

from workflow.BaseAction import BaseAction
from bookset.BookSetService import BookSetService as Service
from setting import Setting as Env


class BookSetAction(BaseAction):

    def __init__(self):
        BaseAction.__init__(self)
        self.service = Service()

    def on_action(self, _request_code, _params_bundle, _stamp_bundle):
        return Env.RESULT_OK
