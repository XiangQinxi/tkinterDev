import tkinter as tk
import tkinter.ttk as ttk
from ctypes import *

__version__ = "1.1.2"


class _PointAPI(Structure):  # 用于getpos()中API函数的调用
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


def getpos():
    # 调用API函数获取当前鼠标位置。返回值以(x,y)形式表示。
    po = _PointAPI()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)


def xpos(): return getpos()[0]


def ypos(): return getpos()[1]


# tkinter控件支持作为字典键。
# bound的键是dragger, 值是包含1个或多个绑定事件的列表, 值用于存储控件绑定的数据
# 列表的一项是对应tkwidget和其他信息的元组
bound = {}


def __add(wid, data):  # 添加绑定数据
    bound[wid] = bound.get(wid, []) + [data]


def __remove(wid, key):  # 用于从bound中移除绑定
    for i in range(len(bound[wid])):
        try:
            if bound[wid][i][0] == key:
                del bound[wid][i]
        except IndexError:
            pass


def __get(wid, key=''):  # 用于从bound中获取绑定数据
    if not key: return bound[wid][0]
    if key == 'devresize':
        for i in range(len(bound[wid])):
            for s in 'nwse':
                if s in bound[wid][i][0].lower():
                    return bound[wid][i]
    for i in range(len(bound[wid])):
        if bound[wid][i][0] == key:
            return bound[wid][i]


def move(widget, x=None, y=None, width=None, height=None):
    """移动控件或窗口widget, 参数皆可选。"""
    x = x if x is not None else widget.winfo_x()
    y = y if y is not None else widget.winfo_y()
    width = width if width is not None else widget.winfo_width()
    height = height if height is not None else widget.winfo_height()
    if isinstance(widget, tk.Wm):
        widget.geometry("%dx%d+%d+%d" % (width, height, x, y))
    else:
        widget.place(x=x, y=y, width=width, height=height)
    return x, y, width, height


def _mousedown(event):
    if event.widget not in bound: return
    lst = bound[event.widget]
    try:
        for data in lst:  # 开始拖动时, 在每一个控件记录位置和控件尺寸
            widget = data[1]
            widget.mousex, widget.mousey = getpos()
            widget.startx, widget.starty = widget.winfo_x(), widget.winfo_y()
            widget.start_w = widget.winfo_width()
            widget.start_h = widget.winfo_height()
    except tk.TclError:
        pass


def _drag(event):
    if event.widget not in bound: return
    lst = bound[event.widget]
    for data in lst:  # 多个绑定
        if data[0] != 'drag': return
        widget = data[1]
        dx = xpos() - widget.mousex  # 计算鼠标当前位置和开始拖动时位置的差距
        # 注: 鼠标位置不能用event.x和event.y
        # event.x,event.y与控件的位置、大小有关，不能真实地反映鼠标移动的距离差值
        dy = ypos() - widget.mousey
        move(widget, widget.startx + dx if data[2] else None,
             widget.starty + dy if data[3] else None)


def _resize(event):
    data = __get(event.widget, 'devresize')
    if data is None: return
    widget = data[1]
    dx = xpos() - widget.mousex  # 计算位置差
    dy = ypos() - widget.mousey

    type = data[0].lower()
    minw, minh = data[2:4]
    if 's' in type:
        try:
            move(widget, height=max(widget.start_h + dy, minh))
        except AttributeError:
            pass
    elif 'n' in type:
        move(widget, y=min(widget.starty + dy, widget.starty + widget.start_h - minh),
             height=max(widget.start_h - dy, minh))

    __remove(event.widget, data[0])  # 取消绑定, 为防止widget.update()中产生新的事件, 避免_resize()被tkinter反复调用
    widget.update()  # 刷新控件, 使以下左右缩放时, winfo_height()返回的是新的控件坐标, 而不是旧的
    __add(event.widget, data)  # 重新绑定

    if 'e' in type:
        move(widget, width=max(widget.start_w + dx, minw))
    elif 'w' in type:
        move(widget, x=min(widget.startx + dx, widget.startx + widget.start_w - minw),
             width=max(widget.start_w - dx, minw))


def draggable(tkwidget, x=True, y=True):
    """调用draggable(tkwidget) 使tkwidget可拖动。
tkwidget: 一个控件(Widget)或一个窗口(Wm)。
x 和 y: 只允许改变x坐标或y坐标。"""
    bind_drag(tkwidget, tkwidget, x, y)


def bind_drag(tkwidget, dragger, x=True, y=True):
    """绑定拖曳事件。
tkwidget: 被拖动的控件或窗口,
dragger: 接收鼠标事件的控件,
调用bind_drag后,当鼠标拖动dragger时, tkwidget会被带着拖动, 但dragger
作为接收鼠标事件的控件, 位置不会改变。
x 和 y: 同draggable()函数。"""
    dragger.bind("<Button-1>", _mousedown, add='+')
    dragger.bind("<B1-Motion>", _drag, add='+')
    __add(dragger, ('drag', tkwidget, x, y))  # 在bound字典中记录数据


