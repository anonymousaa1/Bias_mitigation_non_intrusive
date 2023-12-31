import os
import torch

import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt


# 自定义损失函数

# 1. 继承nn.Mdule
class My_loss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x, y):
        print("-->(x - y)", (x - y))
        print("-->loss", torch.mean(torch.pow((x - y), 2)))
        score = torch.mean(torch.pow((x - y), 2))
        # score = score.clone().detach().requires_grad_(True)
        return score

# 2. 直接定义函数 ， 不需要维护参数，梯度等信息
# 注意所有的数学操作需要使用tensor完成。
def my_mse_loss(x, y):
    return torch.mean(torch.pow((x - y), 2))

# 3, 如果使用 numpy/scipy的操作  可能使用nn.autograd.function来计算了
# 要实现forward和backward函数

# Hyper-parameters 定义迭代次数， 学习率以及模型形状的超参数
input_size = 1
output_size = 1
num_epochs = 60
learning_rate = 0.001

# Toy dataset  1. 准备数据集
x_train = np.array([[3.3], [4.4], [5.5], [6.71], [6.93], [4.168],
                    [9.779], [6.182], [7.59], [2.167], [7.042],
                    [10.791], [5.313], [7.997], [3.1]], dtype=np.float32)

y_train = np.array([[1.7], [2.76], [2.09], [3.19], [1.694], [1.573],
                    [3.366], [2.596], [2.53], [1.221], [2.827],
                    [3.465], [1.65], [2.904], [1.3]], dtype=np.float32)

# Linear regression model  2. 定义网络结构 y=w*x+b 其中w的size [1,1], b的size[1,]
model = nn.Linear(input_size, output_size)
print("-->original grad")
for name, parameters in model.named_parameters():
    print("grad:", name, ':', parameters.grad)

# Loss and optimizer 3.定义损失函数， 使用的是最小平方误差函数
# criterion = nn.MSELoss()
# 自定义函数1
criterion = My_loss()

# 4.定义迭代优化算法， 使用的是随机梯度下降算法
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
loss_dict = []
# Train the model 5. 迭代训练
for epoch in range(num_epochs):
    # Convert numpy arrays to torch tensors  5.1 准备tensor的训练数据和标签
    inputs = torch.from_numpy(x_train)
    targets = torch.from_numpy(y_train)

    # Forward pass  5.2 前向传播计算网络结构的输出结果
    outputs = model(inputs)
    # 5.3 计算损失函数
    # loss = criterion(outputs, targets)

    print("-->outputs", outputs)
    print("-->targets", targets)

    # 1. 自定义函数1
    loss = criterion(outputs, targets)
    # 2. 自定义函数
    # loss = my_mse_loss(outputs, targets)
    # Backward and optimize 5.4 反向传播更新参数
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # 可选 5.5 打印训练信息和保存loss
    loss_dict.append(loss.item())
    if (epoch + 1) % 5 == 0:
        print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch + 1, num_epochs, loss.item()))

    for name, parameters in model.named_parameters():
        print("grad:", name, ':', parameters.grad)

# Plot the graph 画出原y与x的曲线与网络结构拟合后的曲线
predicted = model(torch.from_numpy(x_train)).detach().numpy()
plt.plot(x_train, y_train, 'ro', label='Original data')
plt.plot(x_train, predicted, label='Fitted line')
plt.legend()
plt.show()

# 画loss在迭代过程中的变化情况
plt.plot(loss_dict, label='loss for every epoch')
plt.legend()
plt.savefig("test.png")

