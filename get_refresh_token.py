#!/usr/bin/env python3
"""PikPak Refresh Token 一键获取工具"""

import getpass
import json
import sys
import urllib.request
import urllib.parse
import urllib.error

PK_CLIENT_ID = "YNxT9w7GMdWvEOKa"
PK_CLIENT_SECRET = "dbw2OtmVEeuUvIptb1Coyg"
PK_CLIENT_VERSION = "1.47.1"
PK_PACKAGE = "com.pikcloud.pikpak"
PK_USER_HOST = "https://user.mypikpak.com"


def do_login(username, password):
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
            return json.loads(resp.read()), None
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body)
            return None, err.get("error_description", err.get("error", f"HTTP {e.code}"))
        except Exception:
            return None, f"HTTP {e.code}: {body[:200]}"
    except Exception as e:
        return None, str(e)


def main():
    print("=" * 40)
    print("  PikPak Refresh Token 获取工具")
    print("=" * 40)

    while True:
        username = input("账号（邮箱）: ").strip()
        password = getpass.getpass("密码: ")

        if not username or not password:
            print("账号密码不能为空，请重新输入\n")
            continue

        print("登录中...")

        j, err = do_login(username, password)

        if err:
            print(f"登录失败: {err}")
            print("请重新输入\n")
            continue

        if "error" in j:
            print(f"登录失败: {j.get('error_description', j['error'])}")
            print("请重新输入\n")
            continue

        refresh_token = j.get("refresh_token", "")
        if not refresh_token:
            print("未获取到 refresh_token，响应:")
            print(json.dumps(j, indent=2, ensure_ascii=False))
            sys.exit(1)

        print("\n登录成功！")
        print("-" * 40)
        print(f"Refresh Token:\n\n{refresh_token}")
        print("-" * 40)
        break


if __name__ == "__main__":
    main()
