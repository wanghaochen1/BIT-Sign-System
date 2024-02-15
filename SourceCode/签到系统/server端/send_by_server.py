import json
#发送登录信息
def send_login_information(s,flag):
    data = {
        'usage': 'login',
        'result': flag
    }
    json_str = json.dumps(data)
    s.sendall(json_str.encode())
    print("\n发送登录结果\n")

#发送签到信息
def send_sign_in_information(s,flag):
    data = {
        'usage': 'sign_in',
        'result': flag
    }
    json_str = json.dumps(data)
    s.sendall(json_str.encode())
    print("\n发送签到结果\n")

def send_change_face_information(s,flag):
    data = {
        'usage': 'change_face',
        'result': flag
    }
    json_str = json.dumps(data)
    s.sendall(json_str.encode())
    print("\n发送更换人脸请求结果\n")

def send_sign_out_information(s,flag):
    data = {
        'usage': 'sign_out',
        'result': flag
    }
    json_str = json.dumps(data)
    s.sendall(json_str.encode())
    print("\n发送签退结果\n")

def send_user_image(s,time):
    data = {
        'usage': 'user_image',
        'result': time
    }
    json_str = json.dumps(data)
    s.sendall(json_str.encode())
    print("\n发送用户画像结果\n")   