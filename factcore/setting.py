class BaseSetting(object):
    DEBUG_UI = False
    AUTO_START = True
    CURRENT_STEP = 'PackBurn'
    DEFAULT_FONT_SIZE = 24
    CLASS_MAP = {}
    def __init__(self):
        self.init()

    def init(self):
        pass

    @classmethod
    def getSetting(cls):
        cls = cls.CLASS_MAP[cls.CURRENT_STEP]
        return cls()

class SMTCheckSetting(BaseSetting):
    def __init__(self):
        from factcore.works.smtworks import SnWriteWork, ScreenWork, \
            BacklightWork, SensorWork, AudioWork, RecordWork
        self.STEPS = [SnWriteWork, ScreenWork, BacklightWork,
                        SensorWork, AudioWork, RecordWork ]
        self.AUTO_START = True

BaseSetting.CLASS_MAP['SMTCheckSetting'] = SMTCheckSetting

class PackBurn(BaseSetting):
    def init(self):
        self.AUTO_START = True

    def getStepWorks(self):
        from factcore.works.packageworks import CheckSNWork, BurnVCOMWork, \
            UpdateCITWork
        return [CheckSNWork, BurnVCOMWork, UpdateCITWork]

BaseSetting.CLASS_MAP['PackBurn'] = PackBurn

class PackCIT(BaseSetting):
    def init(self):
        self.AUTO_START = True

    def getStepWorks(self):
        from factcore.works.packageworks import CITCheckWork, UpdateApkWork, ResetWork
        return [CITCheckWork, UpdateApkWork, ResetWork]

BaseSetting.CLASS_MAP['PackCIT'] = PackCIT

Setting = BaseSetting.getSetting()
