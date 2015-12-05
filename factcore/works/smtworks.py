#encoding=utf8
from factcore.works.workflow import BaseWork

class SnWriteWork(BaseWork): 
    def __init__(self, ctx):
        super(SnWriteWork, self).__init__(u'Sn烧写', ctx)
    
class ScreenWork(BaseWork):
    def __init__(self, uicb):
        super(ScreenWork, self).__init__(u'屏幕测试', uicb)
        
class BacklightWork(BaseWork):
    def __init__(self, uicb):
        super(BacklightWork, self).__init__(u'背光测试', uicb)
        
class SensorWork(BaseWork):
    def __init__(self, uicb):
        super(SensorWork, self).__init__(u'传感器测试', uicb)
        
class AudioWork(BaseWork):
    def __init__(self, uicb):
        super(AudioWork, self).__init__(u'音频测试', uicb)
        
class RecordWork(BaseWork):
    def __init__(self, uicb):
        super(RecordWork, self).__init__(u'录音测试', uicb)
