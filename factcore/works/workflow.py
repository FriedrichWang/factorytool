#encoding=utf8
from re import compile
from factcore.ui import BaseWorkUI
from factcore.cmdwrapper import runcmd
from factcore.logger import Log
from factcore.setting import Setting
from factcore.exceptions import FactRuntimeError

class BaseWork(object):
    UNKNOWN = -1
    SUCCESS = 1
    FAILED = 2
    PAUSE = 3
    def __init__(self, name, ctx, uicls=BaseWorkUI):
        self.result = BaseWork.UNKNOWN
        self._name = name
        self.ctx = ctx
        self.ui = uicls(self, ctx)
        self._flag_onBegin = False
        self._flag_onEnd = False

    def onInit(self):
        pass

    def onBegin(self):
        self._flag_onBegin = True
        self.ui.onBeginUI()
        
    def getName(self):
        return self._name
    
    def onWork(self):
        ret, output = runcmd(self.cmd)
        if ret != 0:
            Log.e('[%s]runcmd faield -> %s' % (self.getName(), self.cmd))
            return BaseWork.FAILED
        m = compile(self.expect).search(output)
        if m:
            Log.i('[%s]%s -> match %s' % (self.getName(), self.expect, m.groups()))
            return BaseWork.SUCCESS
        else:
            Log.e('[%s]%s -> notmatch' % (self.getName(), self.expect))
            return BaseWork.FAILED
        
    def onEnd(self):
        self._flag_onEnd = True
        self.ui.onEndUI()

    def onPause(self):
        self.ui.onPauseUI()
        
    def onContinue(self, pass_or_failed):
        self.ui.onContinueUI(pass_or_failed)

    def __unicode__(self):
        return self.getName()
    
    def __str__(self):
        return self.getName()
    
    def getDebugRet(self):
        return BaseWork.SUCCESS
    
    def debugCheckFinishedFlags(self):
        if self._flag_onBegin is not True:
            raise FactRuntimeError(u'%s onBegin not be called' % self.getName())
        if self._flag_onEnd is not True:
            raise FactRuntimeError(u'%s onEnd not be called' % self.getName())


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
        self.reInitWorks()

    def reInitWorks(self):
        # debug check flags
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
        self.win.resetStartButton()
    
    def start(self):
        self.win.root.after(0, self._start)

    def _start(self):
        print('start do...')
        if self.workiter is None:
            self.workiter = self.iterWork()
        while True:
            work = self.workiter.next()
            if work == None:
                self.reset()
                break
            print(repr(work))
            if work.result == BaseWork.PAUSE:
                break

    def iterWork(self):
        for work in self.works:
            if self.curwork:
                self.curwork.onEnd()
            work.onBegin()
            if Setting.DEBUG_UI:
                ret = work.getDebugRet()
            else:
                ret = work.onWork()
            work.result = ret
            self.curwork = work
            yield self.incStep(work)
        if self.curwork:
            self.curwork.onEnd()
        self.curwork = None
        yield None

    def getCurWork(self):
        if self.curworkidx < len(self.works):
            return self.works[self.curworkidx]

    def incStep(self, work, iscontinue=False):
        if not work:
            raise RuntimeError('Can not get work with work(%s)\nworks(%s)' % \
                               (work, self.works))
        if iscontinue:
            work.ui.onContinueUI()
        if work.result == BaseWork.SUCCESS:
            work.ui.onSuccessUI()
        elif work.result == BaseWork.FAILED:
            work.ui.onFailedUI()
        elif work.result == BaseWork.PAUSE:
            work.onPause()
            work.ui.onPauseUI()
            return work
        else:
            raise RuntimeError('Unknown work(%s) return code %s' % \
                               (work, work.result))
        return work

    def reset(self):
        self.reInitWorks()

    def showRestart(self):
        # TODO
        print('showRestart')
