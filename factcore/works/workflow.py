#encoding=utf8
from re import compile
from factcore.ui import BaseWorkUI
from factcore.cmdwrapper import runcmd
from factcore.logger import Log
from factcore.setting import Setting
from factcore.exceptions import FactRuntimeError
from time import sleep

class BaseWork(object):
    UNKNOWN = -1
    SUCCESS = 1
    FAILED = 2
    PAUSE = 3
    def __init__(self, name, ctx, uicls=BaseWorkUI):
        self.result = BaseWork.UNKNOWN
        self._name = name
        self.ctx = ctx
        self.ui_hasentry = False
        self._flag_onBegin = False
        self._flag_onEnd = False
        self._flag_doWork = False
        self.cmd = u'echo "success"'
        self.expect = r'success'
        self.ui = uicls(self, ctx)

    def onInit(self):
        ''' Invoke: 在 workflow 流程初始化时调用'''

    def onBegin(self):
        ''' Invoke: 在 onWork 执行前执行 '''
        self._flag_onBegin = True
        self.ui.onBeginUI()
        
    def getName(self):
        return self._name
    
    def onWork(self):
        ''' Invoke: 工作函数主体, 返回 PAUSE 时等待用户输入entry或者等待点击按钮'''
        if self.ui_hasentry: return BaseWork.PAUSE
        ret, output = runcmd(self.cmd)
        if ret != 0:
            Log.e('[%s]runcmd failed -> %s' % (self.getName(), self.cmd))
            return BaseWork.FAILED
        m = compile(self.expect).search(output)
        if m:
            Log.d('(SUCCESS)[%s] %s -> match %s' % (self.getName(), self.expect, m.groups()))
            return BaseWork.SUCCESS
        else:
            Log.raw('Output:\n%s' % output)
            Log.e('(FAILED)[%s] %s -> not match' % (self.getName(), self.expect))
            return BaseWork.FAILED
        
    def onEnd(self):
        ''' Invoke: 在 onWork 执行 后调用, 可以查看 self.result 结果'''
        self._flag_onEnd = True

    def onPause(self):
        ''' Invoke: 在 onWork 返回 PAUSE 时被调用 '''
        
    def onContinue(self, pass_or_failed=None):
        ''' Invoke: 接受一个参数 , 是操作者点击了 成功(BaseResult.SUCCESS) 或者 失败(BaseResult.FAILED)
            Output: 需要设置 self.result 为  SUCCESS 或者 FAILED, OnEnd 会使用该结果, 无返回
        '''

    def __unicode__(self):
        return u'%s -- %s' % (self.__class__, self.getName())
    
    def __str__(self):
        return '%s -- %s' % (self.__class__, self.getName())
    
    def debugSuccessOutput(self):
        return u'success'
    
    def debugFailedOutput(self):
        return u'failed'
    
    def getDebugRet(self):
        if self.ui_hasentry: return BaseWork.PAUSE
        elif Setting.DEBUG_SUCCESS: return BaseWork.SUCCESS
        else: return BaseWork.FAILED
    
    def onDebugWork(self):
        if self.ui_hasentry: return BaseWork.PAUSE
        if Setting.DEBUG_SUCCESS:
            output = self.debugSuccessOutput()
        else:
            output = self.debugFailedOutput()
        m = compile(self.expect).search(output)
        if m:
            Log.i('(SUCCESS)DebugWork!!![%s] "%s" -> match %s' % (self.getName(), self.expect, m.groups()))
            return BaseWork.SUCCESS
        else:
            Log.raw('Output:\n%s' % output)
            Log.e('(FAILED)DebugWork!!![%s] "%s" -> not match' % (self.getName(), self.expect))
            return BaseWork.FAILED
    
    def debugCheckFinishedFlags(self):
        if self._flag_doWork is not True:
            return # not invoke doWork, every thing be OK.
        if self._flag_onBegin is not True:
            raise FactRuntimeError(u'%s onBegin not be called' % self.getName())
        if self._flag_onEnd is not True:
            raise FactRuntimeError(u'%s onEnd not be called' % self.getName())

    @classmethod
    def ResultToName(cls, res):
        if res == BaseWork.SUCCESS:
            return 'SUCCESS'
        elif res == BaseWork.FAILED:
            return 'FAILED'
        elif res == BaseWork.PAUSE:
            return 'PAUSE'
        elif res == BaseWork.UNKNOWN:
            return 'UNKOWN'
        else:
            return 'UNEXPECTED %s' % res

