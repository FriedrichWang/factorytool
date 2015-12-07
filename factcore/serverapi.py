#encoding=utf8
import requests
import traceback
from json import dumps as jdumps, loads as jloads
from factcore.setting import Setting
from factcore.logger import Log

class ServerApi(object):
    def checkStep(self, sn, step):
        url = Setting.BASE_CHECKSTEP_URL % {'sn': sn, 'step': Setting.getStepInt(step)}
        Log.d(url)
        try:
            resp = requests.get(url)
        except:
            from factcore.works.workflow import BaseWork
            return {'ret': BaseWork.FAILED, 'desc': u'不能连接服务器'}
        return self.jsonloads(resp.text)

    def uploadResult(self, sn, step, result, descobj={}):
        url = Setting.BASE_STEP_URL % {'sn': sn, 'step': Setting.getStepInt(step),
                                       'result': result}
        Log.d(url)
        data = jdumps(descobj, ensure_ascii=False).encode('utf8')
        try:
            resp = requests.post(url, params={}, data=data)
        except:
            from factcore.works.workflow import BaseWork
            return {'ret': BaseWork.FAILED, 'desc': u'不能连接服务器'}
        return self.jsonloads(resp.text)

    def uploadFile(self, url, _file):
        files = {'adjustData': open(_file, 'rb')}
        resp = requests.post(url, files=files)
        return self.jsonloads(resp.text)

    def jsonloads(self, content):
        Log.d('response --> %s' % content)
        try: return jloads(content)
        except:
            from factcore.works.workflow import BaseWork
            return {'ret': BaseWork.FAILED, 'desc': 'Program exception %s' % \
                    traceback.format_exc()}
    
srvapi = ServerApi()
