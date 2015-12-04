#coding=utf-8
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
from setting import Setting

class MainListener(Listener):
    def __init__(self, mainwin):
        Listener.__init__(self)
        self.win = mainwin

    def onResponse(self, controller, response):
        if response['ret'] == 0:
            self.onFailed(controller)
        else:
            self.onSuccess(controller)

    def onInitUI(self, controller):
        if controller and hasattr(controller, 'entry'):
            self.win.sn_input['state'] = NORMAL
        else:
            self.win.sn_input['state'] = DISABLED

        print '==>', controller.get_name()
        self.win.label_text(controller.get_name())

    def onFailed(self, controller):
        self.win.status_text(u'失败 Failed')

    def onSuccess(self, controller):
        self.win.status_text(u'成功 Pass')

    def onContinue(self, controller):
        self.win.success_button['state'] = NORMAL
        self.win.failed_button['state'] = NORMAL

    def onFinish(self, controller):
        # NOTICE: controller is None
        print('finish')
        self.win.status_text(u'完成 Pass')


class MainWindow():
    def __init__(self):
        self.root = Tk()
        self.input_bundle = Bundle()
        self.stamp_bundle = Bundle()
        self.controllers = []
        self.main_frame = None
        self.state_label = None
        self.state_label_var = None
        self.state_indicator = None
        self.state_indicator_var = None
        self.success_button = None
        self.failed_button = None
        self.sn_input = None
        self.title_list = []
        
        self.state_code = Setting.RESULT_OK
        self.mark = 0
        self.listener = MainListener(self)
        self.context = Context(self.input_bundle, self.stamp_bundle, self.listener)
        self.main()
        
    def main(self):
        self.initialize()
        self.context.init_controller(self.controllers)
        self.state_label_var = StringVar()
        self.state_indicator_var = StringVar()
        self.title = u'产线工具'
        self.label_frame_title = u'产线测试工具客户端'
        self.root.title(self.title)
        self.root.geometry('800x260')
        self.label_frame = LabelFrame(self.root, text=self.label_frame_title)
        self.label_frame.pack(fill="both", expand="yes")
        self.main_frame = Frame(self.label_frame)
        self.main_frame.pack()
        self.state_label_var.set(u'准备Smt测试')
        self.state_label = Label(self.main_frame, textvariable=self.state_label_var,
                                 font=("Arial", 12), width=40, height=7, bg="#00BFFF")
        self.state_label.pack(side=LEFT)
        self.state_indicator_var.set(u'未测试')
        self.state_indicator = Label(self.main_frame, textvariable=self.state_indicator_var,
                                     font=("Arial", 12), width=40, height=7, bg="#00BFFF")
        self.state_indicator.pack(side=LEFT)
        self.control_frame = LabelFrame(self.label_frame)
        self.control_frame.pack(side=BOTTOM, fill="both", expand="yes")
        self.success_button = Button(self.control_frame, text=u'成功', font=("Arial", 12),
                                     width=15, height=3, command=self.on_success_button)
        self.failed_button = Button(self.control_frame, text=u'失败', font=("Arial", 12),
                                    width=15, height=3, command=self.on_failed_button)
        self.success_button.pack(side=LEFT)
        self.failed_button.pack(side=RIGHT)
        self.failed_button['state'] = DISABLED
        self.sn_input = Entry(self.control_frame, width=50, font=Font(size=42))
        self.sn_input.pack()
        self.disable_buttons()
        self.sn_input.bind("<KeyRelease-Return>", self.on_sn_input)
        self.root.resizable(width=False, height=False)
        if Setting.DEBUG:
            self.label_text('Debug!!!')
        
    def on_sn_input(self, event):
        self.input_bundle.params[Setting.ID] = self.sn_input.get()
        print('sn %s' % self.sn_input.get())
        self.start_run()
        
    def loop(self):
        print('mainloop')
        self.sn_input.focus()
        self.root.mainloop()

    def initialize(self):
        #_rom_controller = RomController(0, stamp_bundle, listener)
        #controllers.append(_rom_controller)
        #title_list.append(u'rom烧写')
        _sn_controller = SnController(1, self.stamp_bundle, self.listener)
        self.controllers.append(_sn_controller)
        self.title_list.append(u'Sn烧录')
        _adb_controller = AdbController(2, self.stamp_bundle, self.listener)
        self.controllers.append(_adb_controller)
        self.title_list.append(u'Smt测试')
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

    def label_normal(self, text=None):
        self.state_label['background'] = '#00BFFF'
        self.state_indicator['background'] = '#00BFFF'
        if text is not None: self.label_failed(str(text))

    def label_success(self, text=None):
        self.state_label['background'] = '#00BFFF'
        self.state_indicator['background'] = '#00BFFF'
        if text is not None: self.label_failed(str(text))

    def label_failed(self, text=None):
        self.state_label['background'] = '#00BFFF'
        self.state_indicator['background'] = '#00BFFF'
        if text is not None: self.label_failed(str(text))

    def label_text(self, text):
        self.state_label_var.set(text)
        self.root.update()

    def status_text(self, text):
        self.state_indicator_var.set(text)
        if text.endswith('Pass'):
            self.state_label['background'] = '#2E8B57'
            self.state_indicator['background'] = '#2E8B57'
        else:
            self.state_label['background'] = '#DC143C'
            self.state_indicator['background'] = '#DC143C'

    def _start_run(self):
        print('Running')
        self.label_normal()
        self.context.run()

    def disable_buttons(self):
        self.success_button['state'] = DISABLED
        self.failed_button['state'] = DISABLED

    def start_run(self):
        print('wait running')
        self.disable_buttons()
        self.root.after(300, self._start_run)

    def on_failed_button(self):
        self.disable_buttons()
        self._retval = self.context.report_failure()
        if self._retval == Setting.RESULT_FAILED:
            self.context.clear()
        self.state_indicator_var.set(u'失败')
        self.state_label['background'] = '#DC143C'
        self.state_indicator['background'] = '#DC143C'
        self.start_run()

    def on_success_button(self):
        self.disable_buttons()

        self.state_label['background'] = '#DC143C'
        self.state_indicator['background'] = '#DC143C'
        self.start_run()

if __name__ == '__main__':
    win = MainWindow()
    win.loop()
