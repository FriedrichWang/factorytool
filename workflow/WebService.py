__author__ = 'friedrich'

import requests
import traceback
from json import loads as jloads, dumps as jdumps
from setting import Setting

class WebService(object):
    def __init__(self):
        pass

    def make_request(self, url, _params={}, _entity={}):
        _result = requests.post(url, params=_params, data=jdumps(_entity))
        return self.jsonloads(_result.text)

    def upload_request(self, url, _file):
        _files = {'adjustData': open(_file, 'rb')}
        _result = requests.post(url, files=_files)
        return self.jsonloads(_result.text)

    def jsonloads(self, content):
        try:
            return jloads(content)
        except:
            return {'ret': 0, 'desc': 'Program exception %s' % traceback.format_exc()}
        
class FakeWebService(WebService):
    def make_request(self, url, _params={}, _entity=''):
        return {'ret': 1, 'desc': 'Debug pass', Setting.ID: _params[Setting.ID],
                Setting.STEP: _params[Setting.STEP]}

    def upload_request(self, url, _file):
        return {'ret': 1, 'desc': 'Debug pass', Setting.ID: 'test_sn'}
