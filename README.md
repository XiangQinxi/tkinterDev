# tkinterDev

tkinter高级工具包，实现了许多高级功能，我会持续更新的。😁😁😁
____
## 版本信息
请使用最新的稳定版，虽然最新版可以用，但不排除会出现一些不可免得错误，请按照下方标准进行安装。🐋🐳🐋🐳
- 不稳定版本 1.0.0 - 1.5.0
- 最新稳定版本 1.8.0
- 最低稳定版本 1.6.0

### 1.6.0 稳定版发布。
### 1.7.0 功能补充，添加DevAppBar模块。
### 1.8.0 DevDrag优化，预添加组件DevAccumulatorButton、DevDocs、DevResize（在以后可能会删除的组件）。
____

## devdemo
在终端输入以下代码，即可打开实例，看各个组件的功能🤣🤣
```commandline
python -m tkdev
```
____

## DevDrag 🤖
可以使组件拖动另一个组件进行移动，这算是里面做得最好的了。第一个填拖动那个组件使另一个组件移动，第二个填被拖动的组件。第三个填是否是窗口，默认为False。

```python

from src import tkdev as dev
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x500")
    drag_widget = tk.Label(root, background="black", foreground="white", text="Hello DevDrag")
    drag_widget.pack(fill=tk.BOTH, expand=tk.YES)
    dev.DevDrag(drag_widget, drag_widget)
    root.mainloop()
```
运行以上代码，即可拖动窗口中的Label组件，因为是用18行代码写出来，并且无依赖，运行速度很快。但是还未实现调整组件大小的功能，有点苦恼。

### 运行问题❓
1.为什么我用这个拖动窗口会报错？
答：那是因为组件判断不了你是窗口还是组件，窗口用geometry，组件用place，两种方法不同。所以如果要用来拖动窗口的话，请加上iswindow参数，为True，即可正常运行。

```python

from src import tkdev as dev

dev.DevDrag(widget, window, iswindow=true)
```
____

## DevSubWindow🤖
在Qt里可以使用MDI这个组件制作子窗口，而tkinter中未实现这个功能，而我又想制作tkinter的设计器，需要子窗口功能，于是我就自己做了一个，里面都是有tkinter组件做的，并非ttk。不是我不想要漂亮的界面，而是我发现使用ttk，按钮的边框太长了，显得不美观，于是就用tk组件了。

```python

from src import tkdev as dev
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x300")
    subwindow = dev.DevSubWindow(root, title="DevSubWindow")
    subwindow.place(x=5, y=5, width=290, height=290)

    root.mainloop()
```
### 运行问题❓
1.暂无，等待反馈
____
## DevTitleBar和DevWindow
这两个组件需要一起搭配着进行使用最好，DevWindow的wm_titlebar可以设置标题栏，而DevTitleBar做的标题栏与DevWindow正好很搭配。

```python

from src import tkdev as dev
import tkinter as tk

if __name__ == '__main__':
    root = dev.DevWindow()
    root.geometry("300x300")
    titlebar = dev.DevTitleBar(root, iswindow=True, window=root, title_label="Hello")
    root.titlebar(titlebar)
    root.mainloop()
```
可是，当你运行以上的代码之后，你会发现，这个DevTitleBar和DevSubWindow的标题栏一模一样，其实DevSubWindow就是使用DevTitleBar做的。close是指定是否显示关闭按钮，max是指定是否显示放大按钮，min是指定是否显示缩小按钮，title是指定是否显示标题栏。如果后面想要加入标题按钮、标题，可以使用add_close() add_max() add_min() add_title()进行添加
### 运行问题❓
1.为什么我用DevTitleBar时标题没有出现？答：这个组件的参数title并不是直接写入标题参数，而是需要用title_label参数设置标题栏的标题，因为title参数是决定是否显示标题栏的参数，写True则显示标题栏，反之隐藏。
____
