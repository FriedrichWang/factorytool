#!/bin/python
# -*- coding: utf-8 -*-
#coding=utf-8
__author__ = 'friedrich'


BASE_HOST = "http://172.27.13.238:8080/mephisto/smt/"
BASE_STEP_URL = BASE_HOST + "step/{0}/{1}/{2}"
BASE_CHECKSTEP_URL = BASE_HOST + 'checkstep/%(step)s/%(sn)s'
SN_URL = BASE_HOST + "sn/{0}"
ADJUST_URL = BASE_HOST + "adjust/{0}"

ADB_PATH = "/home/friedrich/sdk/platform-tools/adb"

ID = "sn"
STEP = "step"

RESULT_UNKNOWN = 0
RESULT_OK = 1
RESULT_FAILED = 2
RESULT_NONSTOP_FAILED = 3
RESULT_FINISH = 4
RESULT_CONTINUE = 5

ALL_PASS = "state"
PRODUCT_CODE = "produceCode"
HARDWARE_CODE = "hardwareCode"

DEVICE_SERIAL = "e70a976b"

DEFAULT_HOME = "/home/friedrich/"
DEFAULT_ZIP_DIC = DEFAULT_HOME + "adjust_zip/"
DEFAULT_FILE = DEFAULT_HOME + "/adjust/"

DEBUG = True