def bind_resize(tkwidget, dragger, anchor, min_w=0, min_h=0, move_dragger=True):
    """绑定缩放事件。
anchor: 缩放"手柄"的方位, 取值为N,S,W,E,NW,NE,SW,SE,分别表示东、西、南、北。
min_w,min_h: 该方向tkwidget缩放的最小宽度(或高度)。
move_dragger: 缩放时是否移动dragger。
其他说明同bind_drag函数。"""
    dragger.bind("<Button-1>", _mousedown, add='+')
    dragger.bind("<B1-Motion>", _resize, add='+')
    data = (anchor, tkwidget, min_w, min_h, move_dragger)
    __add(dragger, data)


def test():
    btns = []  # 用btns列表存储创建的按钮

    def add_button(func, anchor):
        # func的作用是计算按钮新坐标
        b = ttk.Button(root)
        b._func = func
        bind_resize(btn, b, anchor)
        x, y = func()
        b.place(x=x, y=y, width=size, height=size)
        b.bind('<B1-Motion>', adjust_button, add='+')
        btns.append(b)

    def adjust_button(event=None):
        # 改变大小或拖动后,调整手柄位置
        for b in btns:
            x, y = b._func()
            b.place(x=x, y=y)

    root = tk.Tk()
    root.title("Test")
    root.geometry('500x350')
    btn = ttk.Button(root, text="Button")
    btn.bind('<B1-Motion>', adjust_button, add='+')
    x1 = 20
    y1 = 20
    x2 = 220
    y2 = 170
    size = 10
    btn.place(x=x1, y=y1, width=x2 - x1, height=y2 - y1)
    root.update()
    # 创建各个手柄, 这里是控件缩放的算法
    add_button(lambda: (btn.winfo_x() - size, btn.winfo_y() - size),
               'nw')
    add_button(lambda: (btn.winfo_x() + btn.winfo_width() // 2,
                        btn.winfo_y() - size), 'n')
    add_button(lambda: (btn.winfo_x() + btn.winfo_width(), btn.winfo_y() - size),
               'ne')
    add_button(lambda: (btn.winfo_x() + btn.winfo_width(),
                        btn.winfo_y() + btn.winfo_height() // 2), 'e')
    add_button(lambda: (btn.winfo_x() + btn.winfo_width(),
                        btn.winfo_y() + btn.winfo_height()), 'se')
    add_button(lambda: (btn.winfo_x() + btn.winfo_width() // 2,
                        btn.winfo_y() + btn.winfo_height()), 's')
    add_button(lambda: (btn.winfo_x() - size, btn.winfo_y() + btn.winfo_height()),
               'sw')
    add_button(lambda: (btn.winfo_x() - size,
                        btn.winfo_y() + btn.winfo_height() // 2), 'w')
    root.mainloop()


class DevResize(object):
    def __init__(self, widget: tk.Widget, size: int = 10):
        btns = []  # 用btns列表存储创建的按钮
        self.widget = widget
        self.master = widget.master

        def add_button(func, anchor, cursor):
            # func的作用是计算按钮新坐标
            b = ttk.Button(self.master, cursor=cursor)
            b._func = func
            bind_resize(self.widget, b, anchor)
            x, y = func()
            b.place(x=x, y=y, width=size, height=size)
            b.bind('<B1-Motion>', adjust_button, add='+')
            btns.append(b)

        def adjust_button(event=None):
            # 改变大小或拖动后,调整手柄位置
            for b in btns:
                try:
                    x, y = b._func()
                except tk.TclError:
                    for b in btns:
                        b.destroy()
                try:
                    b.place(x=x, y=y)
                except UnboundLocalError:
                    pass

        self.widget.bind('<B1-Motion>', adjust_button, add='+')
        self.master.update()
        # 创建各个手柄, 这里是控件缩放的算法
        add_button(lambda: (self.widget.winfo_x() - size, self.widget.winfo_y() - size,),
                   'nw',
                   "top_left_corner")
        add_button(lambda: (self.widget.winfo_x() + self.widget.winfo_width() // 2,
                            self.widget.winfo_y() - size), 'n',
                   "top_side")
        add_button(lambda: (self.widget.winfo_x() + self.widget.winfo_width(), self.widget.winfo_y() - size),
                   'ne',
                   "top_right_corner")
        add_button(lambda: (self.widget.winfo_x() + self.widget.winfo_width(),
                            self.widget.winfo_y() + self.widget.winfo_height() // 2), 'e',
                   "right_side")
        add_button(lambda: (self.widget.winfo_x() + self.widget.winfo_width(),
                            self.widget.winfo_y() + self.widget.winfo_height()), 'se',
                   "bottom_right_corner")
        add_button(lambda: (self.widget.winfo_x() + self.widget.winfo_width() // 2,
                            self.widget.winfo_y() + self.widget.winfo_height()), 's',
                   "bottom_side")
        add_button(lambda: (self.widget.winfo_x() - size, self.widget.winfo_y() + self.widget.winfo_height()),
                   'sw',
                   "bottom_left_corner")
        add_button(lambda: (self.widget.winfo_x() - size,
                            self.widget.winfo_y() + self.widget.winfo_height() // 2), 'w',
                   "left_side")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    button = tk.Button(root)
    button.place(x=10, y=10, width=480, height=480)
    DevResize(widget=button)
    root.mainloop()
