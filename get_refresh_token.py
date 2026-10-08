#!/usr/bin/env python3
"""PikPak Refresh Token 一键获取工具"""

import getpass
import json
import sys
import urllib.request
import urllib.parse
import urllib.error

# 从 /dev/tty 读取输入，避免管道 stdin 被占用导致 EOFError
def ask(prompt):
    with open("/dev/tty", "r") as tty:
        print(prompt, end="", flush=True)
        return tty.readline().strip()

PK_CLIENT_ID = "YNxT9w7GMdWvEOKa"
PK_CLIENT_SECRET = "dbw2OtmVEeuUvIptb1Coyg"
PK_CLIENT_VERSION = "1.47.1"
PK_PACKAGE = "com.pikcloud.pikpak"
PK_USER_HOST = "https://user.mypikpak.com"


def main():
    print("=" * 40)
    print("  PikPak Refresh Token 获取工具")
    print("=" * 40)

    username = ask("账号（邮箱）: ")
    password = getpass.getpass("密码: ")

    if not username or not password:
        print("账号密码不能为空")
        sys.exit(1)

    print("\n登录中...")

    data = urllib.parse.urlencode({
        "client_id": PK_CLIENT_ID,
        "client_secret": PK_CLIENT_SECRET,
        "grant_type": "password",
        "username": username,
        "password": password,
    }).encode()

    req = urllib.request.Request(
        f"{PK_USER_HOST}/v1/auth/signin",
        data=data,
        headers={
            "User-Agent": f"ANDROID-{PK_PACKAGE}/{PK_CLIENT_VERSION}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            j = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"\n登录失败 (HTTP {e.code}):")
        try:
            err = json.loads(body)
            print(err.get("error_description", err.get("error", body)))
        except Exception:
            print(body[:300])
        sys.exit(1)

    if "error" in j:
        print(f"\n登录失败: {j.get('error_description', j['error'])}")
        sys.exit(1)

    refresh_token = j.get("refresh_token", "")
    if not refresh_token:
        print("\n未获取到 refresh_token，响应:")
        print(json.dumps(j, indent=2, ensure_ascii=False))
        sys.exit(1)

    print("\n登录成功！")
    print("-" * 40)
    print(f"Refresh Token:\n\n{refresh_token}")
    print("-" * 40)


if __name__ == "__main__":
    main()
