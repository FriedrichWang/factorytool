#encoding=utf8
from Tkinter import *
from tkFont import *
from factcore.setting import Setting
from factcore.ui import ButtonEx
from factcore.works.workflow import BaseWork, Context
from factcore.logger import Log

class MainWindow():
    def __init__(self):
        self.ctx = Context(self)
        self.title = u'产线工具'
        self.label_frame_title = u'产线测试工具客户端'
    
    def main(self):
        self.root = Tk()
        self.initUI()
        self.initWorkFlow()
        self.loop()

    def initWorkFlow(self):
        self.ctx.initWorkClss(Setting.getStepWorks())

    def cleanMainFrame(self):
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()
            self.main_frame = None
        self.main_frame = Frame(self.main_frame_wrapper)
        self.main_frame.pack()

    def initUI(self):
        self.root.title(self.title)

        labelframe = LabelFrame(self.root, text=self.label_frame_title)
        labelframe.pack(fill="both", expand="yes")

        self.main_frame_wrapper = Frame(labelframe)
        self.main_frame_wrapper.pack()

        buttons_frame = LabelFrame(self.root)
        buttons_frame.pack(fill="both", expand="yes")
        self.start_button = ButtonEx(buttons_frame, text=u'开始',
                                     font=Font(size=12), width=30, height=3,
                                     command=lambda: self.root.after(0, self._start))
        self.start_button.pack()

        self.root.update()
        self.root.minsize(self.root.winfo_width()+100, self.root.winfo_height()+40)
        
    def getStatusFrame(self): return self.status_frame
    def getControlFrame(self): return self.control_frame
    def getMainFrame(self): return self.main_frame
        
    def _start(self):
        self.start_button.disable()
        self.ctx.start()
        
    def loop(self):
        if Setting.AUTO_START:
            self._start()
        self.root.mainloop()

    def resetStartButton(self):
        self.start_button['text'] = u'开始'
        self.start_button.enable()
        
if __name__ == '__main__':
    win = MainWindow()
    win.main()