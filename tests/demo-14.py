from src.tkdev import *


class PyFactory(DevWindow):
    def __init__(self):
        super(PyFactory, self).__init__()
        self.setup_ui()
        self.setup()
        self.title("PyFactory")
        self.attributes("-alpha", 0.975)
        self.minsize(100, 55)
        self.geometry("700x400")
        self.configure(background="#282c34")
        self.iconbitmap("python-factory.ico")
        self.centre()

    def setup_ui(self):
        self.devtitlebar = DevTitleBar(self, iswindow=True, window=self, background="#21252b", title=False,
                                       title_bg="#21252b", title_fg="#c5c7cd",
                                       close_bg="#21252b", close_fg="#c5c7cd",
                                       max_bg="#21252b", max_fg="#c5c7cd", max_active_bg="#3e4551",
                                       min_bg="#21252b", min_fg="#c5c7cd", min_active_bg="#3e4551",
                                       minwindow_icon="python-factory.gif")
        self.titlebar_mainmenu = DevButton(self.devtitlebar, text="≣", default_bg="#21252b", default_fg="#c5c7cd", active_bg="#17deff", click_bg="#17ceff")
        self.titlebar_mainmenu.pack(side=tk.LEFT, ipadx=5, ipady=3)
        #self.titlebar_settings = DevButton(self.devtitlebar, text="", default_bg="#21252b", default_fg="#c5c7cd", font=("等线 Light", 1, "bold"))
        #self.titlebar_settings.pack(side=tk.RIGHT, ipadx=5, ipady=3, padx=3)
        self.titlebar_run = DevButton(self.devtitlebar, text="▷", default_bg="#21252b", default_fg="#c5c7cd", active_bg="#17deff", click_bg="#17ceff")
        self.titlebar_run.pack(side=tk.RIGHT, ipadx=5, ipady=3, padx=3)
        self.devstatusbar = DevStatusBar(self, "状态栏 | ", background="#21252b", foreground="#c5c7cd")
        Resize = DevResize(self, border_color="#35384b")
        self.titlebar(self.devtitlebar, showtask=True)
        self.statusbar(self.devstatusbar)
        self.sidebar = DevSideBar(self, background="#21252b")
        self.sidebar_files = self.sidebar.add_action("📂", default_bg="#21252b", default_fg="#c5c7cd", active_bg="#17deff", click_bg="#17ceff")
        self.sidebar_settings = self.sidebar.add_action("⚙", default_bg="#21252b", default_fg="#c5c7cd", active_bg="#17deff", click_bg="#17ceff")
        self.sidebar.show()

    def setup(self):
        self.editor_area = tk.Frame(self, background="#282c34")
        self.editor = tk.Text(self.editor_area, background="#282c34", foreground="#abb2bf", relief=tk.FLAT, selectbackground="#17deff", selectforeground="#282c34")
        self.editor_vbar = tk.Scrollbar(self.editor_area, background="#282c34", orient=tk.VERTICAL)
        self.editor.configure(yscrollcommand=self.editor_vbar.set)
        self.editor_vbar.configure(command=self.editor.yview)
        self.editor_vbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.editor.pack(fill=tk.BOTH, expand=tk.YES)
        self.editor_area.pack(fill=tk.BOTH, expand=tk.YES)


if __name__ == '__main__':
    root = PyFactory()
    root.mainloop()