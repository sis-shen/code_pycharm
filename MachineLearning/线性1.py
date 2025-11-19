import numpy as np
import matplotlib.pyplot as plt

# 给定的数据
data = np.array([[1, 9], [1.1, 10.5], [2, 18], [3, 28], [3.2, 30], [4, 37], [5, 48], [1.2, 10]])

# 提取x和y
X = data[:, 0]
y = data[:, 1]

# 一元线性回归 闭式解
X_bias = np.c_[np.ones(X.shape[0]), X]  # 加入偏置项
theta = np.linalg.inv(X_bias.T @ X_bias) @ X_bias.T @ y  # 正规方程


# 用闭式解的theta进行预测
def predict_closure(x_values, theta):
    X_values_bias = np.c_[np.ones(len(x_values)), x_values]
    return X_values_bias @ theta


# 预测x=3.5和x=4时的y值
x_predict = np.array([3.5, 4])
y_predict_closure = predict_closure(x_predict, theta)

print("闭式解预测结果:")
print(f"当x=3.5时，y={y_predict_closure[0]}")
print(f"当x=4时，y={y_predict_closure[1]}")


# 一元线性回归 梯度下降法
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
theta_init = np.zeros(2)
alpha = 0.01
iterations = 1000

# 使用梯度下降法拟合模型
theta_gd = gradient_descent(X, y, theta_init, alpha, iterations)

# 用梯度下降法的theta进行预测
y_predict_gd = predict_closure(x_predict, theta_gd)

print("\n梯度下降预测结果:")
print(f"当x=3.5时，y={y_predict_gd[0]}")
print(f"当x=4时，y={y_predict_gd[1]}")

# 计算误差
error_closure = np.mean((y_predict_closure - y_predict_gd) ** 2)
print(f"\n两者误差平方和(MSE): {error_closure}")
