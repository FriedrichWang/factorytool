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
from tkFont import Font

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

root = Tk()
input_bundle = Bundle()
stamp_bundle = Bundle()
controllers = []
context = Context(input_bundle, stamp_bundle)
main_frame = None
state_label = None
state_label_var = None
state_indicator = None
state_indicator_var = None
success_button = None
failed_button = None
sn_input = None
title_list = []

state_code = Env.RESULT_OK
mark = 0

class MainListener(Listener):
    def __init__(self):
        Listener.__init__(self)
        
    def onResponse(self, controller, response):
        if response['ret'] == 0:
            self.onFailed(controller)
        else:
            self.onSuccess(controller)
            
    def onInitUI(self, controller):
        if controller and hasattr(controller, 'entry'):
            sn_input['state'] = NORMAL
        else:
            sn_input['state'] = DISABLED

    def onFailed(self, controller):
        state_indicator_var.set(u'失败')
        state_label['background'] = '#DC143C'
        state_indicator['background'] = '#DC143C'
        
    def onSuccess(self, controller):
        state_indicator_var.set(u'成功')
        state_label['background'] = '#2E8B57'
        state_indicator['background'] = '#2E8B57'
        
    def onContinue(self, controller):
        success_button['state'] = NORMAL
        failed_button['state'] = NORMAL

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
    
def label_normal():
    state_label['background'] = '#00BFFF'
    state_indicator['background'] = '#00BFFF'

def label_success():
    state_label['background'] = '#00BFFF'
    state_indicator['background'] = '#00BFFF'

def label_failed():
    state_label['background'] = '#00BFFF'
    state_indicator['background'] = '#00BFFF'

def _start_run():
    print('Running')
    label_normal()
    if context.mark == 1:
        input_bundle.params['sn_number'] = sn_input.get()
    context.run()
    
def disable_buttons():
    success_button['state'] = DISABLED
    failed_button['state'] = DISABLED
    
def start_run():
    print('wait running')
    disable_buttons()
    root.after(300, _start_run)

def on_failed_button():
    disable_buttons()
    _retval = context.report_failure()
    if _retval == Env.RESULT_FAILED:
        context.clear()
    state_indicator_var.set(u'失败')
    state_label['background'] = '#DC143C'
    state_indicator['background'] = '#DC143C'
    start_run()
    
def on_success_button():
    disable_buttons()

    state_label['background'] = '#DC143C'
    state_indicator['background'] = '#DC143C'
    start_run()

if __name__ == '__main__':
    initialize()
    context.init_controller(controllers)
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
    success_button = Button(control_frame, text=u'成功', font=("Arial", 12), width=15, height=3, command=on_success_button)
    failed_button = Button(control_frame, text=u'失败', font=("Arial", 12), width=15, height=3, command=on_failed_button)
    success_button.pack(side=LEFT)
    start_run()
    failed_button.pack(side=RIGHT)
    failed_button['state'] = DISABLED
    sn_input = Entry(control_frame, width=50, font=Font(size=42))
    sn_input.pack()
    sn_input['state'] = DISABLED
    root.resizable(width=False, height=False)
    root.mainloop()
