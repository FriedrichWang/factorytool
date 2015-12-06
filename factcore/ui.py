#encoding=utf8
from Tkinter import *
from tkFont import *
from sys import platform
from factcore.setting import Setting

class ButtonEx(Button):
    def enable(self):
        self['state'] = NORMAL
    def disable(self):
        self['state'] = DISABLED

class BaseWorkUI(object):
    def __init__(self, work, ctx):
        self.font = Font(size=Setting.DEFAULT_FONT_SIZE)
        self.work = work
        self.ctx = ctx
        self._pause_text = u'正在测试...'
        
    def setPauseText(self, text):
        self._pause_text = text

    def onInitUI(self, frame):
        workframe = self.createFrame(frame, side=TOP)

        self.status_frame = self.createFrame(workframe)
        self.control_frame = self.createFrame(workframe, expand=None)

        self._initStatus(self.status_frame)

        def _onentry(event):
            self.ctx.incStep(self.work, True)
            self.ctx.start()
        if self.work.ui_hasentry:
            self.entry = self.createEntry(self.control_frame, side=LEFT)
            self.entry.bind('<KeyRelease-Return>', _onentry)

        self._initControl(self.control_frame)
        def _onsuccess(event):
            self.work.result = self.work.SUCCESS
            self.ctx.incStep(self.work, True)
            self.ctx.start()
        def _onfailed(event):
            self.work.result = self.work.FAILED
            self.ctx.incStep(self.work, True)
            self.ctx.start()
        self.connectButton(self.pass_btn, _onsuccess)
        self.connectButton(self.fail_btn, _onfailed)
        self.pass_btn.disable()
        self.fail_btn.disable()
 
    def onBeginUI(self):
        if self.work.ui_hasentry:
            self.entry.focus()
        self.status_text(self._pause_text)
    
    def onEndUI(self):
        pass
        
    def onSuccessUI(self):
        self.status_text(u'成功Pass')

    def onFailedUI(self):
        self.status_text(u'失败Failed')
    
    def onPauseUI(self):
        if not self.work.ui_hasentry:
            self.pass_btn.enable()
            self.fail_btn.enable()
    
    def onContinueUI(self, pass_or_failed=None):
        self.pass_btn.disable()
        self.fail_btn.disable()

    def _initStatus(self, frame):
        frame0 = self.createFrame(frame)
        name_label = self.createLabel(frame0)
        name_label.var.set(u'%s:' % self.work.getName())
         
        self.status_label = self.createLabel(frame0)
        self.status_label.var.set(u'准备测试')

    def _initControl(self, frame):
        self.pass_btn = self.createButton(frame, u'成功 ', side=LEFT)
        self.fail_btn = self.createButton(frame, u'失败', side=LEFT)
        
    def createLabelFrame(self, parent, text, fill="both", expand="yes", side=LEFT):
        frame = LabelFrame(parent, text=text)
        frame.pack(side=side, fill=fill, expand=expand)
        return frame

    def createFrame(self, parent, bg=None, fill="both", expand="yes", side=LEFT):
        frame = Frame(parent, bg=bg)
        frame.pack(side=side, fill=fill, expand=expand)
        return frame

    def createLabel(self, parent, width=15, height=3, bg="#00BFFF", side=LEFT):
        txtvar = StringVar()
        label = Label(parent, textvariable=txtvar, font=self.font,
                      width=width, height=height, bg=bg)
        label.var = txtvar
        label.pack(side=side)
        return label
    
    def createButton(self, parent, label='', side=LEFT):
        btn = ButtonEx(parent, text=label, font=self.font)
        btn.pack(side=side)
        return btn
    
    def createEntry(self, parent, side=LEFT):
        entry = Entry(parent, font=self.font)
        entry.pack(side=side)
        return entry

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

    def connectButton(self, btn, func, data=None):
        if platform == 'win32':
            # on windows platform have bugs on bind method 
            # (variable do not change before event, so get variable value is incorrect)
            btn.config(command=lambda : func(data))
        else:
            btn.bind("<ButtonRelease-1>", lambda event: func(data))
