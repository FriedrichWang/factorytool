#encoding=utf8
from Tkinter import *
from tkFont import *

class ButtonEx(Button):
    def enable(self):
        self['state'] = NORMAL
    def disable(self):
        self['state'] = DISABLED

class BaseWorkUI(object):
    def __init__(self, work, ctx):
        self.font = Font(size=12)
        self.work = work
        self.ctx = ctx

    def onInitUI(self, frame):
        workframe = self.createFrame(frame, side=TOP)

        self.status_frame = self.createFrame(workframe)
        self.control_frame = self.createFrame(workframe)

        self._initStatus(self.status_frame)
        self._initControl(self.control_frame)
        self.pass_btn.disable()
        self.fail_btn.disable()
        def _success(event):
            self.work.result = self.work.SUCCESS
            self.ctx.incStep(self.work.result, True)
            self.ctx.start()
        def _failed(event):
            self.work.result = self.work.FAILED
            self.ctx.incStep(self.work.result, True)
            self.ctx.start()
        self.pass_btn.bind("<Button-1>", _success)
        self.fail_btn.bind("<Button-1>", _failed)
        
    def onBeginUI(self):
        self.status_text(u'正在测试...')
    
    def onEndUI(self):
        pass
        
    def onSuccessUI(self):
        self.status_text(u'成功Pass')

    def onFailedUI(self):
        self.status_text(u'失败Failed')
    
    def onPauseUI(self):
        self.pass_btn.enable()
        self.fail_btn.enable()
    
    def onContinueUI(self):
        self.pass_btn.disable()
        self.fail_btn.disable()

    def _initStatus(self, frame):
        self.status_label = self.createLabel(frame, side=LEFT)
        self.status_label.var.set(u'准备测试')

    def _initControl(self, frame):
        self.pass_btn = self.createButton(frame, u'成功 ')
        self.fail_btn = self.createButton(frame, u'失败')
        
    def createLabelFrame(self, parent, text, side=LEFT):
        frame = LabelFrame(parent, text=text)
        frame.pack(side=side, fill="both", expand="yes")
        return frame

    def createFrame(self, parent, side=LEFT):
        frame = Frame(parent)
        frame.pack(side=side, fill="both", expand="yes")
        return frame

    def createLabel(self, parent, width=15, height=3, bg="#00BFFF", side=LEFT):
        txtvar = StringVar()
        label = Label(parent, textvariable=txtvar, #font=self.font,
                      width=width, height=height, bg=bg)
        label.var = txtvar
        label.pack(side=side)
        return label
    
    def createButton(self, parent, label='', side=LEFT):
        btn = ButtonEx(parent, text=label)
        btn.pack(side=side)
        return btn
    
    def createEntry(self, parent, label='', side=LEFT):
        entry = Entry(parent)
        entry.pack(side=side)

    def status_normal(self, text=None):
        self.status_text(text)
        self.status_label['background'] = '#00BFFF'

    def status_success(self, text=None):
        self.status_text(text)
        self.status_label['background'] = '#2E8B57'

    def status_failed(self, text=None):
        self.status_text(text)
        self.status_label['background'] = '#DC143C'

    def status_text(self, text):
        if text is None: return
        self.status_label.var.set(text)
        if text.endswith('Pass'):
            self.status_success()
        elif text.endswith('Failed'):
            self.status_failed()
        else:
            self.status_normal()
        self.ctx.getRoot().update()
