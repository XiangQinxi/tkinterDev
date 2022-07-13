import tktooltip
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.tix as tix
from tkdev.devresize import DevResize
from ctypes import windll
from os import environ

windll.user32.SetProcessDPIAware()

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080


def add_taskbar(window):
    if 'PROGRAMFILES(X86)' in environ:
        hwnd = windll.user32.GetParent(window.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
    else:
        hwnd = windll.user32.GetParent(window.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
    window.wm_withdraw()
    window.after(10, lambda: window.wm_deiconify())


def window_centre(window: tk.Tk):
    x = window.winfo_screenwidth() / 2 - window.winfo_width() / 2
    y = window.winfo_screenheight() / 2 - window.winfo_height() / 2
    window.geometry(f"{window.winfo_width()}x{window.winfo_height()}+{round(x)}+{round(y)}")


def resize_widget(widget: tk.Widget):
    try:
        widget.after(10, lambda: DevResize(widget))
    except tk.TclError:
        pass


class DevAccumulatorButton(tk.Button):
    def __init__(self):
        super(DevAccumulatorButton, self).__init__()
        pass


class DevAppBar(tk.Frame):
    def __init__(self, master: tk.Widget = None, title: str = "", background="#ffffff", foreground="#000000"):
        super(DevAppBar, self).__init__(master=master, relief=tk.FLAT, background=background)
        self.title = tk.Label(self, text=title, justify=tk.LEFT, background=background, foreground=foreground)
        self.title.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=5)

    def show(self):
        self.pack(fill=tk.X, ipadx=10, ipady=10)


class DevButton(tk.Button):
    def __init__(self, master, text: str = "", borderwidth: int = 0, image=None, font=("等线 Light", 10, "bold"),
                 command=None,
                 default_bg="#ffffff", default_fg="#000000",
                 active_bg="#177aff", active_fg="#d6eaff",
                 click_bg="#175bff", click_fg="#d6deff"):
        super(DevButton, self).__init__(master=master, relief=tk.FLAT, text=text, font=float, command=command,
                                        borderwidth=borderwidth, image=image,
                                        background=default_bg, foreground=default_fg)
        self.default_bg = default_bg
        self.default_fg = default_fg
        self.active_bg = active_bg
        self.active_fg = active_fg
        self.click_bg = click_bg
        self.click_fg = click_fg
        self.bind("<Leave>", self.nofocus)
        self.bind("<Enter>", self.focus)
        self.bind("<Button-1>", self.click)

    def nofocus(self, event=None):
        self.configure(background=self.default_bg, foreground=self.default_fg)

    def focus(self, event=None):
        self.configure(background=self.active_bg, foreground=self.active_fg)

    def click(self, event=None):
        self.configure(activebackground=self.click_bg, activeforeground=self.click_fg)


class DevDrag(object):
    def __init__(self, widget: tk.Widget, dragwidget: tk.Widget, iswindow: bool = False, x: bool = True, y: bool = True,
                 click_func=None, noclick_func=None, move_func=None):
        """
        这个组件能够拖动组件移动，实现更高级的功能 \n widget设为拖动命令的组件，你拖动这个组件，拖动的组件会移动 \n dragwidget设为被拖动的组件 \n
        iswindow是声明你要拖动的组件是窗口还是组件，是窗口填True，是组件填False

        :param widget:
        :param dragwidget:
        :param iswindow:
        """
        self.widget = widget
        self.dragwidget = dragwidget
        self.iswindow = iswindow
        self.movex = tk.IntVar(self.widget, value=0)
        self.movey = tk.IntVar(self.widget, value=0)
        self.moved = tk.BooleanVar(self.widget, value=False)
        if click_func is None:
            self.widget.bind("<Button-1>", self.click)
        else:
            self.widget.bind("<Button-1>", click_func)
        if noclick_func is None:
            self.widget.bind("<ButtonRelease-1>", self.noclick)
        else:
            self.widget.bind("<ButtonRelease-1>", noclick_func)
        if move_func is None:
            self.widget.bind("<B1-Motion>", self.move)
        else:
            self.widget.bind("<B1-Motion>", move_func)
        self.x = x
        self.y = y

    def move(self, event=None):
        if not self.moved.get():
            return

        if self.x:
            newx = self.dragwidget.winfo_x() + (event.x - self.movex.get())
        else:
            newx = self.dragwidget.winfo_x()

        if self.y:
            newy = self.dragwidget.winfo_y() + (event.y - self.movey.get())
        else:
            newy = self.dragwidget.winfo_y()
        geometry = f"{self.dragwidget.winfo_width()}x{self.dragwidget.winfo_height()}+{newx}+{newy}"
        if self.iswindow:
            self.dragwidget.geometry(geometry)
        else:
            self.dragwidget.place(x=newx, y=newy, width=self.dragwidget.winfo_width(),
                                  height=self.dragwidget.winfo_height())
        self.widget.update()

    def click(self, event=None):
        self.movex.set(event.x)
        self.movey.set(event.y)
        self.moved.set(True)

    def noclick(self, event=None):
        self.moved.set(False)


class DevDocs(tk.PanedWindow):
    def __init__(self, master: tk.Widget):
        super(DevDocs, self).__init__(master=master, orient=tk.HORIZONTAL, height=3)
        self.docsvar = tk.StringVar()
        self.docslist_area = tk.Frame(self)
        self.docslist = tk.Listbox(self.docslist_area, listvariable=self.docsvar)
        self.docslist.bind("<<ListboxSelect>>", self.check)
        self.docslist.pack(fill=tk.BOTH, expand=tk.YES)
        self.docscheck = {}
        self.docstext_area = tk.Frame(self)
        self.docstext = tk.Text(self.docstext_area)
        self.docstext.pack(fill=tk.BOTH, expand=tk.YES)

        self.add(self.docslist_area)
        self.add(self.docstext_area)

    def check(self, event=None):
        self.docstext.delete("0.0", tk.END)
        list = self.docslist.curselection()
        self.docstext.insert("0.0", self.docscheck[list])

    def add_docs(self, list_name: str = "", docs_text: str = ""):
        self.docslist.insert(tk.END, list_name)
        self.docscheck[list_name] = docs_text


class DevExtend(tk.Frame):
    def __init__(self, master: tk.Widget, label: tk.Widget = tk.Label, text: str = "", widget: tk.Widget = tk.Message):
        super(DevExtend, self).__init__(master=master)
        self.label = label
        self.text = text
        self.widget = widget

        self.label.pack(fill=tk.X, side=tk.TOP)
        self.extend_area = tk.Frame()
        self.extend_area.pack(fill=tk.BOTH, expand=tk.YES)


class DevImage(tk.Label):
    def __init__(self, master: tk.Widget, image: tk.PhotoImage = None, ):
        super(DevImage, self).__init__(master=master, image=image)


class DevMenu(tk.Menubutton):
    def __init__(self, master=None, menu: tk.Menu = None, text: str = "", bg="#fafafa", fg="#000000",
                 active_bg="#3c7bfc", active_fg="#ffffff"):
        super(DevMenu, self).__init__(master=master, menu=menu, text=text, relief=tk.FLAT, background=bg, foreground=fg,
                                      activebackground=active_bg, activeforeground=active_fg)


class DevMenuBar(tk.Frame):
    def __init__(self, master: tk.Widget, bg="#fafafa"):
        super(DevMenuBar, self).__init__(master=master, background=bg)

    def add_menu(self, menu: DevMenu, side=tk.LEFT):
        menu.pack(side=side)

    def show(self):
        self.pack(fill=tk.X, side=tk.TOP)


class DevObject(object):
    def __init__(self):
        self.obj = {}

    def add_widget(self, widget: tk.Widget, id: str):
        self.obj[id] = widget

    def set_widget(self, id: str, widget: tk.Widget):
        self.obj[id] = widget

    def get_widget(self, id: str) -> tk.Widget:
        return self.obj[id]


class DevPopupWindow(tk.Toplevel):
    def __init__(self, master, widget: tk.Widget):
        """
        这个组件有些不稳定，还在研发当中，请谨慎使用

        :param master:
        :param wiget:
        """
        super(DevPopupWindow, self).__init__(master=master)
        self.overrideredirect(True)
        self.withdraw()
        widget.bind("<Button-1>", lambda event: self.popup(widget.winfo_x() + widget.winfo_width(),
                                                           widget.winfo_y() + widget.winfo_height()))
        self.bind("<Button-3>", lambda event: self.withdraw())

    def popup(self, x=0, y=0):
        self.deiconify()
        self.geometry(f"+{x}+{y}")


class DevBorder(object):
    def __init__(self, widget: tk.Widget = None, iswindow: bool = True, border_color="#e1e1e1"):
        self.widget = widget
        self.iswindow = iswindow
        self.top = tk.Frame(widget, height=0, cursor="sb_v_double_arrow", background=border_color)
        self.top.pack(side=tk.TOP, ipady=1, fill=tk.X)
        self.bottom = tk.Frame(widget, height=0, cursor="sb_v_double_arrow", background=border_color)
        self.bottom.pack(side=tk.BOTTOM, ipady=1, fill=tk.X)
        self.left = tk.Frame(widget, height=0, cursor="sb_h_double_arrow", background=border_color)
        self.left.pack(side=tk.LEFT, ipadx=1, fill=tk.Y)
        self.right = tk.Frame(widget, height=0, cursor="sb_h_double_arrow", background=border_color)
        self.right.pack(side=tk.RIGHT, ipadx=1, fill=tk.Y)

    def top_click(self, evt=None):
        self._topx = self.top.winfo_x()
        self._topy = self.top.winfo_y()
        self._widgetx = self.widget.winfo_x()
        self._widgety = self.widget.winfo_y()
        self._widgetrootx = self.widget.winfo_rootx()
        self._widgetrooty = self.widget.winfo_rooty()

    def top_move(self, evt=None):
        widgetx = 0
        if self.iswindow:
            self.widget.geometry(f"")

    def bottom_move(self, evt=None):
        if self.iswindow:
            self.widget.geometry(f"{self.widget.winfo_width()}x{self.bottom.winfo_y()}")


class DevSideBar(tk.Frame):
    def __init__(self, master: tk.Widget, background="#ffffff", ):
        super(DevSideBar, self).__init__(master=master, background=background)

    def add_action(self, text: str = "", icon: str = None, commnad=None,
                   default_bg: str = "#ffffff", default_fg: str = "#000000",
                   font=("等线 Light", 10, "bold"), side=tk.TOP,
                   active_bg: str = "#177aff", active_fg: str = "#d6eaff",
                   click_bg: str = "#175bff", click_fg: str = "#d6deff"):
        if icon is None:
            button_icon = None
        else:
            button_icon = tk.PhotoImage(file=icon)
        return DevButton(self, text=text, image=button_icon, command=commnad,
                         default_bg=default_bg, default_fg=default_fg, font=font,
                         active_bg=active_bg, active_fg=active_fg,
                         click_bg=click_bg, click_fg=click_fg).pack(side=side)

    def show(self, side: str = tk.LEFT):
        self.pack(side=side, fill=tk.Y)


class DevStatusBar(tk.Frame):
    def __init__(self, master: tk.Widget = None, default_text: str = "", sizegrip: bool = True, background="#fcfcfc",
                 foreground="#000000"):
        """
        简单的状态栏，使用show可以将它显示出来，使用add_status在鼠标指针移动到组件上时，状态栏会显示状态文本。

        :param master:
        :param default_text:
        :param background
        """
        super(DevStatusBar, self).__init__(master=master, background=background, )
        self.widgetlist = []
        self.master = master
        self.default_text = default_text
        self.style = ttk.Style()
        self.style.configure("Dev.TSizegrip", background=background, foreground=foreground)
        self.status = tk.Label(self, text=default_text, background=background, foreground=foreground)
        self.status.pack(side=tk.LEFT, expand=tk.NO)
        self.sizegrip = ttk.Sizegrip(self, style="Dev.TSizegrip")
        if sizegrip:
            self.sizegrip.pack(side=tk.RIGHT, anchor=tk.SE, expand=tk.NO)

    def add_status(self, widget: tk.Widget, status: str = ""):
        self.widgetlist.append(widget)
        widget.bind("<Enter>", lambda event: self.status.configure(text=status))
        widget.bind("<Leave>", lambda event: self.status.configure(text=self.default_text))

    def set_sizegrip(self, sizegrip: ttk.Sizegrip):
        self.sizegrip = sizegrip

    def show(self):
        self.pack(fill=tk.X, side=tk.BOTTOM)


class DevSubWindow(tk.Frame):
    def __init__(self, master, title_label: str = "Title", background="white",
                 button_side=tk.RIGHT,
                 titlebar_background="white",
                 close: bool = True, max: bool = True, min: bool = True, title: bool = True,
                 title_bg="#ffffff", title_fg="#000000",
                 close_bg="#ffffff", max_bg="#ffffff", min_bg="#ffffff", close_func=None,
                 close_active_bg="#e81123", close_active_fg="#f5f5f5", max_active_bg="#c2c2c2", max_active_fg="#ffffff",
                 min_active_bg="#c2c2c2", min_active_fg="#ffffff",
                 close_fg="#000000", max_fg="#000000", min_fg="#000000"):
        """
        实现了子窗口的功能，在tkinter中没有子窗口，我终于研究成功了。他是个框架，你可以将他使用pack、place进行显示

        :param master:
        :param title:
        :param background:
        :param titlebar_background:
        :param titlebar_foreground:
        """
        super(DevSubWindow, self).__init__(master=master, background=background, borderwidth=1, relief=tk.RIDGE)
        self.titlebar = DevTitleBar(master=self, iswindow=False, widget=self, button_side=button_side,
                                    background=titlebar_background,
                                    close=close, max=max, min=min, title=title, title_label=title_label,
                                    title_bg=title_bg, title_fg=title_fg,
                                    close_bg=close_bg, max_bg=max_bg, min_bg=min_bg, close_func=None,
                                    close_active_bg=close_active_bg, close_active_fg=close_active_fg,
                                    max_active_bg=max_active_bg,
                                    max_active_fg=max_active_fg, min_active_bg=min_active_bg,
                                    min_active_fg=min_active_fg,
                                    close_fg=close_fg, max_fg=max_fg, min_fg=min_fg)
        self.titlebar.pack(fill=tk.X, side=tk.TOP)
        self.bind("Configure", DevResize)
        resize_widget(self)
        self.update()

    def set_titlebar(self, titlebar):
        self.titlebar = titlebar

    def show(self):
        self.place(x=0, y=0, width=300, height=300)


class DevToolTip(tktooltip.ToolTip):
    def __init__(self, widget: tk.Widget,
                 msg: str = "",
                 delay: float = 1.0,
                 follow: bool = True,
                 refresh: float = 1.0,
                 x_offset: int = +10,
                 y_offset: int = +10,
                 parent_kwargs: dict = {"bg": "black", "padx": 1, "pady": 1},
                 foreground: str = "#ffffff", background="#1c1c1c",
                 **message_kwargs):
        """
        本人比较懒，不想写，就用了tkinter-tooltip组件，请不要喷我

        :param widget:
        :param msg:
        :param delay:
        :param follow:
        :param refresh:
        :param x_offset:
        :param y_offset:
        :param parent_kwargs:
        :param foreground:
        :param background:
        :param message_kwargs:
        """
        super(DevToolTip, self).__init__(widget=widget, msg=msg, delay=delay, follow=follow, refresh=refresh,
                                         x_offset=x_offset, y_offset=y_offset, parent_kwargs=parent_kwargs,
                                         fg=foreground, bg=background)


class DevTitleBar(tk.Frame):
    def __init__(self, master: tk.Widget, iswindow: bool = True, window: tk.Tk = None, widget: tk.Widget = None,
                 button_side: str = tk.RIGHT, background="#ffffff",
                 close: bool = True, max: bool = True, min: bool = True, title: bool = True, title_label: str = "",
                 title_bg="#ffffff", title_fg="#000000",
                 close_bg="#ffffff", max_bg="#ffffff", min_bg="#ffffff", close_func=None,
                 close_active_bg="#e81123", close_active_fg="#f5f5f5", max_active_bg="#c2c2c2", max_active_fg="#ffffff",
                 min_active_bg="#c2c2c2", min_active_fg="#ffffff", minwindow_border_color="#35384b",
                 minwindow_icon=None,
                 close_fg="#000000", max_fg="#000000", min_fg="#000000"):
        super(DevTitleBar, self).__init__(background=background, master=master)
        self.widget = widget
        self.button_side = button_side
        self.title = title
        self.title_label = title_label
        self.title_bg = title_bg
        self.title_fg = title_fg
        self.close = close
        self.close_bg = close_bg
        self.close_fg = close_fg
        self.close_active_bg = close_active_bg
        self.close_active_fg = close_active_fg
        self.close_func = close_func
        self.max = max
        self.max_bg = max_bg
        self.max_fg = max_fg
        self.max_active_bg = max_active_bg
        self.max_active_fg = max_active_fg
        self.min = min
        self.min_bg = min_bg
        self.min_fg = min_fg
        self.min_active_bg = min_active_bg
        self.min_active_fg = min_active_fg
        self.minwindow_border_color = minwindow_border_color
        self.minwindow_icon = minwindow_icon

        self.ismax = False

        if self.title:
            self.add_title(title=self.title_label, title_bg=self.title_bg, title_fg=self.title_fg)
        if self.close:
            self.add_close(close_bg=self.close_bg, close_fg=self.close_fg, close_active_bg=self.close_active_bg,
                           close_active_fg=self.close_active_fg, close_func=self.close_func)
        if self.max:
            self.add_max(max_bg=self.max_bg, max_fg=self.max_fg, max_active_bg=self.max_active_bg,
                         max_active_fg=self.max_active_fg)
        if self.min:
            self.add_min(min_bg=self.min_bg, min_fg=self.min_fg, min_active_bg=self.min_active_bg,
                         min_active_fg=self.min_active_fg)
        self.widget = widget
        DevDrag(self, self.widget)
        self.window = window
        self.iswindow = iswindow

        if self.iswindow:
            if self.close:
                self.closebutton.configure(command=self.widget_close)
            if self.max:
                self.maxbutton.configure(command=self.widget_max)
            if self.min:
                self.minbutton.configure(command=self.widget_min)
        else:
            if self.close:
                self.closebutton.configure(command=self.widget_close)
            if self.max:
                self.maxbutton.configure(command=self.widget_max)
            if self.min:
                self.minbutton.configure(command=self.widget_min)
        self.bind("<Double-Button-1>", lambda evt: self.widget_max())

    def add_title(self, title: str = "", title_bg="#ffffff", title_fg="#000000"):
        self.title = tk.Label(self, text=title, background=title_bg, foreground=title_fg)
        self.title.pack(fill=tk.X, side=tk.LEFT, padx=5)

    def add_close(self, close_bg="#ffffff", close_fg="#000000", close_active_bg="#e81123", close_active_fg="#f5f5f5",
                  close_func=None):
        self.closebutton = tk.Button(self, text='×', borderwidth=0, background=close_bg, foreground=close_fg,
                                     activebackground=close_active_bg, command=close_func,
                                     activeforeground=close_active_fg)
        self.closebutton.pack(fill=tk.Y, side=self.button_side, ipadx=5)

    def add_max(self, max_bg="#ffffff", max_fg="#000000", max_active_bg="#c2c2c2", max_active_fg="#ffffff"):
        self.maxbutton = tk.Button(self, text="▢", borderwidth=0, background=max_bg, foreground=max_fg,
                                   activebackground=max_active_bg,
                                   activeforeground=max_active_fg)
        self.maxbutton.pack(fill=tk.Y, side=self.button_side, ipadx=5)

    def add_min(self, min_bg="#ffffff", min_fg="#000000", min_active_bg="#c2c2c2", min_active_fg="#ffffff"):
        self.minbutton = tk.Button(self, text="-", borderwidth=0, background=min_bg, foreground=min_fg,
                                   activebackground=min_active_bg,
                                   activeforeground=min_active_fg)
        self.minbutton.pack(fill=tk.Y, side=self.button_side, ipadx=8)

    def widget_close(self):
        if self.iswindow:
            self.window.destroy()
        elif not self.iswindow:
            self.widget.destroy()

    def widget_max(self):
        if self.iswindow:
            if self.ismax:
                self.window.geometry(f"{self._width}x{self._height}+{self._x}+{self._y}")
                self.ismax = False
            elif not self.ismax:
                self._x = self.window.winfo_x()
                self._y = self.window.winfo_y()
                self._width = self.window.winfo_width()
                self._height = self.window.winfo_height()
                self.window.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
                self.window.attributes('-topmost', 1)
                self.window.attributes('-topmost', 0)
                self.window.geometry("+0+0")
                self.ismax = True
            self.window.update()
        if not self.iswindow:
            if self.ismax:
                self.widget.place(width=self._width, height=self._height, x=self._x, y=self._y)
                self.ismax = False
            elif not self.ismax:
                self._x = self.widget.winfo_x()
                self._y = self.widget.winfo_y()
                self._width = self.widget.winfo_width()
                self._height = self.widget.winfo_height()
                self.widget.place(width=self.widget.master.winfo_width(), height=self.widget.master.winfo_height(), x=0,
                                  y=0)
                self.widget.place(x=0, y=0)
                self.ismax = True
            self.widget.update()
        self.update()

    def widget_min(self):
        if self.iswindow:
            windowsize = (self.window.winfo_width(), self.window.winfo_height())
            self.window.withdraw()
            self.minwindow = DevToplevel()
            self.minwindow.configure(background=self.window.cget("background"))
            self.minwindow.geometry(f"50x50+{windowsize[0]}+{windowsize[1]}")
            self.minwindow.overrideredirect(True)
            if self.minwindow_icon is None:
                pass
            else:
                self.image = tk.Label(self.minwindow, image=tk.PhotoImage(file=self.minwindow_icon))
                self.image.pack(fill=tk.BOTH, expand=tk.YES, padx=5, pady=5)
            resize = DevBorder(self.minwindow, border_color=self.minwindow_border_color)
            add_taskbar(self.minwindow)
            self.minwindow.attributes("-topmost", True)
            DevDrag(self.minwindow, self.minwindow, iswindow=True)

            def show_window(evt):
                self.window.deiconify()
                self.window.attributes("-topmost", True)
                self.minwindow.destroy()
                self.window.attributes("-topmost", False)

            self.minwindow.bind("<Double-Button-1>", show_window)

    def show(self):
        self.pack(fill=tk.X, side=tk.TOP)


class DevToast(tk.Toplevel):
    def __init__(self, master: tk.Tk = None,
                 title: str = "Title", message: str = "Message", height: int = 80):
        super(DevToast, self).__init__(master=master)
        self.overrideredirect(True)
        self.title = tk.Label(self, text=title, justify=tk.LEFT, anchor=tk.W)
        self.title.pack(side=tk.TOP, fill=tk.X)
        self.message = tk.Label(self, text=message, justify=tk.LEFT, anchor=tk.W)
        self.message.pack(side=tk.TOP, fill=tk.X)
        self.height = height
        self.withdraw()

    def show_toast(self):
        x = 20
        y = 20
        width = self.winfo_screenwidth() - x * 2
        height = self.height

        self.deiconify()

        self.geometry(f"{round(width)}x{round(height)}+{x}+{y}")
        self.attributes("-topmost", True)


class DevToplevel(tk.Toplevel):
    def __init__(self, master: tk.Tk = None):
        super(DevToplevel, self).__init__(master=master)
        self.title("tkDev")
        self.geometry("500x500")
        self.configure(background="#f0f0f0")

    def wm_statusBar(self, statusBar: tk.Widget):
        self._statusBar = statusBar
        self._statusBar.pack(fill=tk.X, side=tk.BOTTOM)
        return self._statusBar

    statusbar = wm_statusBar

    def wm_titleBar(self, titleBar: tk.Label, showtask: bool = True):
        from ctypes import windll
        self.minsize(100, 30)
        self.overrideredirect(True)
        if showtask:
            self.after(10, lambda: add_taskbar(self))
        self._titlebar = titleBar
        self._titlebar.pack(fill=tk.X, side=tk.TOP)
        DevDrag(self._titlebar, self, True)
        return self._titlebar

    titlebar = wm_titleBar

    def wm_centre(self):
        self.after(1, lambda evt=None: window_centre(self))

    centre = wm_centre

    def min_window(self):
        self.withdraw()
        self.minwindow = DevToplevel(self)
        self.minwindow.overrideredirect(True)
        self.minwindow.attributes("-topmost", True)
        DevDrag(self.minwindow, self.minwindow, iswindow=True)
        self.minwindow.bind("<Double-Button-1>", lambda evt: self.deiconify())


class DevWindow(tk.Tk):
    def __init__(self):
        super(DevWindow, self).__init__()
        self.title("tkDev")
        self.geometry("500x500")
        self.configure(background="#f0f0f0")

    def wm_statusbar(self, statusBar: tk.Widget):
        self._statusBar = statusBar
        self._statusBar.pack(fill=tk.X, side=tk.BOTTOM)
        return self._statusBar

    statusbar = wm_statusbar

    def wm_titlebar(self, titleBar: tk.Label, showtask: bool = True):
        from ctypes import windll
        self.minsize(100, 30)
        self.overrideredirect(True)
        if showtask:
            self.after(10, lambda: add_taskbar(self))
        self._titlebar = titleBar
        self._titlebar.pack(fill=tk.X, side=tk.TOP)
        DevDrag(self._titlebar, self, True)
        return self._titlebar

    titlebar = wm_titlebar

    def wm_menubar(self, menubar: DevMenuBar):
        menubar.show()

    menubar = wm_menubar

    def wm_centre(self):
        self.after(1, lambda evt=None: window_centre(self))

    centre = wm_centre

    def min_window(self):
        self.withdraw()
        self.minwindow = DevToplevel(self)
        self.minwindow.overrideredirect(True)
        self.minwindow.attributes("-topmost", True)
        DevDrag(self.minwindow, self.minwindow, iswindow=True)
        self.minwindow.bind("<Double-Button-1>", lambda evt: self.deiconify())


if __name__ == '__main__':
    Root = DevWindow()
    Root.centre()
    Root.mainloop()
