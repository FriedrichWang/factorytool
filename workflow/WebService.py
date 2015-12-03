__author__ = 'friedrich'

import requests


class WebService(object):

    def __init__(self):
        self.url = ""

    def reload_url(self, _url):
        self.url = _url

    def make_request(self, _params, _entity):
        _result = requests.post(self.url, params=_params, data=_entity)
        return _result.text

    def upload_request(self, _file):
        _files = {'adjustData': open(_file, 'rb')}
        _result = requests.post(self.url, files=_files)
        return _result.text

