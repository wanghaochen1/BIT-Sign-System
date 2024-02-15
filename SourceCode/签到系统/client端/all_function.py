import cv2
import os
from PIL import Image
import numpy as np
from datetime import datetime
import cv2
import time
import send_client
import read_from_server
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import userimage
#引入库~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def user_image_GUI(stu_number,time):
    fame=userimage.user_fame(time)
    class Ball:
        def __init__(self, canvas, windows, x, y, dx, dy):
            self.canvas = canvas
            self.windows = windows
            self.x = x
            self.y = y
            self.dx = dx
            self.dy = dy
            self.ball = canvas.create_oval(x, y, x+100, y+100, fill='red')
            self.text = canvas.create_text((x+x+100)/2, (y+y+100)/2, text=f'str{fame}',font=('宋体',20))

        def move(self):
            self.canvas.move(self.ball, self.dx, self.dy)
            self.canvas.move(self.text, self.dx, self.dy)  # 移动文本与球同步
            if self.canvas.winfo_width() < self.x + 50 or self.x < 0:
                self.dx = -self.dx
            if self.canvas.winfo_height() < self.y + 50 or self.y < 0:
                self.dy = -self.dy
            self.x += self.dx
            self.y += self.dy

        def animate(self):
            self.move()
            self.windows.after(20, self.animate)  # 20毫秒后再次调用animate
    #创建一个新的窗口
    windows = tk.Tk()  # 创建windows的窗口
    windows.title('你的用户画像')  # 窗口名称
    windows.geometry('500x600+1000+100')
    #获得签到情况
    [morning_in,morning_out,night_in,night_out]=userimage.count(time)
    #记录总签到时间
    classtime=userimage.class_time(time)
    #创建一个文字框
    label_head=tk.Label(windows,text=f"你本月一共签到/退 {morning_in+night_in} 次，其中下午签到/退 {night_in} 次",bg='maroon',fg='white',font=('宋体',15),width=60,height=2)
    label_head.pack()
    #创建一个文字框
    label_type=tk.Label(windows,text=f"本学期累计上课时间{classtime}",bg='blue',fg='white',font=('宋体',20),width=40,height=2)
    label_type.pack()
    
    #绘制历次签到时间图
    x = range(len(time))  # 假设 x 是一个表示时间序列的列表
    fig, ax = plt.subplots(figsize=(5, 2))
    if len(x) > len(time):
        x = x[:len(time)]
    # 如果 time 的长度大于 x 的长度，截取 time
    elif len(time) > len(x):
        time = time[:len(x)]

    ax.plot(x, time)
    ax.legend(["Sign in","Sign out"], loc='upper right')
    canvas = FigureCanvasTkAgg(fig, master=windows)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack()
    #预测下次签到时间
    pre_time=datetime.now()
    label_head=tk.Label(windows,text=f"你下次签到时间可能是{pre_time},仅供参考",bg='maroon',fg='white',font=('宋体',10),width=60,height=2)
    label_head.pack()
    #写荣誉称号
    label_head=tk.Label(windows,text=f"获得荣誉称号*{fame}*",bg='green',fg='white',font=('宋体',20),width=30,height=2)
    label_head.pack()
    #绘制小球动画
    canvas = tk.Canvas(windows, width=400, height=400)
    canvas.pack()
    ball = Ball(canvas, windows,0, 0, 2.5, 2.5)

    ball.animate()
    #绘制小球动画
    #根据time返回的数据，创建一个图片，使用plot
    windows.mainloop()
