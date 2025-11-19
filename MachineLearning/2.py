def generate_shamir_shares():
    # 秘密值
    secret = 60
    # 模数（必须为质数且大于所有输入值和秘密）
    prime = 73
    # 选择的随机系数 a1, a2（例子中固定为1）
    a1 = 1
    a2 = 1
    # 参与者的输入点
    x_coordinates = [3, 5, 7, 8]

    # 计算秘密份额
    shares = []
    for x in x_coordinates:
        y = (a2 * x ** 2 + a1 * x + secret) % prime
        shares.append((x, y))

    return shares


# 生成并输出结果
if __name__ == "__main__":
    secret_shares = generate_shamir_shares()
    print("(3,4)门限方案的秘密份额：")
    for share in secret_shares:
        print(f"({share[0]}, {share[1]})")