#!/bin/python
# -*- coding: utf-8 -*-
#coding=utf-8

from threading import Thread
from Tkinter import Tk
from Tkinter import Label
from Tkinter import LEFT
from Tkinter import RIGHT
from Tkinter import BOTTOM
from Tkinter import Frame
from Tkinter import LabelFrame
from Tkinter import Button
from Tkinter import StringVar
from Tkinter import DISABLED
from Tkinter import NORMAL
from Tkinter import Entry

from workflow.FlowContext import FlowContext as Context
from workflow.Bundle import Bundle
from workflow.Listener import Listener
from rom.RomController import RomController
from smt.SmtController import SmtController
from sn.SnController import SnController
from adb.AdbController import AdbController
from data.DataController import DataController
from adjust.AdjustController import AdjustController
from backup.BackupController import BackupController
from bookset.BookSetController import BookSetController
from reset.ResetController import ResetController
from printtag.PrintController import PrintController
from weight.WeightController import WeightController
from setting import Setting as Env

input_bundle = Bundle()
stamp_bundle = Bundle()
controllers = []
context = Context(input_bundle, stamp_bundle)
main_frame = None
state_label = None
state_label_var = None
state_indicator = None
state_indicator_var = None
start_button = None
stop_button = None
sn_input = None
title_list = []

state_code = Env.RESULT_OK
mark = 0


class MainListener(Listener):
    def __init__(self):
        Listener.__init__(self)

    def on_result(self, _request_id, _response_code, _stamp_bundle, _sub_process=0):
        print('on_result request_id(%s) response_code(%s) stamp_bundle(%s) sub_process(%s)' % \
              (_request_id, _response_code, _stamp_bundle, _sub_process))
        if _response_code == Env.RESULT_FINISH:
            state_label_var.set(u'准备Smt测试')
            state_label['background'] = '#00BFFF'
            state_indicator['background'] = '#00BFFF'
            start_button['text'] = u'开始测试'
            stop_button['state'] = DISABLED
            return
        if _request_id == 0:
            sn_input['state'] = NORMAL
        else:
            sn_input['state'] = DISABLED
        if _request_id == 2:
            state_label_var.set(Env.SMT_TEST_SUB_PROCESS[_sub_process - 1])
            if _sub_process == 6:
                start_button['text'] = u'上传报告'
            else:
                stop_button['state'] = NORMAL
        else:
            state_label_var.set(title_list[_request_id])
            context.mark_up()
            start_button['text'] = u'继续测试'
            stop_button['state'] = DISABLED
        if _response_code == Env.RESULT_OK:
            state_indicator_var.set(u'成功')
            state_label['background'] = '#2E8B57'
            state_indicator['background'] = '#2E8B57'
        else:
            state_indicator_var.set(u'失败')
            state_label['background'] = '#DC143C'
            state_indicator['background'] = '#DC143C'


listener = MainListener()


class Task(Thread):

    def run(self):
        context.run()


def initialize():
    #_rom_controller = RomController(0, stamp_bundle, listener)
    #controllers.append(_rom_controller)
    #title_list.append(u'rom烧写')
    _sn_controller = SnController(1, stamp_bundle, listener)
    controllers.append(_sn_controller)
    title_list.append(u'Sn烧录')
    _adb_controller = AdbController(2, stamp_bundle, listener)
    controllers.append(_adb_controller)
    title_list.append(u'Smt测试')
    #_data_controller = DataController(4, stamp_bundle, listener)
    #controllers.append(_data_controller)
    #title_list.append(u'数据保存')
    #_adjust_controller = AdjustController(5, stamp_bundle, listener)
    #controllers.append(_adjust_controller)
    #title_list.append(u'wifi校准')
    #_backup_controller = BackupController(6, stamp_bundle, listener)
    #controllers.append(_backup_controller)
    #title_list.append(u'it备份')
    #_book_set_controller = BookSetController(7, stamp_bundle, listener)
    #controllers.append(_book_set_controller)
    #title_list.append(u'预置书籍')
    #_reset_controller = ResetController(8, stamp_bundle, listener)
    #controllers.append(_reset_controller)
    #title_list.append(u'重置系统')
    #_print_controller = PrintController(9, stamp_bundle, listener)
    #controllers.append(_print_controller)
    #title_list.append(u'打印标签')
    #_weight_controller = WeightController(10, stamp_bundle, listener)
    #controllers.append(_weight_controller)
    #title_list.append(u'彩盒称重')


def start_run():
    print('Running')
    state_label['background'] = '#00BFFF'
    state_indicator['background'] = '#00BFFF'
    if context.mark == 1:
        input_bundle.params['sn_number'] = sn_input.get()
    context.run()


def stop_test():
    _retval = context.report_failure()
    if _retval == Env.RESULT_FAILED:
        context.clear()
    state_indicator_var.set(u'失败')
    state_label['background'] = '#DC143C'
    state_indicator['background'] = '#DC143C'


if __name__ == '__main__':
    initialize()
    context.init_controller(controllers)
    root = Tk()
    state_label_var = StringVar()
    state_indicator_var = StringVar()
    title = u'产线工具'
    label_frame_title = u'产线测试工具客户端'
    root.title(title)
    root.geometry('800x260')
    label_frame = LabelFrame(root, text=label_frame_title)
    label_frame.pack(fill="both", expand="yes")
    main_frame = Frame(label_frame)
    main_frame.pack()
    state_label_var.set(u'准备Smt测试')
    state_label = Label(main_frame, textvariable=state_label_var, font=("Arial", 12), width=40, height=7, bg="#00BFFF")
    state_label.pack(side=LEFT)
    state_indicator_var.set(u'未测试')
    state_indicator = Label(main_frame, textvariable=state_indicator_var, font=("Arial", 12), width=40, height=7, bg="#00BFFF")
    state_indicator.pack(side=LEFT)
    control_frame = LabelFrame(label_frame)
    control_frame.pack(side=BOTTOM, fill="both", expand="yes")
    #start_button = Button(control_frame, text=u'开始测试', font=("Arial", 12), width=15, height=3, command=start_run)
    stop_button = Button(control_frame, text=u'标记失败', font=("Arial", 12), width=15, height=3, command=stop_test)
    #start_button.pack(side=LEFT)
    root.after(2000, start_run)
    stop_button.pack(side=RIGHT)
    stop_button['state'] = DISABLED
    sn_input = Entry(control_frame)
    sn_input.pack()
    sn_input['state'] = DISABLED
    root.resizable(width=False, height=False)
    root.mainloop()
