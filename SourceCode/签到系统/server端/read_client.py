import socket 
import json
import server_fun
import read_client
import send_by_server
from datetime import datetime
from db import *
import pop
import tkinter as tk
import time
# con=sql_connection()
def signing_UI():
    
    windows = tk.Tk()  # 创建windows的窗口
    windows.title('教师端窗口')  # 窗口名称
    windows.geometry('500x600+1000+100')  # 窗口大小（注：x是小写字母x，不能写乘号*），+1000+100表

    welcome_label = tk.Label(windows, text="欢迎使用教师端", fg="white", bg="maroon", font=("Arial", 20))
    welcome_label.pack()

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    time_label = tk.Label(windows, text="当前时间：" + current_time, fg="white", bg="maroon")
    time_label.pack()


    windows.mainloop()
def read(con,client_socket,json_str):
    data=json.loads(json_str)
    usage=data['usage']
    #用户使用账号密码登录
    if usage == 'login':
        print("\n用户申请登录\n")
        stu_num=data['stu_num']
        stu_password=data['stu_password']
        pop.create_popup(f"学号：{stu_num}，密码：{stu_password}，尝试登录")
        print("学号：",stu_num,"密码：",stu_password,"尝试登录\n")
        if server_fun.check(con,stu_num,stu_password):
            print("\n用户登录成功\n")
            pop.create_popup("登录成功")
            send_by_server.send_login_information(client_socket,True)
        else:
            pop.create_popup("登录失败")
            print("\n用户登录失败\n")
            send_by_server.send_login_information(client_socket,False) 
    #用户请求更换人脸
    elif usage == 'change_face':
        stu_num=data['stu_num']
        pop.create_popup(f"学号：{stu_num}，请求更换人脸")
        print(f"\n用户{stu_num}请求更换人脸\n")
        if server_fun.allow_change_face(con,stu_num):
            send_by_server.send_change_face_information(client_socket,True)
        else:
            send_by_server.send_change_face_information(client_socket,False)
            
    elif usage == 'sign_in':
        pop.create_popup("用户请求签到")
        print("\n用户请求签到\n")
        stu_num=data['stu_num']
        signtime=datetime.now()
        pop.create_popup(f"学号{stu_num}，签到时间{signtime}，尝试签到")
        print("学号：",stu_num,"签到时间：",signtime,"尝试签到\n")
        if server_fun.write_sign_in(con,stu_num,signtime):
            send_by_server.send_sign_in_information(client_socket,True)
        else:
            send_by_server.send_sign_in_information(client_socket,False)    
    
    elif usage == 'sign_out':
        print("\n用户请求签退\n")
        stu_num=data['stu_num']
        pop.create_popup(f"学号{stu_num}，尝试签退")
        #读取本机时间
        sign_out_time=datetime.now()
        print("学号：",stu_num,"签退时间：",sign_out_time,"尝试签退\n")
        pop.create_popup(f"学号{stu_num}，签退时间{sign_out_time}，尝试签退")
        if server_fun.write_sign_out(con,stu_num,sign_out_time):
            send_by_server.send_sign_out_information(client_socket,True)
        else:
            send_by_server.send_sign_out_information(client_socket,False)

    elif usage == 'user_image':
        print("\n用户请求用户画像\n")
        stu_num=data['stu_num']
        pop.create_popup(f"学号{stu_num}，尝试获取用户画像")
        print("学号：",stu_num,"尝试获取用户画像\n")
        time = server_fun.user_image(con,stu_num)
        send_by_server.send_user_image(client_socket,time)

import hashlib
import pickle

def save_credentials(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()  # 生成密码的哈希值
    with open('credentials.pkl', 'wb') as f:
        pickle.dump((username, password_hash), f)  # 存储用户名和密码的哈希值

def load_credentials():
    try:
        with open('credentials.pkl', 'rb') as f:
            username, password_hash = pickle.load(f)
            return username, password_hash
    except FileNotFoundError:
        return None, None

# 保存用户名和密码的哈希值
save_credentials('my_username', 'my_password')

# 加载用户名和密码的哈希值
username, password_hash = load_credentials()
if username and password_hash:
    print(f'Loaded credentials for {username}')
else:
    print('No saved credentials found')