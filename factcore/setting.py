#encoding=utf8
class BaseSetting(object):
    # NOTICE: 正常部署请至 DEBUG_* 为 False
    DEBUG_UI = False  # 不执行 onWork 获取 getDebugRet作为结果, 只调试UI用
    DEBUG_WORK = False# 执行 debugSuccessOutput 作为 output, 以  expect 作为判断依据
    DEBUG_SUCCESS = False# 是调试 success output 还是 failed output 情况
    DEBUG_WORK_INTERVAL = 0.3
    AUTO_START = True
    CURRENT_STEP = 'PackBurn'
    DEFAULT_FONT_SIZE = 12
    DEVICE_CIT_RESULT_PATH = '/data/citresult.txt'
    DEVICE_SN_PATH = '/etc/sn_number'
    CLASS_MAP = {}
    
    BASE_HOST = "http://localhost:8080/mephisto/smt/"
    BASE_STEP_URL = BASE_HOST + "step/%(step)s/%(sn)s/%(result)s"
    BASE_CHECKSTEP_URL = BASE_HOST + 'checkstep/%(step)s/%(sn)s'

    def __init__(self):
        import sys
        if sys.platform == 'win32':
            self.ADB_PATH = 'bin/adb.exe'
        else:
            self.ADB_PATH = "adb"
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
        self.AUTO_START = False

    def getStepWorks(self):
        from factcore.works.packageworks import CheckSNWork, BurnVCOMWork, \
            UpdateCITWork, WaitAdbWork, UploadResult, GetSnWork, CheckStep
        return [CheckStep, WaitAdbWork, GetSnWork, BurnVCOMWork, UpdateCITWork,
                UploadResult]

BaseSetting.CLASS_MAP['PackBurn'] = PackBurn

class PackCIT(BaseSetting):
    def init(self):
        self.AUTO_START = True

    def getStepWorks(self):
        from factcore.works.packageworks import CITCheckWork, UpdateApkWork, \
            ResetWork, WaitAdbWork, UploadResult, GetSnWork, CheckStep
        return [CheckStep, WaitAdbWork, GetSnWork, CITCheckWork, UpdateApkWork,
                ResetWork, UploadResult]

BaseSetting.CLASS_MAP['PackCIT'] = PackCIT

Setting = BaseSetting.getSetting()
