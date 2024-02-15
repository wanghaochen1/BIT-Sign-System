import socket
import json

def receive_json_data(host, port):
    # 创建socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 连接服务器
        client_socket.connect((host, port))
        
        # 接收数据
        data = client_socket.recv(1024)
        
        # 解析JSON数据
        json_data = json.loads(data.decode())
        
        return json_data
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        
    finally:
        # 关闭socket连接
        client_socket.close()

# 设置服务器的IP地址和端口号
server_host = '127.0.0.1'
server_port = 12345

# 调用函数接收JSON数据
received_data = receive_json_data(server_host, server_port)

# 打印接收到的数据
print(received_data)
