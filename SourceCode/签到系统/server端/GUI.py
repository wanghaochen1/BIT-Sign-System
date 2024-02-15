import tkinter
# 第四步：设计GUI
# 1. 导入第三方库
import os
import tkinter as tk
import time
def server_window():
    def show_time():
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        time_label.config(text=current_time)
        windows.after(1000, show_time)
  
    windows = tk.Tk()  # 创建windows的窗口
    windows.title('服务端窗口')  # 窗口名称
    windows.geometry('500x600+1000+100')  # 窗口大小（注：x是小写字母x，不能写乘号*），+1000+100表
    #在窗口的最上面显示现在的时间
    def function6():
        windows.destroy()
    time_label = tk.Label(windows, text='', font=('Arial', 25))
    time_label.pack()
    show_time()  # 初始化时间
    #给时间添加一个背景，让时间更加醒目
    time_label.config(bg='blue', fg='white')
    # 在窗口上添加一个标签
    label = tk.Label(windows, text='欢迎使用服务端', font=('Arial', 20))
    label.pack()
    label.config(bg='blue', fg='green')
    #添加一个退出窗口，摁了退出窗口就退出程序
    button = tk.Button(windows, text='开始签到', font=('Arial', 20), width=10, height=1,command=lambda: function6())
    button.pack()
    windows.mainloop()
   