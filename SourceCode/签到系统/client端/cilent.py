import socket
import sys
import tkinter as tk
import GUI_fun
import send_client
import read_from_server
import os
from PIL import Image, ImageTk
import all_function
import secret
import hashlib
s=None#定义全局变量s，用于指定socket
stu_number=None#定义全局变量stu_number，用于指定学号
Var_Pass=False
#定义socket连接函数
def socket_connect(host,port):
    global s #给全局的s赋值
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except:
        print(f"出现问题\n")
        sys.exit(1)#退出程序
    print("\n已连接到server\n")
    return s


#定义登陆认证函数
def comp(window_connect,stu_num,stu_password):
    global stu_number
    global Var_Pass#使用全局的Var_Pass
    #测试能否连接到server
    #给学号赋值
    stu_num=secret.hash_password(stu_num)
    stu_number=stu_num
    print("\n正在等待老师打开签到连接\n")
    socket_connect('127.0.0.1',12345)
    print("\n可以开始签到,正在进行登陆认证\n")
    #检查账号密码是否正确
    send_client.login(stu_num,stu_password,s)
    if read_from_server.identify_result(s) :
        Var_Pass=True
        print("\n登陆成功\n")
        window_connect.destroy()
        return
    else:
        Var_Pass=False
        print("\n登陆失败\n")
        return

#定义初始连接界面
def create_window():
    def fun_temp():
        if all_function.log_in_with_face():
            if os.path.exists('credentials.pkl'):
                user_number=secret.load_credentials()[0]
                user_password=secret.load_credentials()[1]
                comp(window_connect,str(user_number),str(user_password))
        else:
            print("人脸识别登陆失败")
        return
    window_connect=tk.Tk()
    window_connect.title("登陆界面")
    window_connect.geometry("500x1000+1000+100")
    #创建标签
    tk.Label(window_connect,text="统一身份认证登陆",bg='maroon',fg='white',font=('宋体',20),width=30,height=2).pack()

    #在窗口的最上端的中间，创建一个图片，放入dataset中的图片
    canvas=tk.Canvas(window_connect,height=500,width=500)
    image_path = os.path.join('R-C.png')
    image = Image.open(image_path)
    window_connect.photo = ImageTk.PhotoImage(image)   # 修改这里
    image=canvas.create_image(250,0,anchor='n',image=window_connect.photo)  # 修改这里
    canvas.pack(side='top')

    #创建一个按钮，上面写着人脸识别登陆
    tk.Button(window_connect,text="人脸识别登陆",font=('宋体',20),width=15,command=lambda:fun_temp()).pack()


    #定义学号输入框
    tk.Label(window_connect,text="学号",font=('宋体',20),width=30).pack()
    stu_num=tk.Entry(window_connect,show=None,font=('宋体',20),width=15)
    stu_num.pack(anchor='center')  # Center-align the input field

    #定义密码输入框
    tk.Label(window_connect,text="密码",font=('宋体',20),width=30).pack()
    stu_password=tk.Entry(window_connect,show="*",font=('宋体',20),width=30)
    stu_password.pack(anchor='center')
    
    #定义登陆按钮
    tk.Button(window_connect,text="登陆",font=('宋体',20),width=10,command=lambda:comp(window_connect,stu_num.get(),stu_password.get())).pack()

    return window_connect

#创建主函数
window_1=create_window()
window_1.mainloop()

#判断是否成功登陆：
if Var_Pass is True:
    print(f"已成功登陆，学号为{stu_number}")
    GUI_fun.Sign_window(s,stu_number)
else:
    print("请重启界面")