class Context(object):
    def __init__(self, win):
        self.workclss = []
        self.works = []
        self.win = win
        self.dirty = ''
        self.curwork = None
        self.workiter = None
    
    def getRoot(self):
        return self.win.root

    def initWorkClss(self, clss):
        self.workclss = clss

    def reInitWorks(self):
        # debug check flags
        Log.d('reInitWorks')
        self.curwork = None
        for work in self.works:
            work.debugCheckFinishedFlags()

        self.win.cleanMainFrame()
        self.works = []
        for cls in self.workclss:
            work = cls(self)
            self.works.append(work)
            work.onInit()
            work.ui.onInitUI(self.win.getMainFrame())
        self.workiter = self.iterWork()
        self.win.showStartButton()
    
    def start(self):
        self.win.root.after(0, self._start)

    def _start(self):
        Log.i('start do...')
        # check previous status, if failed, break return
        if self.curwork and self.curwork.result == BaseWork.FAILED:
            self._endCurrentWork()
            self.win.showRestartButton()
            return
        if self.workiter is None:
            self.workiter = self.iterWork()
        while True:
            work = self.workiter.next()
            if work == None:
                self.reset()
                break
            Log.d('%s->%s' % (work, BaseWork.ResultToName(work.result)))
            if work.result == BaseWork.PAUSE:
                break
            elif work.result == BaseWork.FAILED:
                self._endCurrentWork()
                self.win.showRestartButton()
                break

    def iterWork(self):
        for work in self.works:
            if self.curwork:
                self._endCurrentWork()
            work.onBegin()
            if Setting.DEBUG_UI:
                ret = work.getDebugRet()
                sleep(Setting.DEBUG_WORK_INTERVAL)
            elif Setting.DEBUG_WORK:
                ret =  work.onDebugWork()
                sleep(Setting.DEBUG_WORK_INTERVAL)
            else:
                ret = work.onWork()
                work._flag_doWork = True
            work.result = ret
            self.curwork = work
            yield self.incStep(work)
        if self.curwork:
            self._endCurrentWork()
        self.curwork = None
        yield None

    def incStep(self, work, iscontinue=False):
        if not work:
            raise RuntimeError('Can not get work with work(%s)\nworks(%s)' % \
                               (work, self.works))
        if iscontinue:
            if Setting.DEBUG_WORK or Setting.DEBUG_UI:
                if work.result not in (BaseWork.SUCCESS, BaseWork.FAILED):
                    if Setting.DEBUG_SUCCESS: work.result = BaseWork.SUCCESS
                    else: work.result = BaseWork.FAILED
                sleep(Setting.DEBUG_WORK_INTERVAL)
            else:
                work.onContinue(work.result)
                work.ui.onContinueUI(work.result)
            if work.result not in (BaseWork.SUCCESS, BaseWork.FAILED):
                raise FactRuntimeError('(%s) onContinue should set works\'s ' % work \
                                        +'result(%s) to SUCCESS or FAILED' % \
                                        BaseWork.ResultToName(work.result))
        if work.result == BaseWork.SUCCESS:
            work.ui.onSuccessUI()
        elif work.result == BaseWork.FAILED:
            work.ui.onFailedUI()
        elif work.result == BaseWork.PAUSE:
            work.onPause()
            work.ui.onPauseUI()
            return work
        elif work.result == BaseWork.UNKNOWN:
            work.result = work.onWork()
            work._flag_doWork = True
        else:
            raise FactRuntimeError('Unknown work(%s) return code "%s"' % \
                               (work, work.result))
        return work

    def reset(self, force=False):
        if force:
            self.reInitWorks()
        else:
            allsuccess = True
            for work in self.works:
                if work.result != BaseWork.SUCCESS:
                    allsuccess = False
                    break
            if not allsuccess:
                self.win.showRestartButton()
            else:
                self.reInitWorks()

    def _endCurrentWork(self):
        if self.curwork:
            self.curwork.onEnd()
            self.curwork.ui.onEndUI()
            self.curwork = None
