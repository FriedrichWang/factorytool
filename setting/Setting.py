#!/bin/python
# -*- coding: utf-8 -*-
#coding=utf-8
__author__ = 'friedrich'


BASE_HOST = "http://localhost:8080/mephisto/smt/"
BASE_STEP_URL = BASE_HOST + "step/{0}/{1}/{2}"
SN_URL = BASE_HOST + "sn/{0}"
ADJUST_URL = BASE_HOST + "adjust/{0}"

ADB_PATH = "/home/friedrich/sdk/platform-tools/adb"

ID = "id"
STEP = "step"

RESULT_UNKNOWN = 0
RESULT_OK = 1
RESULT_FAILED = 2
RESULT_NONSTOP_FAILED = 3
RESULT_FINISH = 4

ALL_PASS = "state"
PRODUCT_CODE = "produceCode"
HARDWARE_CODE = "hardwareCode"

DEVICE_SERIAL = "e70a976b"

DEFAULT_HOME = "/home/friedrich/"
DEFAULT_ZIP_DIC = DEFAULT_HOME + "adjust_zip/"
DEFAULT_FILE = DEFAULT_HOME + "/adjust/"

SMT_TEST_SUB_PROCESS = [u'wifi测试', u'屏幕测试', u'背光测试', u'传感器测试', u'音频测试', u'录音测试', u'上传报告']
