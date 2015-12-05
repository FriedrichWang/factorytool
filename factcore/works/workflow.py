#encoding=utf8
from re import compile
from factcore.ui import BaseWorkUI
from factcore.cmdwrapper import runcmd
from factcore.logger import Log

class BaseWork(BaseWorkUI):
    def __init__(self, name, ctx):
        self._name = name
        self.ctx = ctx
        self.listner = ctx.getListener()
        
    def getName(self):
        return self._name
    
    def work(self):
        ret, output = runcmd(self.cmd)
        if ret != 0: self.listener.onFailed(self)
        m = compile(self.expect).search(output)
        if m:
            Log.d('[%s]%s -> match %s' % (self.getName(), self.expect, m.groups()))
            return True
        else:
            Log.d('[%s]%s -> notmatch' % (self.getName(), self.expect))
            return False
