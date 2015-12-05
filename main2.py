#encoding=utf8
from Tkinter import *
from tkFont import *
from factcore.setting import Setting
from factcore.ui import ButtonEx

class Context(object):
    def __init__(self):
        self.works = []

    def appendWork(self, work):
        self.works.append(work)
        
    def OnSuccess(self):
        pass
    def OnFailed(self):
        pass
    def OnContinue(self):
        pass
    def OnFinished(self):
        pass
        # TODO: reset
        
    def getListener(self): return self

class MainWindow():
    def __init__(self):
        self.workflows = []
        self.ctx = Context()
        self.title = u'产线工具'
        self.label_frame_title = u'产线测试工具客户端'
    
    def main(self):
        self.root = Tk()
        self.initWorkFlow()
        self.initUI()
        self.loop()

    def initWorkFlow(self):
        self.workflows.extend(Setting.getStepWorks())
        
    def initUI(self):
        self.root.title(self.title)

        labelframe = LabelFrame(self.root, text=self.label_frame_title)
        labelframe.pack(fill="both", expand="yes")

        self.main_frame = Frame(labelframe)
        self.main_frame.pack()
        
        for workcls in self.workflows:
            work = workcls(self.ctx)
            self.ctx.appendWork(work)
            work.onInitUI(self.main_frame)
            
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
        
    def loop(self):
        if Setting.AUTO_START:
            self.root.after(300, self._start)
        self.root.mainloop()
        
if __name__ == '__main__':
    win = MainWindow()
    win.main()
