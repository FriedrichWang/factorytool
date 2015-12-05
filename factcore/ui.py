#encoding=utf8
from Tkinter import *
from tkFont import *

class ButtonEx(Button):
    def enable(self):
        self['state'] = NORMAL
    def disable(self):
        self['state'] = DISABLED

class BaseWorkUI(object):
    def __init__(self):
        self.font = Font("Arial", 12)

    def onInitUI(self, frame):
        workframe = self.createFrame(frame, side=BOTTOM)

        self.status_frame = self.createFrame(workframe)
        self.control_frame = self.createFrame(workframe)

        self._initStatus(self.status_frame)
        self._initControl(self.control_frame)

    def _initStatus(self, frame):
        self.createLabel(frame)
        self.status_label = self.createLabel(frame, side=LEFT)
        self.status_label.var.set(u'准备SMT测试')
        self.info_label = self.createLabel(frame, side=LEFT)
        self.info_label.var.set(u'未测试')

    def _initControl(self, frame):
        self.createButton(frame, u'成功 ')
        self.createButton(frame, u'失败')
        
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
        btn = Button(parent, text=label)
        btn.pack(side=side)
        return btn
    
    def createEntry(self, parent, label='', side=LEFT):
        entry = Entry(parent)
        entry.pack(side=side)
