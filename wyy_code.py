import json
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

# 定义常量
bi_radix_bits = 16
bits_per_digit = bi_radix_bits
bi_half_radix = 32768
max_digit_val = 65535
high_bit_masks = [0,32768,49152,57344,61440,63488,64512,65024,65280,65408,65472,65504,65520,65528,65532,65534,65535]
bi_radix = 65536
bi_radix_squared = 4294967296
low_bit_masks = [0,1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535]
hex_to_char = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

# 示例数据
i1x = {
    "hlpretag": "<span class=\"s-fc7\">",
    "hlposttag": "</span>",
    "s": "林俊杰",
    "type": "1",
    "offset": "30",
    "total": "false",
    "limit": "30",
    "csrf_token": "1eab3f57815d42c05e8923a194848797"
}

g_3 = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'

def create_random_str(length):
    """生成指定长度的随机字符串"""
    base_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_str = ""
    for i in range(length):
        random_str += random.choice(base_str)
    return random_str

def aes_encrypt(text, key):
    """AES加密"""
    # 将字符串转换为字节
    text = text.encode('utf-8')
    key = key.encode('utf-8')
    iv = b"0102030405060708"
    
    # 创建加密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # 加密
    encrypted = cipher.encrypt(pad(text, AES.block_size))
    
    # 转换为base64
    return base64.b64encode(encrypted).decode('utf-8')

def rsa_encrypt(text, pubkey, modulus):
    """RSA加密"""
    # 将字符串转换为数字
    text = text[::-1]  # 反转字符串
    rs = int(text.encode('utf-8').hex(), 16) ** int(pubkey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)

def encrypted_request(text, pubkey, modulus, nonce):
    """加密请求数据"""
    # 第一次AES加密
    text = json.dumps(text)
    enc_text = aes_encrypt(text, nonce)
    
    # 第二次AES加密
    rand_str = create_random_str(16)
    enc_text = aes_encrypt(enc_text, rand_str)
    
    # RSA加密
    enc_sec_key = rsa_encrypt(rand_str, pubkey, modulus)
    
    return {
        'encText': enc_text,
        'encSecKey': enc_sec_key
    }

# 使用示例
if __name__ == '__main__':
    result = encrypted_request(i1x, '010001', g_3, '0CoJUm6Qyw8W8jud')
    print(result)