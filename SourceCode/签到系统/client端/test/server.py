import socket
import json

# 创建socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP地址和端口号
server_address = ('localhost', 8888)
server_socket.bind(server_address)

# 监听连接
server_socket.listen(1)
print('服务器已启动，等待客户端连接...')

while True:
    # 等待客户端连接
    client_socket, client_address = server_socket.accept()
    print('客户端已连接:', client_address)

    try:
        # 接收数据
        data = client_socket.recv(1024)
        if data:
            # 解析JSON数据
            json_data = json.loads(data.decode('utf-8'))
            print('接收到的JSON数据:', json_data)

            # 处理数据
            # TODO: 在这里添加你的处理逻辑

            # 发送响应
            response = {'status': 'success'}
            response_data = json.dumps(response).encode('utf-8')
            client_socket.sendall(response_data)
            print('响应已发送:', response)

    except Exception as e:
        print('发生异常:', str(e))

    finally:
        # 关闭客户端连接
        client_socket.close()
        print('客户端连接已关闭')

