from tkdev import *

Window = DevWindow()
TitleBar = DevTitleBar(Window, window=Window, title_label="Hello World")
Window.titlebar(TitleBar)
Window.mainloop()