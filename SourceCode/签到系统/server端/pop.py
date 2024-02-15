import tkinter as tk

def create_popup(txt):
    # 创建一个新的窗口
    popup = tk.Tk()
    popup.geometry("800x100")
    popup.wm_title("server端消息")
    # 在窗口中添加一些文本
    label = tk.Label(popup, text=str(txt),font=("Helvetica", 20))
    label.pack()

    # 设置一个定时器，在10秒后关闭窗口
    popup.after(1000, popup.destroy)

    # 显示窗口，直到它被关闭
    popup.mainloop()