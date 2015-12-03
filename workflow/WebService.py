__author__ = 'friedrich'

import requests
import traceback
from json import loads as jloads

class WebService(object):
    def __init__(self):
        pass

    def make_request(self, url, _params={}, _entity=''):
        _result = requests.post(url, params=_params, data=_entity)
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
        return {'ret': 1, 'desc': 'Debug pass'}

    def upload_request(self, url, _file):
        return {'ret': 1, 'desc': 'Debug pass'}
