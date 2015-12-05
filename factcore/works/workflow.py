#encoding=utf8
from re import compile
from factcore.ui import BaseWorkUI
from factcore.cmdwrapper import runcmd
from factcore.logger import Log
from setting import Setting

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
        
    def onInit(self):
        pass

    def onBegin(self):
        self.ui.onBeginUI()
        
    def getName(self):
        return self._name
    
    def onWork(self):
        ret, output = runcmd(self.cmd)
        if ret != 0: self.listener.onFailed(self)
        m = compile(self.expect).search(output)
        if m:
            Log.d('[%s]%s -> match %s' % (self.getName(), self.expect, m.groups()))
            return BaseWork.SUCCESS
        else:
            Log.d('[%s]%s -> notmatch' % (self.getName(), self.expect))
            return BaseWork.FAILED
        
    def onEnd(self):
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

class Context(object):
    def __init__(self, win):
        self.works = []
        self.curworkidx = 0
        self.win = win
    
    def getRoot(self):
        return self.win.root

    def appendWork(self, work):
        self.works.append(work)
    
    def start(self):
        self.win.root.after(0, self._start)

    def _start(self):
        while self.curworkidx < len(self.works):
            work = self.works[self.curworkidx]
            work.onBegin()
            if Setting.DEBUG:
                ret = work.getDebugRet()
            else:
                ret = work.onWork()

            if self.incStep(ret): break # pause break

    def getCurWork(self):
        if self.curworkidx < len(self.works):
            return self.works[self.curworkidx]

    def incStep(self, ret, iscontinue=False):
        work = self.getCurWork()
        if not work:
            raise RuntimeError('Can not get work with id(%s)\nworks(%s)' % \
                               (self.curworkidx, self.works))
        work.result = ret
        if iscontinue:
            work.ui.onContinueUI()
        if ret == BaseWork.SUCCESS:
            work.ui.onSuccessUI()
        elif ret == BaseWork.FAILED:
            work.ui.onFailedUI()
        elif ret == BaseWork.PAUSE:
            work.onPause()
            work.ui.onPauseUI()
            return True
        else:
            raise RuntimeError('Unknown work(%s) return code %s' % \
                               (work, ret))
        work.onEnd()
        self.curworkidx += 1
        return False
