class CaesarCipher:
    def __init__(self, key):
        self.key = key  # 密钥，表示字母偏移量

    def encrypt(self, plaintext):
        """加密函数"""
        ciphertext = ""
        for char in plaintext:
            if char.isalpha():  # 只加密字母
                # 处理大写字母
                if char.isupper():
                    cipher_char = chr((ord(char) - ord('A') + self.key) % 26 + ord('A'))
                # 处理小写字母
                else:
                    cipher_char = chr((ord(char) - ord('a') + self.key) % 26 + ord('a'))
                ciphertext += cipher_char
            else:
                # 保持非字母字符不变
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext):
        """解密函数"""
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():  # 只解密字母
                # 处理大写字母
                if char.isupper():
                    plain_char = chr((ord(char) - ord('A') - self.key) % 26 + ord('A'))
                # 处理小写字母
                else:
                    plain_char = chr((ord(char) - ord('a') - self.key) % 26 + ord('a'))
                plaintext += plain_char
            else:
                # 保持非字母字符不变
                plaintext += char
        return plaintext


# 示例使用
if __name__ == "__main__":
    key = 3  # 密钥，可以选择任何整数
    cipher = CaesarCipher(key)

    # 加密消息
    message = "hello there,this is a msg"
    encrypted_message = cipher.encrypt(message)
    print("密文:", encrypted_message)

    # 解密消息
    decrypted_message = cipher.decrypt(encrypted_message)
    print("明文:", decrypted_message)
