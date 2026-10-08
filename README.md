# PikPak Refresh Token

通过 PikPak 用户名密码登录，直接获取 refresh_token 的命令行小工具。

## 安装

```bash
git clone https://github.com/WangWaichit/pikpak-refresh-token.git
cd pikpak-refresh-token
pip3 install requests
```

## 用法

### 交互式（推荐）

```bash
python3 get_refresh_token.py
```

按提示输入 PikPak 邮箱和密码，密码输入时不显示。

### 命令行传参

```bash
python3 get_refresh_token.py --user you@example.com --pass yourpassword
```

> 不建议在命令行直接传密码，会留在 shell 历史记录里。

### 环境变量

```bash
export PIKPAK_USER=you@example.com
export PIKPAK_PASS=yourpassword
python3 get_refresh_token.py
```

## 输出示例

```
============================================================
登录成功！
============================================================
用户 ID (sub) : Zsa0L-A6udTdD_4K
Access Token 有效期: 7200 秒
------------------------------------------------------------
【你的 Refresh Token】（复制到 PIKPAK_REFRESH_TOKEN= 后面）：

os.8UWB0v-ZZmbG5o8Es7t3g50q4dZWR3vBcE06Ewgvnw6dTTLAYFuX236RkBBy
------------------------------------------------------------
```

## 说明

- 模拟 PikPak Android 客户端登录（client_id: `YNxT9w7GMdWvEOKa`）
- 只调用 PikPak 官方认证接口 `user.mypikpak.com/v1/auth/signin`
- refresh_token 长期有效，access_token 每 2 小时过期（用 refresh_token 可自动换新）
- 适用于 PikPak 网页版 / 客户端注册的正式邮箱账号

## 常见问题

**登录失败怎么办？**
- 确认邮箱密码正确
- 如果开启了两步验证，需要用独立密码
- 频繁登录会触发风控，等几分钟再试

**refresh_token 会过期吗？**
- 不会主动过期，但修改密码或手动退出登录会使其失效
- 部分 API 调用会轮换 refresh_token（拿到新的要替换旧的）
