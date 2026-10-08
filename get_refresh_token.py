#!/usr/bin/env python3
"""PikPak Refresh Token 一键获取工具"""

import getpass
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import uuid

PK_CLIENT_ID = "YNxT9w7GMdWvEOKa"
PK_CLIENT_SECRET = "dbw2OtmVEeuUvIptb1Coyg"
PK_CLIENT_VERSION = "1.47.1"
PK_PACKAGE = "com.pikcloud.pikpak"
PK_USER_HOST = "https://user.mypikpak.com"


def http_post_json(url, payload, extra_headers=None):
    """POST application/json"""
    body = json.dumps(payload).encode()
    headers = {
        "User-Agent": f"ANDROID-{PK_PACKAGE}/{PK_CLIENT_VERSION}",
        "Content-Type": "application/json; charset=utf-8",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read()), None
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return json.loads(raw), f"HTTP {e.code}"
        except Exception:
            return None, f"HTTP {e.code}: {raw[:300]}"
    except Exception as e:
        return None, str(e)


def http_post_form(url, data_dict, extra_headers=None):
    """POST form-urlencoded"""
    body = urllib.parse.urlencode(data_dict).encode()
    headers = {
        "User-Agent": f"ANDROID-{PK_PACKAGE}/{PK_CLIENT_VERSION}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read()), None
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return json.loads(raw), f"HTTP {e.code}"
        except Exception:
            return None, f"HTTP {e.code}: {raw[:300]}"
    except Exception as e:
        return None, str(e)


def captcha_init(device_id, action, meta):
    """初始化验证码，返回 captcha_token"""
    payload = {
        "client_id": PK_CLIENT_ID,
        "action": action,
        "device_id": device_id,
        "meta": meta,
    }
    j, err = http_post_json(f"{PK_USER_HOST}/v1/shield/captcha/init", payload)
    if err:
        return ""
    return j.get("captcha_token", "")


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

        device_id = uuid.uuid4().hex

        # 1. 先初始化 captcha，meta 传邮箱
        captcha_token = captcha_init(
            device_id,
            f"POST:{PK_USER_HOST}/v1/auth/signin",
            {"email": username},
        )

        # 2. 登录，captcha_token 放在 body 里
        login_data = {
            "client_id": PK_CLIENT_ID,
            "client_secret": PK_CLIENT_SECRET,
            "username": username,
            "password": password,
            "captcha_token": captcha_token,
        }
        j, err = http_post_form(f"{PK_USER_HOST}/v1/auth/signin", login_data)

        if err:
            print(f"登录失败: {err}")
            if j:
                print(f"  {j.get('error_description', j)}")
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
