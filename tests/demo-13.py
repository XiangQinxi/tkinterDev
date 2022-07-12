# 导入包
import tkinter


# 计算窗口居中的位置
def get_window_positon(width, height):
    system_metrics = get_system_metrics()
    window_x_position = (system_metrics[0] - width) // 2
    window_y_position = (system_metrics[1] - height) // 2
    return window_x_position, window_y_position


# 设置窗口属性
login = tkinter.Tk()
login.title('此处输入窗口的标题')
tk_width = 324  # 窗口的宽度
tk_height = 180  # 窗口的长度
pos = get_window_positon(tk_width, tk_height)  # 调用get_window_positon()方法
login.geometry(f'{tk_width}x{tk_height}+{pos[0]}+{pos[1]}')  # 窗口的大小与位置
login.resizable(False, False)  # 窗口大小不可变

# 显示窗口
login.mainloop() 