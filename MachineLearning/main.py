import numpy as np

# 数据准备
data = np.array([
    [1.0, 9.0],
    [1.1, 10.5],
    [2.0, 18.0],
    [3.0, 28.0],
    [3.2, 30.0],
    [4.0, 37.0],
    [5.0, 48.0],
    [1.2, 10.0]
])
x_data = data[:, 0]
y_data = data[:, 1]


# ================== 闭式解 ==================
def closed_form_solution(x, y):
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.dot(x, y)
    sum_x2 = np.dot(x, x)

    w = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    b = (sum_y - w * sum_x) / n
    return w, b


w_closed, b_closed = closed_form_solution(x_data, y_data)


# 闭式解预测函数
def predict_closed(x):
    return w_closed * x + b_closed


# ================ 梯度下降 ================
def gradient_descent(x, y, lr=0.01, epochs=5000):
    w = 0.0  # 初始斜率
    b = 0.0  # 初始截距
    n = len(x)

    for _ in range(epochs):
        y_pred = w * x + b

        # 计算梯度
        dw = (-2 / n) * np.dot(x, (y - y_pred))
        db = (-2 / n) * np.sum(y - y_pred)

        # 更新参数
        w -= lr * dw
        b -= lr * db

    return w, b


w_gd, b_gd = gradient_descent(x_data, y_data)


# 梯度下降预测函数
def predict_gd(x):
    return w_gd * x + b_gd


# ============ 结果计算与对比 ============
# 计算预测值
x_test = np.array([3.5, 4.0])
closed_pred = predict_closed(x_test)
gd_pred = predict_gd(x_test)

# 计算两种方法的MSE
closed_mse = np.mean((y_data - predict_closed(x_data)) ** 2)
gd_mse = np.mean((y_data - predict_gd(x_data)) ** 2)

# 显示结果
print(f"[闭式解] 参数：w = {w_closed:.4f}, b = {b_closed:.4f}")
print(f"闭式解预测值：x=3.5 → {closed_pred[0]:.2f}, x=4.0 → {closed_pred[1]:.2f}\n")

print(f"[梯度下降] 参数：w = {w_gd:.4f}, b = {b_gd:.4f}")
print(f"梯度下降预测值：x=3.5 → {gd_pred[0]:.2f}, x=4.0 → {gd_pred[1]:.2f}\n")

print(f"闭式解训练MSE：{closed_mse:.4f}")
print(f"梯度下降训练MSE：{gd_mse:.4f}")
print(f"参数差异：Δw = {abs(w_closed - w_gd):.5f}, Δb = {abs(b_closed - b_gd):.5f}")
