#encoding=utf8
from factcore.works.workflow import BaseWork

## Step1
class CheckSNWork(BaseWork):
    def __init__(self, ctx):
        super(CheckSNWork, self).__init__(u'检查SN', ctx)
        self.cmd = u'echo "success"'
        self.expect = r'success'

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