#人脸采集函数
def capture_face(s,stu_number):
    send_client.change_face(s,stu_number)
    if read_from_server.identify_result(s):
        print('同意更换人脸\n')
        font = cv2.FONT_HERSHEY_SIMPLEX    # 定义字体，使用opencv中的FONT_HERSHEY_SIMPLEX字体
        classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  # 导入人脸检测级联文件。CascadeClassifier是opencv中做人脸检测时的一个级联分类器，对输入的图片进行分类，判断图像内是否有无人脸
        try:
            current_directory = os.getcwd()
            print(f"\n当前你人脸所在的目录为:{current_directory}\n")
            if not os.path.exists('dataset'):  # 判断项目目录中是否存在dataset文件（dataset中存放采集到的人脸图像）
                print('\n你是第一次录入人脸,正在创建dataset文件夹\n')
                os.mkdir('dataset')  # 如果没有就新建立dataset文件夹
            else:
                print("\n你已经录入过人脸,正在尝试重新导入\n")
                #清空dataset文件夹
                for root, dirs, files in os.walk('dataset'):
                    for name in files:
                        os.remove(os.path.join(root, name))
                print("\n已经清空dataset文件夹\n")
        except Exception as e:
            print("导入人脸出现问题,请联系管理员", str(e))
        finally:
            count = 0  # 人脸图像的初始数量
    else:
        print('拒绝更换人脸\n')
        return

    # 3.输入学号
    student_ID = 1120210529

    # 4.采集图像
    capture = cv2.VideoCapture(0)  # 打开电脑的内置摄像头

    while capture.isOpened():  # 当摄像头打开的时候
        kk = cv2.waitKey(1)    # 等待键盘的输入，1:表示延时1ms切换到下一帧图像
        _, frame = capture.read()   # 读取摄像头内容，返回两个参数
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # 将读取到的RGB图像转换为灰度图像
        faces = classifier.detectMultiScale(gray, 1.3, 5)  # 让classifier判断人脸，detectMultiScale函数可以检测出图像中的人脸，其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为minNeighbors
        if len(faces) != 0:  # 如果找到人脸
            # 框选人脸
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)  # 用矩形框框出人脸，xy为左上角的坐标,w为宽，h为高
                cv2.putText(frame, 'please "s" to save a picture ', (200, 450), font, 0.8, (0, 255, 255), 2)  # 在人脸图像上添加文字，参数依次表示：图像、要添加的文字、文字的位置、字体、字体大小、颜色、粗细

                if kk == ord('s'):  # ord(' ')将字符转化为对应的整数（ASCII码）
                    try:
                        cv2.imwrite('dataset/caixukun.'+str(student_ID)+'.'+str(count)+'.jpg', gray[y:y+h, x:x+w])  # 保存图像
                        count += 1  # 成功框选人脸后，则样本数增加
                        print('采集了'+str(count)+'张人脸图像')
                    except Exception as e:
                        print("采集人脸文件位置出现问题", str(e))

        cv2.putText(frame, 'please "esc" to quit ', (10, 20), font, 0.8, (0, 255, 255), 2)  # 在窗口上添加文字，参数依次表示：图像、要添加的文字、文字的位置、字体、字体大小、颜色、粗细

        cv2.imshow("picture from a cammre", frame)  # 打开窗口的名称
        if kk == 27:
            print('一共采集了' + str(student_ID) + '同学的' + str(count) + '张人脸图像')
            break

    # 5.退出程序
    capture.release()  # 释放变量
    cv2.destroyAllWindows()  # 检查有无打开窗口，有的话关掉

#人脸训练函数

def train(s):
    # 2. 加载特征提取模型
    recognizer_create = cv2.face.LBPHFaceRecognizer_create()

    # 3. 数据处理
    def data_translate(path):
        face_data = []
        id_data = []
        file_list = [os.path.join(path, f) for f in os.listdir(path)]
        # print(file_list)
        for file in file_list:
            PIL_image = Image.open(file).convert("L")
            np_image = np.array(PIL_image, 'uint8')
            image_id = int(file.split('.')[1])
            # print(image_id)
            face_data.append(np_image)
            id_data.append(image_id)
        return face_data, id_data

    # 4. 训练模型
    Face, ID = data_translate('dataset')
    recognizer_create.train(Face, np.array(ID))
    print('训练完成')

    # 5. 保存模型
    recognizer_create.save('face_model.yml')
    print('模型已保存')

