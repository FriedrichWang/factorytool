__author__ = 'friedrich'


class IController(object):

    def __init__(self):
        pass

    def handle_action(self, request_code, input_bundle):
        pass

    def handle_successful(self, request_code, stamp_bundle):
        pass

    def handle_failure(self, request_code, stamp_bundle):
        pass

    def report_failure(self):
        pass
