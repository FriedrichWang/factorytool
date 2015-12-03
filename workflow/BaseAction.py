__author__ = 'friedrich'
from workflow.Action import Action


class BaseAction(Action):

    def __init__(self):
        Action.__init__(self)

    def on_action(self, request_code, param, stamp):
        pass
