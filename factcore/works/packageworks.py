#encoding=utf8
from re import compile
from factcore.works.workflow import BaseWork
from factcore.ui import BaseWorkUI
from factcore.cmdwrapper import runcmd
from factcore.logger import Log

## common step
class WaitAdbWork(BaseWork):
    def __init__(self, ctx):
        super(WaitAdbWork, self).__init__(u'等待Adb', ctx)
        self.cmd = u'adb devices'
        self.expect = r'\bdevice\b'
        
    def debugSuccessOutput(self):
        return '''
adb server is out of date.  killing...
* daemon started successfully *
List of devices attached 
e70a976b    device
'''

    def debugFailedOutput(self):
        return '''
error:

'''

## Step1
class CheckSNWork(BaseWork):
    def __init__(self, ctx):
        super(CheckSNWork, self).__init__(u'检查SN', ctx)
        self.ui_hasentry = True
        self.ui.setPauseText(u'请扫描SN:')
        
    def onContinue(self, pass_or_failed):
        param = self.ui.entry.get()
        sn = self.getSn()
        Log.d(u'%s -> %s' % (self.getName(), repr(sn)))
        if sn != param:
            self.result = BaseWork.FAILED
        else:
            self.result = BaseWork.SUCCESS
        BaseWork.onContinue(self, self.result)

    def getSn(self):
        ret, output = runcmd('adb shell cat /etc/sn_number')
        if not ret: return None
        else: return output

class BurnVCOMWork(BaseWork):
    def __init__(self, ctx):
        super(BurnVCOMWork, self).__init__(u'烧写VCOM', ctx)
        self.ui.setPauseText(u'请扫描VCOM值:')
        self.ui_hasentry = True

    def getDebugRet(self):
        return BaseWork.PAUSE

class UpdateCITWork(BaseWork):
    def __init__(self, ctx):
        super(UpdateCITWork, self).__init__(u'更新CIT', ctx)
        self.cmd = 'adb push cit.apk /system/app/cit.apk'
        self.expect = r'success'

    def getDebugRet(self):
        return BaseWork.PAUSE

## Step2
class CITCheckWork(BaseWork):
    def __init__(self, ctx):
        super(CITCheckWork, self).__init__(u'检查CIT', ctx)
        self.cmd = 'adb shell cat /data/citresult.txt'
        self.expect = u'AllPass'

class UpdateApkWork(BaseWork):
    def __init__(self, ctx):
        super(UpdateApkWork, self).__init__(u'更新Apk', ctx)
        self.cmd = 'adb push data/yuewen.apk /system/app/yuewen.apk'
        self.expect = u'success'
        
class ResetWork(BaseWork):
    def __init__(self, ctx):
        super(ResetWork, self).__init__(u'重置', ctx)
        self.cmd = 'adb shell reboot recovery --reset'
        self.expect = 'success'
