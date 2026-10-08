# PikPak Refresh Token

一键获取 PikPak refresh_token。

## 一键使用

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/WangWaichit/pikpak-refresh-token/main/refresh.sh)"
```

按提示输入 PikPak 邮箱和密码，直接输出 refresh_token。

## 本地使用

```bash
git clone https://github.com/WangWaichit/pikpak-refresh-token.git
cd pikpak-refresh-token
bash refresh.sh
```

零依赖，纯 Python 标准库，Python 3.6+ 即可。

## 示例

```
========================================
  PikPak Refresh Token 获取工具
========================================
账号（邮箱）: you@example.com
密码: ********

登录中...

登录成功！
----------------------------------------
Refresh Token:

os.8UWB0v-ZZmbG5o8Es7t3g50q4dZWR3vBcE06Ewgvnw6dTTLAYFuX236RkBBy
----------------------------------------
```
