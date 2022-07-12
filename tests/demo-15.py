from tkinter import *

Window = Tk()
Window.overrideredirect(True)
Window.geometry(f"{Window.winfo_screenwidth()}x{Window.winfo_screenheight()}+0+0")

Label = Label(Window, text="向曼婷就是个大傻逼", font=("等线 Light", 60))
Num = 0


def swich(evt):
    global Num
    if Num == 0:
        Label.configure(text="专心学习，把作业写完")
        Num = 1
    else:
        Label.configure(text="向曼婷你有本事就来打我")
        Num = 0


Window.bind("<Return>", swich)
Window.bind("<Triple-Return>", lambda evt:Window.destroy())
#Label.bind("<Double-Button-1>", lambda evt: Label.configure(text="下面有个按钮，点击就能关闭"))
Label.pack(fill=BOTH, expand=YES)
Button = Button(Window, text='关闭', foreground="#f6f6f6", relief=FLAT, borderwidth=0, command=Window.destroy)
Button.pack(fill=X, side=BOTTOM)
Window.attributes("-topmost", True)
Window.mainloop()
