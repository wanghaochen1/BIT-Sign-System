import tkinter as tk
from tkinter import scrolledtext
import time
import pandas as pd

windows = tk.Tk()  # 创建windows的窗口
windows.title('教师端窗口')  # 窗口名称
windows.geometry('800x600+1000+100')  # 窗口大小（注：x是小写字母x，不能写乘号*），+1000+100表

welcome_label = tk.Label(windows, text="欢迎使用教师端", fg="white", bg="maroon", font=("Arial", 20))
welcome_label.pack()

current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
time_label = tk.Label(windows, text="当前时间：" + current_time, fg="white", bg="maroon", font=("Arial", 16))
time_label.pack()

# 打开db.xlsx文件
df = pd.read_excel('db.xlsx', sheet_name='Log_in')


second_row = df.iloc[0]

# 找到第二行最后一个非空元素的位置
last_non_empty_position = second_row.last_valid_index()

# 获取列名对应的列数
column_number = df.columns.get_loc(last_non_empty_position)

signtimes=column_number+1

#添加一个Label
label = tk.Label(windows, text=f"这是第{signtimes}次签到", fg="white", bg="maroon", font=("Arial", 16))
label.pack()

def update_text():
    # 打开db.xlsx文件
    df = pd.read_excel('db.xlsx', sheet_name='Log_in')
    # 访问signtimes列
    signtimes_column = df.iloc[:, signtimes-1]
     # 计算signtimes列中非空的个数   
    non_empty_count = signtimes_column.count()
    text_area.insert(tk.END, f"目前有{non_empty_count}人签到\n")
    # 自动滚动到文本区域的末尾
    text_area.see(tk.END)

# 滚动更新窗口
text_area = scrolledtext.ScrolledText(windows, width=40, height=20)  # Increase the height to 20
text_area.pack()

button = tk.Button(windows, text="刷新", command=update_text, font=("Arial", 20), padx=10, pady=10)
button.pack()

windows.mainloop()