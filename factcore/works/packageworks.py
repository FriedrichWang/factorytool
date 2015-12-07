#encoding=utf8
from re import compile
from factcore.works.workflow import BaseWork
from factcore.ui import BaseWorkUI
from factcore.cmdwrapper import runcmd

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
        self.cmd = u'echo "success"'
        self.expect = r'success'
        self.ui_hasentry = True
        self.ui.setPauseText(u'请输入SN:')

    def onWork(self):
        return BaseWork.PAUSE
        
    def onContinue(self, pass_or_failed):
        param = self.ui.entry.get()
        sn = self.getSn()
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
        self.cmd = u'echo "success"'
        self.expect = r'success'

    def getDebugRet(self):
        return BaseWork.PAUSE

class UpdateCITWork(BaseWork):
    def __init__(self, ctx):
        super(UpdateCITWork, self).__init__(u'更新CIT', ctx)
        self.cmd = u'echo "success"'
        self.expect = r'success'

## Step2
class CITCheckWork(BaseWork):
    def __init__(self, ctx):
        super(CITCheckWork, self).__init__(u'检查CIT', ctx)

class UpdateApkWork(BaseWork):
    def __init__(self, ctx):
        super(UpdateApkWork, self).__init__(u'更新Apk', ctx)
        self.cmd = u'echo "success"'
        self.expect = r'success'
        
class ResetWork(BaseWork):
    def __init__(self, ctx):
        super(ResetWork, self).__init__(u'重置', ctx)
        self.cmd = u'echo "success"'
        self.expect = r'success'
        
    def getDebugRet(self):
        return BaseWork.PAUSE
