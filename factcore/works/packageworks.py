#encoding=utf8
from factcore.works.workflow import BaseWork
from factcore.cmdwrapper import runcmd
from factcore.logger import Log
from factcore.setting import Setting
from time import sleep

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
        self.result = self.SUCCESS
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
    def onFailed(self):
        ''' NOTE: 复写该方法, 不上传错误信息 '''

class GetSnWork(BaseWork):
    def __init__(self, ctx):
        super(GetSnWork, self).__init__(u'获取SN', ctx)
        
    def onWork(self):
        ret, output = runcmd('adb remount')
        if ret != 0:
            self.err = u'adb remount 失败'
            return self.FAILED
        ret, output = runcmd('adb shell cat "%s"' % Setting.DEVICE_SN_PATH)
        sn = output.strip()
        if len(sn) > 12:
            self.err = u'不能获取SN'
            return self.FAILED
        else:
            self.ctx.showInfo('GetSn "%s"' % sn)
            self.ctx.setSn(sn)
            return self.SUCCESS

## Step1
class CheckSNWork(BaseWork):
    def __init__(self, ctx):
        super(CheckSNWork, self).__init__(u'检查SN', ctx)
        self.ui_hasentry = True
        self.ui.setPauseText(u'请扫描SN:')
        
    def onContinue(self, pass_or_failed):
        param = self.ui.entry.get().strip()
        sn = self.getSn()
        Log.d(u'%s -> %s' % (self.getName(), repr(sn)))
        if sn != param:
            return BaseWork.FAILED
        else:
            return BaseWork.SUCCESS
        self.ctx.setSn(sn)
        return BaseWork.onContinue(self, self.result)

    def getSn(self):
        ret, output = runcmd('adb shell cat "%s"' % Setting.DEVICE_SN_PATH)
        if not ret: return None
        else: return output

class BurnVCOMWork(BaseWork):
    def __init__(self, ctx):
        super(BurnVCOMWork, self).__init__(u'烧写VCOM', ctx)
        self.ui.setPauseText(u'请扫描VCOM值:')
        self.ui_hasentry = True

    def onContinue(self, pass_or_failed=None):
        param = self.ui.entry.get().strip()
        try:
            float(param)
        except:
            self.err = u'请输入数值'
            return self.FAILED
        cmd = 'adb shell "echo %s > %s"' % (param, Setting.DEVICE_VCOM_PATH)
        ret, output = runcmd(cmd)
        output = output.strip()
        if ret != 0 or output:
            self.err = u'写入 VCOM 失败'
            self.ctx.showInfo(output)
            return self.FAILED
        ret, output =  runcmd('adb shell "cat %s"' % Setting.DEVICE_VCOM_PATH)
        output = output.strip()
        if output != param:
            self.err = u'写入 VCOM 不一致'
            self.ctx.showInfo(u'"%s"\n"%s"' % (param, output))
            return self.FAILED
        return self.SUCCESS

class UpdateCITWork(BaseWork):
    def __init__(self, ctx):
        super(UpdateCITWork, self).__init__(u'更新CIT', ctx)
        self.cmd = 'adb push data/FactoryTool.apk /system/app/FactoryTool/FactoryTool.apk'
        self.expect = r'KB/s'

    def onWork(self):
        ret, output = runcmd('adb shell rm "%s"' % Setting.DEVICE_CIT_RESULT_PATH)
        if ret != 0:
            Log.w('CIT RESULT not exists\n%s' % output)

        # TODO: push other files, so
        cmds = []
        cmds.append('adb remount')
        cmds.append('adb push data/audio.primary.imx6.so /system/lib/hw/')
        cmds.append('adb push data/libinputflinger.so /system/lib/')
        cmds.append('adb push data/gralloc.imx6.so /system/lib/hw/')
        success_snipptes = ['remount succeeded', 'KB/s',]
        for cmd in cmds:
            ret, output = runcmd(cmd)
            Log.d(cmd)
            output = output.strip()
            if ret != 0:
                self.err = output
                return self.FAILED
            # match success outputs
            matchsnippet = False
            for snippet in success_snipptes:
                if snippet in output:
                    matchsnippet = True
                    break
            if matchsnippet: continue

            if output:
                self.err = output
                return self.FAILED

        return super(UpdateCITWork, self).onWork()

## Step2
class CITCheckWork(BaseWork):
    def __init__(self, ctx):
        super(CITCheckWork, self).__init__(u'检查CIT', ctx)
        self.cmd = 'adb shell cat /data/citresult.txt'
        self.expect = r'allpass\tpass'
        
class WifiCheck(BaseWork):
    def __init__(self, ctx):
        super(WifiCheck, self).__init__(u'检查wifi', ctx)
        self.cmd = 'adb shell "/data/wl.dat scanresults"'
        self.expect = r'SSID:'

    def onWork(self):
        cmds = []
        cmds.append('adb remount')
        cmds.append('adb push data/cfg80211.ko /system/lib/modules/')
        cmds.append('adb push data/bcmdhd.ko /system/lib/modules/')
        cmds.append('adb push data/nvram.txt /etc/')
        cmds.append('adb push data/fw_bcmdhd.bin /etc/')
        cmds.append('adb push data/wl.dat /data/')
        cmds.append('adb shell "busybox chmod +x /data/wl.dat"')
        cmds.append('adb shell "insmod /system/lib/modules/cfg80211.ko"')
        cmds.append('adb shell "insmod /system/lib/modules/bcmdhd.ko nvram_path=/etc/nvram.txt firmware_path=/etc/fw_bcmdhd.bin"')

        cmds.append('adb shell "busybox ifconfig wlan0 up"')
        cmds.append('adb shell "/data/wl.dat scan"')
        success_snipptes = ['remount succeeded', 'KB/s',
                            '(File exists)']
        for cmd in cmds:
            ret, output = runcmd(cmd)
            Log.d(cmd)
            output = output.strip()
            if ret != 0:
                self.err = output
                return self.FAILED
            # match success outputs
            matchsnippet = False
            for snippet in success_snipptes:
                if snippet in output:
                    matchsnippet = True
                    break
            if matchsnippet: continue

            if output:
                self.err = output
                return self.FAILED

        # wait scan results perpared
        cmd = 'adb shell "/data/wl.dat" scanresults'
        expectstr = '/data/wl.dat: Not Ready'
        while True:
            sleep(1)
            ret, output = runcmd(cmd)
            if expectstr not in output: break

        return BaseWork.onWork(self)

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
