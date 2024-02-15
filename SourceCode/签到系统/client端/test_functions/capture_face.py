# 第一步：采集人脸图像

# 1.导入第三方库
import cv2
import os
import xlrd

# 2.初始化变量
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

# 3.输入学号
student_ID = 2021520542

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
