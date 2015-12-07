#encoding=utf8
from re import compile
from factcore.works.workflow import BaseWork
from factcore.ui import BaseWorkUI
from factcore.cmdwrapper import runcmd
from factcore.logger import Log
from factcore.setting import Setting
from factcore.serverapi import srvapi

## common step
class CheckStep(BaseWork):
    def __init__(self, ctx):
        super(CheckStep, self).__init__(u'卡站%s' % Setting.CURRENT_STEP, ctx)

    def onWork(self):
        resp = self.ctx.checkStep()
        self.err = resp.get('desc', '')
        return resp['ret']
    
class UploadResult(BaseWork):
    def __init__(self, ctx):
        super(UploadResult, self).__init__(u'上传日志', ctx)
        
    def onWork(self):
        resp = self.ctx.uploadResult()
        self.err = resp.get('desc', '')
        return resp['ret']

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

class GetSnWork(BaseWork):
    def __init__(self, ctx):
        super(GetSnWork, self).__init__(u'获取SN', ctx)
        
    def onWork(self):
        ret, output = runcmd('adb shell cat "%s"' % Setting.DEVICE_SN_PATH)
        if ret != 0:
            self.err = u'不能获取SN'
            return BaseWork.FAILED
        else:
            Log.d('GetSn "%s"' % output)
            self.ctx.setSn(output)

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
        self.ctx.setSn(sn)
        BaseWork.onContinue(self, self.result)

    def getSn(self):
        ret, output = runcmd('adb shell cat "%s"' % Setting.DEVICE_SN_PATH)
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

    def onWork(self):
        ret, output = runcmd('adb shell rm "%s"' % Setting.DEVICE_CIT_RESULT_PATH)
        if ret != 0:
            Log.w('CIT RESULT not exists\n%s' % output)
        return BaseWork.onWork(self)

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
