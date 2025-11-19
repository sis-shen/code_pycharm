import numpy as np

# 给定数据
data = np.array([
    [1, 2, 3, 20],
    [2, 3, 3, 25],
    [3, 2, 2, 21],
    [4, 2, 3, 28],
    [2, 3, 2, 22],
    [1, 2, 4, 23],
    [3, 3, 2, 25],
    [4, 4, 2, 29],
    [5, 5, 4, 43]
])

# 提取X和y
X = data[:, :3]  # 前三列为X
y = data[:, 3]  # 最后一列为y

# 标准方程法 (正规方程法)
X_bias = np.c_[np.ones(X.shape[0]), X]  # 加入偏置项
theta = np.linalg.inv(X_bias.T @ X_bias) @ X_bias.T @ y  # 正规方程


# 预测函数
def predict_closure(X_values, theta):
    X_values_bias = np.c_[np.ones(len(X_values)), X_values]
    return X_values_bias @ theta


# 预测x1=3, x2=3, x3=3时的y值
x_predict = np.array([[3, 3, 3]])
y_predict_closure = predict_closure(x_predict, theta)

print("标准方程法预测结果:")
print(f"当x1=3, x2=3, x3=3时，y的预测值为：{y_predict_closure[0]}")


# 梯度下降法
def gradient_descent(X, y, theta, alpha, iterations):
    m = len(y)
    X_bias = np.c_[np.ones(m), X]

    for i in range(iterations):
        predictions = X_bias @ theta
        errors = predictions - y
        gradients = (2 / m) * X_bias.T @ errors
        theta -= alpha * gradients
    return theta


# 初始化theta和学习率
theta_init = np.zeros(4)  # 3个属性加一个偏置项
alpha = 0.01
iterations = 1000

# 使用梯度下降法拟合模型
theta_gd = gradient_descent(X, y, theta_init, alpha, iterations)

# 预测梯度下降法的结果
y_predict_gd = predict_closure(x_predict, theta_gd)

print("\n梯度下降法预测结果:")
print(f"当x1=3, x2=3, x3=3时，y的预测值为：{y_predict_gd[0]}")
