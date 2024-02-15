import json

#client端的json格式：(client端发出的信号)用户端
#data={
#    'usage':'',
#    'stu_num':'',
#    'sign_time':''}

#发送签到信息
def sign_in(stu_num,sign_time,s):
    data={
        'usage':'sign_in',
        'stu_num':stu_num,
        'sign_time':sign_time}
    json_str=json.dumps(data)
    s.sendall(json_str.encode())
    print("已发送签到信息")
    return 
#发送更换人脸信息
def change_face(s,stu_num):
    data={
        'usage':'change_face',
        'stu_num' : stu_num}
    json_str=json.dumps(data)
    s.sendall(json_str.encode())
    print("已发送更换人脸信息")
    return

#发送登陆信息
def login(stu_num,stu_password,s):
    data={
        'usage':'login',
        'stu_num':stu_num,
        'stu_password':stu_password}
    json_str=json.dumps(data)
    s.sendall(json_str.encode())
    return
#发送签退信息
def sign_out(stu_num,s):
    data={
        'usage':'sign_out',
        'stu_num':stu_num,}
    json_str=json.dumps(data)
    s.sendall(json_str.encode())
    return

def user_image(s,stu_num):
    data={
        'usage':'user_image',
        'stu_num':stu_num,}
    json_str=json.dumps(data)
    s.sendall(json_str.encode())
    return

    
