# tkinterDev

`tkinter`高级工具包，实现了许多高级功能，我会持续更新的。😁😁😁
____
## 版本信息
请使用最新的稳定版，虽然最新版可以用，但不排除会出现一些不可免得错误，大版本更新有时会出现BUG，但是小版本可以考虑，因为小版本是对大版本的优化和改正，请按照下方标准进行安装。🐋🐳🐋🐳
- 不稳定版本 1.0.0 - 1.5.0 1.8.3 - 1.8.4
- 最新稳定版本 1.9.1
- 最低稳定版本 1.6.0
 
1.6.0 稳定版发布。

1.7.0 功能补充，添加`DevAppBar`模块。

1.8.0 `DevDrag`优化，预添加组件`DevAccumulatorButton`、`DevDocs`、`DevResize`（在以后可能会删除的组件）。

1.8.1 `DevWindow`优化，加入标题栏后，可显示在任务栏内。

1.8.2 `DevTitleBar`修正标题按钮放大按钮，删去最小化按钮的函数，因为最小化后就找不到窗口了，任务栏中的窗口也不见了，所以等以后尝试改正。

1.8.3 `DevTitleBar`优化。

1.8.4 `DevToplevel`修正。

1.8.5 `DevTitleBar`修正，真的最后一次修正了！

1.8.6 `DevWindow`优化，可以选择是否将窗口显示在任务栏。

1.8.7 `DevWindow`优化，可以使用`centre()`将窗口居中。

1.8.8 `DevTitleBar`优化，双击窗口放大。

1.9.0 正式稳定更新，组件参数各种优化，添加`DevSideBar`组件。

1.9.1 文档改正。

1.9.2 `DevTitleBar`修正最大化按钮和最小化按钮的的事件特征。
____

## devdemo
在终端输入以下代码，即可打开实例，看各个组件的功能🤣🤣
```commandline
python -m tkdev
```
____

## DevDrag 🤖
可以使组件拖动另一个组件进行移动，这算是里面做得最好的了。第一个填拖动那个组件使另一个组件移动，第二个填被拖动的组件。第三个填是否是窗口，默认为`False`。

```python

import tkdev as dev
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x500")
    drag_widget = tk.Label(root, background="black", foreground="white", text="Hello DevDrag")
    drag_widget.pack(fill=tk.BOTH, expand=tk.YES)
    dev.DevDrag(drag_widget, drag_widget)
    root.mainloop()
```
运行以上代码，即可拖动窗口中的`Label`组件，因为是用18行代码写出来，并且无依赖，运行速度很快。但是还未实现调整组件大小的功能，有点苦恼。

### 运行问题❓
1.为什么我用这个拖动窗口会报错？
答：那是因为组件判断不了你是窗口还是组件，窗口用`geometry`，组件用`place`，两种方法不同。所以如果要用来拖动窗口的话，请加上`iswindow`参数，为`True`，即可正常运行。

```python

import tkdev as dev

dev.DevDrag(widget, window, iswindow=true)
```
____

## DevSubWindow🤖
在`Qt`里可以使用`MDI`这个组件制作子窗口，而tkinter中未实现这个功能，而我又想制作`tkinter`的设计器，需要子窗口功能，于是我就自己做了一个，里面都是有`tkinter`组件做的，并非`ttk`。不是我不想要漂亮的界面，而是我发现使用`ttk`，按钮的边框太长了，显得不美观，于是就用`tk`组件了。

```python

import tkdev as dev
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
这两个组件需要一起搭配着进行使用最好，`DevWindow`的`wm_titlebar`可以设置标题栏，而`DevTitleBar`做的标题栏与`DevWindow`正好很搭配。

```python

import tkdev as dev
import tkinter as tk

if __name__ == '__main__':
    root = dev.DevWindow()
    root.geometry("300x300")
    titlebar = dev.DevTitleBar(root, iswindow=True, window=root, title_label="Hello")
    root.titlebar(titlebar)
    root.mainloop()
```
可是，当你运行以上的代码之后，你会发现，这个`DevTitleBar`和`DevSubWindow`的标题栏一模一样，其实`DevSubWindow`就是使用`DevTitleBar`做的。`close`是指定是否显示关闭按钮，`max`是指定是否显示放大按钮，`min`是指定是否显示缩小按钮，`title`是指定是否显示标题栏。如果后面想要加入标题按钮、标题，可以使用`add_close()` `add_max()` `add_min()` `add_title()`进行添加
### 运行问题❓
1.为什么我用`DevTitleBa`r时标题没有出现？答：这个组件的参数`title`并不是直接写入标题参数，而是需要用`title_label`参数设置标题栏的标题，因为`title`参数是决定是否显示标题栏的参数，写True则显示标题栏，反之隐藏。
____

## DevStatusBar