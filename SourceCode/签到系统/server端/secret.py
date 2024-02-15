import hashlib
import pickle

def hash_password(password):
    # 创建哈希对象
    hasher = hashlib.sha256()
    # 对密码进行哈希处理
    hasher.update(password.encode('utf-8'))
    hashed_password = hasher.hexdigest()
    return hashed_password


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