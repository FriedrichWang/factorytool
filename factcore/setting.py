
class Setting(object):
    DEBUG_UI = False
    AUTO_START = False
    CURRENT_STEP = 'PackBurn'
    @classmethod
    def getStepWorks(cls):
        from factcore.works.smtworks import SnWriteWork, ScreenWork, \
            BacklightWork, SensorWork, AudioWork, RecordWork

        from factcore.works.packageworks import CheckSNWork, BurnVCOMWork, \
            UpdateCITWork, CITCheckWork, UpdateApkWork, ResetWork
        STEPS = {
             'SMTCheck': [SnWriteWork, ScreenWork, BacklightWork,
                          SensorWork, AudioWork, RecordWork ],
             'PackBurn': [CheckSNWork, BurnVCOMWork, UpdateCITWork],
             'PackCIT': [CITCheckWork, UpdateApkWork, ResetWork]
             }
        return STEPS[cls.CURRENT_STEP]
