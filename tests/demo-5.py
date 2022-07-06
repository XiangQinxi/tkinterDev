from tkinter import *
from tkinter import dnd



root = Tk()
root.title('tkinter鼠标样式 wb98·com')
root.wm_attributes('-topmost', 1)
# 以下是鼠标光标样式列表，共77种
cursorList = ['arrow', 'double_arrow', 'man', 'sizing',
              'based_arrow_down', 'draft_large', 'middlebutton', 'spider',
              'based_arrow_up', 'draft_small', 'mouse', 'spraycan',
              'boat', 'draped_box', 'pencil', 'star',
              'bogosity', 'exchange', 'pirate', 'target',
              'bottom_left_corner', 'fleur', 'plus', 'tcross',
              'bottom_right_corner', 'gobbler', 'question_arrow', 'top_left_arrow',
              'bottom_side', 'gumby', 'right_ptr', 'top_left_corner',
              'bottom_tee', 'hand1', 'right_side', 'top_right_corner',
              'box_spiral', 'hand2', 'right_tee', 'top_side',
              'center_ptr', 'heart', 'rightbutton', 'top_tee',
              'circle', 'icon', 'rtl_logo', 'trek',
              'clock', 'iron_cross', 'sailboat', 'ul_angle',
              'coffee_mug', 'left_ptr', 'sb_down_arrow', 'umbrella',
              'cross', 'left_side', 'sb_h_double_arrow', 'ur_angle',
              'cross_reverse', 'left_tee', 'sb_left_arrow', 'watch',
              'crosshair', 'leftbutton', 'sb_right_arrow', 'xterm',
              'diamond_cross', 'll_angle', 'sb_up_arrow', 'X_cursor',
              'dot', 'lr_angle', 'sb_v_double_arrow',
              'dotbox', 'shuttle']

row1 = 0  # 行，初始化
col1 = 0  # 列，初始化
for i in cursorList:
    Label(root, text=i, cursor=i, relief='raised').grid(row=row1, column=col1, sticky=W + E, ipadx=20, ipady=5)
    col1 = col1 + 1
    if col1 == 4:  # 每行显示4个样式
        row1 = row1 + 1  # 换下一行
        col1 = 0  # 列返回第1列

root.mainloop()