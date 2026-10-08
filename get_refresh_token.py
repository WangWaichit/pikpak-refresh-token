#!/usr/bin/env python3
"""
PikPak Refresh Token 获取工具

通过 PikPak 用户名密码登录，拿到 refresh_token，
方便填入 .env 的 PIKPAK_REFRESH_TOKEN=...

用法：
    python3 get_refresh_token.py
    # 然后按提示输入邮箱和密码

    或命令行直接传参：
    python3 get_refresh_token.py --user you@example.com --pass yourpassword

    也支持环境变量：
    PIKPAK_USER=you@example.com PIKPAK_PASS=yourpassword python3 get_refresh_token.py
"""

import argparse
import getpass
import json
import os
import sys

import requests

# ---- PikPak 官方常量 ---- #
PK_CLIENT_ID = "YNxT9w7GMdWvEOKa"
PK_CLIENT_SECRET = "dbw2OtmVEeuUvIptb1Coyg"
PK_CLIENT_VERSION = "1.47.1"
PK_PACKAGE = "com.pikcloud.pikpak"
PK_USER_HOST = "https://user.mypikpak.com"


def login(username: str, password: str) -> dict:
    """用用户名密码登录 PikPak，返回完整 token dict。"""
    url = f"{PK_USER_HOST}/v1/auth/signin"
    data = {
        "client_id": PK_CLIENT_ID,
        "client_secret": PK_CLIENT_SECRET,
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    headers = {
        "User-Agent": f"ANDROID-{PK_PACKAGE}/{PK_CLIENT_VERSION}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    print(f"正在登录 {PK_USER_HOST}/v1/auth/signin ...")
    r = requests.post(url, data=data, headers=headers, timeout=30)

    if r.status_code != 200:
        print(f"\n[错误] HTTP {r.status_code}")
        try:
            err = r.json()
            print(json.dumps(err, indent=2, ensure_ascii=False))
        except Exception:
            print(r.text[:500])
        sys.exit(1)

    j = r.json()

    if "error" in j:
        print(f"\n[错误] 登录失败: {j.get('error_description', j['error'])}")
        sys.exit(1)

    if "refresh_token" not in j:
        print("\n[错误] 响应中没有 refresh_token：")
        print(json.dumps(j, indent=2, ensure_ascii=False))
        sys.exit(1)

    return j


def main():
    parser = argparse.ArgumentParser(
        description="PikPak Refresh Token 获取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 get_refresh_token.py
  python3 get_refresh_token.py --user you@example.com --pass yourpassword
  PIKPAK_USER=you@example.com PIKPAK_PASS=xxx python3 get_refresh_token.py
        """,
    )
    parser.add_argument("--user", help="PikPak 登录邮箱/用户名")
    parser.add_argument("--pass", dest="password", help="PikPak 登录密码（不建议命令行传，会留在历史记录）")
    args = parser.parse_args()

    username = args.user or os.environ.get("PIKPAK_USER", "")
    if not username:
        username = input("PikPak 邮箱/用户名: ").strip()

    password = args.password or os.environ.get("PIKPAK_PASS", "")
    if not password:
        password = getpass.getpass("PikPak 密码: ")

    if not username or not password:
        print("[错误] 用户名和密码不能为空")
        sys.exit(1)

    token_data = login(username, password)

    access_token = token_data.get("access_token", "")
    refresh_token = token_data.get("refresh_token", "")
    expires_in = token_data.get("expires_in", 0)
    sub = token_data.get("sub", "")

    print("\n" + "=" * 60)
    print("登录成功！")
    print("=" * 60)
    print(f"用户 ID (sub) : {sub}")
    print(f"Access Token 有效期: {expires_in} 秒")
    print("-" * 60)
    print("【你的 Refresh Token】（复制到 PIKPAK_REFRESH_TOKEN= 后面）：")
    print()
    print(refresh_token)
    print("-" * 60)
    print()
    print("完整 access_token（前 50 字符）:")
    print(access_token[:50] + "...")
    print()


if __name__ == "__main__":
    main()
