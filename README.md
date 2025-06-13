# NetEase-CloudMusic-reverse
# 网易云音乐API加密机制研究

> **法律声明**：本项目仅用于密码学技术研究，所有代码均为教学演示用途。请勿用于实际请求网易云音乐API，遵守[网易云音乐用户协议](https://music.163.com/html/web2/service.html)。

## 研究内容
通过逆向工程分析网易云音乐歌单Web端的API请求加密机制，重点研究：
- 双重AES加密流程
- RSA密钥交换实现
- 动态参数生成策略

## 技术架构
```mermaid
graph LR
    A[请求参数] --> B(AES-128加密)
    B --> C(随机密钥生成)
    C --> D(RSA加密)
    D --> E{网络传输}
    E --> F[网易云服务器]
