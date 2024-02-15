import json
import datetime
from datetime import datetime
def identify_result(s):
    try:
        receivedata = s.recv(10240)
        json_str = receivedata.decode('utf-8')
        data = json.loads(json_str)
    except json.JSONDecodeError:
        print('Failed to decode JSON data')
        return False
    #如果是登陆信息：
    if data['usage'] == 'login':
        return data['result']
    #如果是签到信息：
    if data['usage'] == 'sign_in':
        return data['result']
    if data['usage'] == 'change_face':
        return data['result']
    if data['usage'] == 'sign_out':
        return data['result']
    if data['usage'] == 'user_image':
        time_str=data['result']
        dates = []  # 定义 dates
        for row in time_str:
            date_row = []
            for date_string in row:
                date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")
                date_row.append(date)
            dates.append(date_row)
        return dates