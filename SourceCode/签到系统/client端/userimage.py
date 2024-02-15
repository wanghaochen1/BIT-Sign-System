import datetime
import torch
import torch.nn as nn
from datetime import datetime
from datetime import datetime, timedelta
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
def count(time):
    morning_in=0; 
    morning_out=0; 
    night_in=0; 
    night_out=0; 
    for row in time:
        for date in row:
            if date.hour<12 :
                morning_in+=1
            elif date.hour<12 :
                morning_out+=1
            elif date.hour>=12 :
                night_in+=1
            elif date.hour>=12 :
                night_out+=1
    print(night_in+night_out+morning_in+morning_out)
    return morning_in,morning_out,night_in,night_out

def class_time(time):
    time_diffs = []
    for row in time:
        if len(row) >= 2:
            diff = abs(row[1] - row[0])
            time_diffs.append(diff)

    total_diff = sum(time_diffs, timedelta())  # 求和
    return total_diff

def preprocess_time_data(time_data):
    # 将时间转换为一天中的分钟数
    # 将时间转换为一天中的分钟数
    time_data_minutes = [[time.minute + time.hour * 60 for time in row] for row in time_data]

    # 将数据标准化
    min_value = min(min(row) for row in time_data_minutes)
    max_value = max(max(row) for row in time_data_minutes)
    if max_value == min_value:
        time_data_normalized = [[0 for value in row] for row in time_data_minutes]
    else:
        time_data_normalized = [[(value - min_value) / (max_value - min_value) for value in row] for row in time_data_minutes]

    return time_data_normalized

class MyModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MyModel, self).__init__()
        self.hidden_layer_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size)
        self.linear = nn.Linear(hidden_size, output_size)
        self.hidden_cell = (torch.zeros(1, 1, self.hidden_layer_size),
                            torch.zeros(1, 1, self.hidden_layer_size))

    def forward(self, x):
        x, self.hidden_cell = self.lstm(x, self.hidden_cell)
        x = self.linear(x)
        return x


def predict_next_checkin(time_data):
    def train_lstm_model(time_data, epochs=150):
        try:
            torch.autograd.set_detect_anomaly(False)
            time_data = preprocess_time_data(time_data)
            train_data = torch.Tensor(time_data[:-1])

            # 设置 LSTM 参数
            input_size = 2  # 输入数据的特征数量
            hidden_size = 50  # 隐藏层的大小
            output_size = 2  # 输出数据的特征数量

            # 创建并训练模型
            model = MyModel(input_size, hidden_size, output_size)
            loss_function = nn.MSELoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

            # LSTM 需要输入的形状为 (序列长度, 批大小, 特征数量)
            train_data = train_data.view(len(train_data), 1, -1)

            for i in range(epochs):
                y_pred = model(train_data)

                single_loss = loss_function(y_pred, train_data)
                optimizer.zero_grad()  # 清除旧的梯度
                single_loss.backward(retain_graph=True)
                optimizer.step()
        except Exception as e:
    # 如果发生了 RuntimeError 异常，代表训练数据量过少，需要
            print('需要多进行签到才能进行预测')
            return True
        # 数据预处理
        return model
    if train_lstm_model(time_data):
        return datetime.now()
    model=train_lstm_model(time_data)
    time_data = preprocess_time_data(time_data)
    test_data = torch.Tensor(time_data[-1:])
    # 使用模型进行预测
    with torch.no_grad():
        model.hidden_cell = (torch.zeros(1, 1, model.hidden_layer_size),
                             torch.zeros(1, 1, model.hidden_layer_size))
        prediction = model(test_data)

    # 将预测结果转换回时间格式
    hours = prediction.item() // 60
    minutes = prediction.item() % 60
    next_checkin = datetime.time(int(hours), int(minutes))
    return next_checkin
def user_fame(time):
    if class_time(time) > timedelta(days=5):
        return str("学霸")
    if class_time(time) > timedelta(days=3):
        return str("实力股")
    else:
        return str("潜力股")