#人脸识别签到
def sign_in(s,stu_number):
    def sign_name():
        send_client.sign_in(stu_number,datetime.now().strftime('%Y-%m-%d %H:%M:%S'),s)
        return read_from_server.identify_result(s)
    # 3. 导入模块，初始化变量
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    recognizer_create = cv2.face.LBPHFaceRecognizer_create()
    recognizer_create.read('face_model.yml')  # 读取训练好的模型
    flag = 0  # 标记次数

    ID = 'Unkonw'
    font = cv2.FONT_HERSHEY_SIMPLEX  # 定义字体，使用opencv中的FONT_HERSHEY_SIMPLEX字体

    # 4. 导入应到学生名单


    # 5.识别签到
    capture = cv2.VideoCapture(0)  # 打开摄像头

    while capture.isOpened():  # 当打开摄像头的时候
        kk = cv2.waitKey(1)  # 等待键盘的输入
        _, frame = capture.read()  # 读取摄像头内容
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # 将读取到的RGB图像转换为灰度图像
        faces = classifier.detectMultiScale(gray, 1.3, 5)  # 让classifier判断人脸，detectMultiScale函数可以检测出图像中的人脸
        if len(faces) != 0:  # 如果能找到人脸
            # 框选人脸
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)  # 用矩形框框出人脸，xy为左上角的坐标，w为宽，h为高
                roi_face = gray[y:y + h, x:x + w]
                label, conf = recognizer_create.predict(roi_face)  # 预测出的学号和可信度
                # print(label,conf)

                if conf < 60:
                    index = [list for list, i in enumerate(stu_number) if i == str(label)]  # 得到预测学号在excel表格中所在的行数（注：index的值是从0开始的，index=3表示在excel表格中的第4行）
                    # print(index)
                    flag+=1;
                    if index != []:
                        flag += 1
                    else:
                        ID = 'unknow'
            cv2.putText(frame, stu_number, (x, y-10), font, 0.8, (0, 0, 255), 2)  # 添加字幕

        cv2.putText(frame, 'press "esc" to quit ', (10, 20), font, 0.8, (0, 255, 255), 2)  # 在窗口上添加文字，参数依次表示：图像、要添加的文字、文字的位置、字体、字体大小、颜色、粗细
        cv2.imshow("picture from a cammre", frame)  # 打开窗口的名称
        if flag > 5:
            if sign_name():
                print('签到成功')
                break
            else:
                print('签到失败')
                break
        if kk == 27:  # 如果退出
            print('程序被终止，请重新签到！')
            break

    # 6.退出程序
    capture.release()  # 释放变量
    cv2.destroyAllWindows()  # 检查有无打开窗口，有的话关掉

    #签退
def sign_out(s,stu_number):
    send_client.sign_out(stu_number,s)
    return read_from_server.identify_result(s)

def show_user_image(s,stu_number):
    send_client.user_image(s,stu_number)
    return read_from_server.identify_result(s)

def log_in_with_face():
    # 3. 导入模块，初始化变量
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    recognizer_create = cv2.face.LBPHFaceRecognizer_create()
    recognizer_create.read('face_model.yml')  # 读取训练好的模型
    flag = 0  # 标记次数

    ID = 'Unkonw'
    font = cv2.FONT_HERSHEY_SIMPLEX  # 定义字体，使用opencv中的FONT_HERSHEY_SIMPLEX字体

    # 4. 导入应到学生名单

    # 5.识别签到
    capture = cv2.VideoCapture(0)  # 打开摄像头

    while capture.isOpened():  # 当打开摄像头的时候
        kk = cv2.waitKey(1)  # 等待键盘的输入
        _, frame = capture.read()  # 读取摄像头内容
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # 将读取到的RGB图像转换为灰度图像
        faces = classifier.detectMultiScale(gray, 1.3, 5)  # 让classifier判断人脸，detectMultiScale函数可以检测出图像中的人脸
        if len(faces) != 0:  # 如果能找到人脸
            # 框选人脸
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)  # 用矩形框框出人脸，xy为左上角的坐标，w为宽，h为高
                roi_face = gray[y:y + h, x:x + w]
                label, conf = recognizer_create.predict(roi_face)  # 预测出的学号和可信度
                # print(label,conf)

                if conf < 60:
                    flag+=1;

        cv2.putText(frame, 'press "esc" to quit ', (10, 20), font, 0.8, (0, 255, 255), 2)  # 在窗口上添加文字，参数依次表示：图像、要添加的文字、文字的位置、字体、字体大小、颜色、粗细
        cv2.imshow("picture from a cammre", frame)  # 打开窗口的名称
        if flag > 5:
            capture.release()  # 释放变量
            cv2.destroyAllWindows()  # 检查有无打开窗口，有的话关掉
            return True
        if kk == 27:  # 如果退出
            print('程序被终止，请重新签到！')
            break

    # 6.退出程序
    capture.release()  # 释放变量
    cv2.destroyAllWindows()  # 检查有无打开窗口，有的话关掉