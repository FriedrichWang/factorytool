__author__ = 'friedrich'
import json

from setting import Setting as Env

class FlowContext(object):

    def __init__(self, _input_bundle, _stamp_bundle):
        self.work_queue = []
        self.input_bundle = _input_bundle
        self.stamp_bundle = _stamp_bundle
        self.result = Env.RESULT_UNKNOWN
        self.input_bundle.params[Env.ID] = -1
        self.input_bundle.params[Env.STEP] = 1
        self.mark = 0

    def init_controller(self, _controllers):
        self.work_queue.extend(_controllers)

    def set_input(self, _input_bundle):
        self.input_bundle = _input_bundle

    def start_loop(self, sub_process=-1):
        while self.mark < len(self.work_queue):
            _controller = self.work_queue[self.mark]
            _controller.init()
            self.mark += 1
    
            _result = _controller.handle_action(self.result, self.input_bundle)
            if _result == Env.RESULT_OK:
                _controller.handle_successful(self.result, self.stamp_bundle)
                self.result = Env.RESULT_OK
            elif _result == Env.RESULT_FAILED:
                _controller.handle_failure(self.result, self.stamp_bundle)
                self.result = Env.RESULT_FAILED
            elif _result == Env.RESULT_FINISH:
                self.clear()
            else:
                _controller.handle_failure(self.result, self.stamp_bundle)
                self.result = Env.RESULT_FAILED

    def stamp_result(self):
        if self.stamp_bundle is not None and self.stamp_bundle.params is not None:
            self.stamp_bundle.params[Env.ALL_PASS] = self.result
            _stamp_result = json.dumps(self.stamp_bundle.params)
            print(_stamp_result)

    def clear(self):
        self.result = Env.RESULT_UNKNOWN
        self.input_bundle.clear()
        self.input_bundle.clear()
        self.input_bundle.params[Env.ID] = -1
        self.input_bundle.params[Env.STEP] = 1
        self.mark = 0

    def run(self):
        if self.mark == len(self.work_queue):
            self.clear()
        self.start_loop()
        #self.stamp_result()

    def report_failure(self):
        self.work_queue[self.mark].report_failure()
