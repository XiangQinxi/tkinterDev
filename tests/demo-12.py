from src.tkdev import *


Window = DevWindow()
Window.geometry("500x500")
TitleBar = DevTitleBar(Window, window=Window)
Window.titlebar(TitleBar)
StatusBar = DevStatusBar(Window)
Window.statusbar(StatusBar)
Window.centre()
Window.mainloop()