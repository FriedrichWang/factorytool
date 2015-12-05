from factcore.works.smtworks import SnWriteWork, ScreenWork, \
    BacklightWork, SensorWork, AudioWork, RecordWork

from factcore.works.packageworks import CheckSNWork, BurnVCOMWork, \
    UpdateCITWork, CITCheckWork, UpdateApkWork, ResetWork

class Setting(object):
    AUTO_START = False
    CURRENT_STEP = 'PackBurn'
    STEPS = {
             'SMTCheck': [SnWriteWork, ScreenWork, BacklightWork,
                          SensorWork, AudioWork, RecordWork ],
             'PackBurn': [CheckSNWork, BurnVCOMWork, UpdateCITWork],
             'PackCIT': [CITCheckWork, UpdateApkWork, ResetWork]
             }
    @classmethod
    def getStepWorks(cls):
        return cls.STEPS[cls.CURRENT_STEP]
