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
        self.label_frame_title = u'产线测试工具客户端 - %s' % Setting.CURRENT_STEP
    
    def main(self):
        self.root = Tk()
        self.initUI()
        self.initWorkFlow()
        self.loop()

    def initWorkFlow(self):
        self.ctx.initWorkClss(Setting.getStepWorks())
        self.ctx.reset(force=True)

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
        self.main_frame_wrapper.pack(side=LEFT)
        self.infoarea = Text(labelframe)
        self.infoarea.pack(side=LEFT)

        buttons_frame = LabelFrame(self.root)
        buttons_frame.pack(fill="both", expand="yes")
        self.start_button = ButtonEx(buttons_frame, text=u'开始',
                                     font=Font(size=Setting.DEFAULT_FONT_SIZE), width=30, height=3,
                                     command=lambda: self.root.after(0, self._start))
        self.start_button.pack(fill="both", expand="yes")

        self.root.update()
        self.root.minsize(self.root.winfo_width()+100, self.root.winfo_height()+40)
        
    def getStatusFrame(self): return self.status_frame
    def getControlFrame(self): return self.control_frame
    def getMainFrame(self): return self.main_frame
        
    def _start(self):
        if self.start_button['text'] == u'重新开始':
            self.ctx.reset(force=True)
            self.start_button['text'] = u'开始'
        self.start_button.disable()
        self.ctx.start()

    def loop(self):
        if Setting.AUTO_START:
            self._start()
        self.root.mainloop()

    def showStartButton(self):
        self.start_button['text'] = u'开始'
        self.start_button.enable()
        self.start_button.focus()
        
    def showRestartButton(self):
        self.start_button['text'] = u'重新开始'
        self.start_button.enable()
        self.start_button.focus()
        
    def showInfo(self, msg):
        if not msg: return
        if type(msg) is unicode:
            msg = msg.encode('utf8')
        msg = str(msg)
        self.infoarea.insert(END, msg)
        self.infoarea.insert(END, '\n')
        
    def cleanInfo(self):
        self.infoarea.delete(1.0, END)

if __name__ == '__main__':
    win = MainWindow()
    win.main()
