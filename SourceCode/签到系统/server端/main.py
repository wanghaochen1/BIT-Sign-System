import socket
import read_client
import GUI
from db import *
import pop
import subprocess
import secret

GUI.server_window()
print("服务端启动成功")
# Create a socket object
subprocess.Popen(['python', 'teacher.py'])
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('127.0.0.1', 12345)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(50)

print('Server is listening on {}:{}'.format(*server_address))
con=sql_connection()
create_table_student(con)
insert_table_student(con,"student",1120210529,"王昊宸","123456","./face/1.jpg")
insert_table_student(con,"student",1120210530,"王昊宸-2","123456","./face/2.jpg")
create_table_qd(con)



while True:
    # Wait for a client to connect
    print('\n等待学生连接中...\n')
    client_socket, client_address = server_socket.accept()
    pop.create_popup("有学生连接")
    print('客户端 connected from {}:{}'.format(*client_address))
    
    try:
        while True:
            new_socket, client_address = server_socket.accept()
            server_queue = queue.Queue()
            socket_queue_dict[new_socket] = server_queue
            client_handler = threading.Thread(target= read_client.read(con,client_socket,data.decode()), args=(new_socket, client_address))
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break
            print("\n收到来自客户端的消息,正在解析\n")
            client_handler.daemon = True
    except Exception as e:
        pop.create_popup("连接中断")
        print(f"An error occurred: {e}")
    finally:
        # Close the client socket
        client_socket.close()