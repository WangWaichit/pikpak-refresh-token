#!/usr/bin/env python3
"""PikPak Refresh Token 一键获取工具"""

import getpass
import hashlib
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

PK_SALTS = [
    "Gez0T9ijiI9WCeTsKSg3SMlx",
    "zQdbalsolyb1R/",
    "ftOjr52zt51JD68C3s",
    "yeOBMH0JkbQdEFNNwQ0RI9T3wU/v",
    "BRJrQZiTQ65WtMvwO",
    "je8fqxKPdQVJiy1DM6Bc9Nb1",
    "niV",
    "9hFCW2R1",
    "sHKHpe2i96",
    "p7c5E6AcXQ/IJUuAEC9W6",
    "",
    "aRv9hjc9P+Pbn+u3krN6",
    "BzStcgE8qVdqjEH16l4",
    "SqgeZvL5j9zoHP95xWHt",
    "zVof5yaJkPe3VFpadPof",
]


def _captcha_sign(device_id: str, ts_ms: str) -> str:
    s = PK_CLIENT_ID + PK_CLIENT_VERSION + PK_PACKAGE + device_id + ts_ms
    for salt in PK_SALTS:
        s = hashlib.md5((s + salt).encode()).hexdigest()
    return f"1.{s}"


def http_post(url, data_dict, extra_headers=None):
    """POST form-urlencoded，返回 (json_dict, error_str)"""
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
            return json.loads(raw), f"HTTP {e.code}: {raw[:300]}"
        except Exception:
            return None, f"HTTP {e.code}: {raw[:300]}"
    except Exception as e:
        return None, str(e)


def captcha_init(device_id: str, action: str) -> str:
    ts = str(int(time.time() * 1000))
    meta_str = json.dumps({
        "captcha_sign": _captcha_sign(device_id, ts),
        "client_version": PK_CLIENT_VERSION,
        "package_name": PK_PACKAGE,
        "timestamp": ts,
    })
    j, err = http_post(f"{PK_USER_HOST}/v1/shield/captcha/init", {
        "client_id": PK_CLIENT_ID,
        "action": action,
        "device_id": device_id,
        "meta": meta_str,
    })
    if err:
        print(f"  [debug] captcha_init 失败: {err}")
        return ""
    token = j.get("captcha_token", "")
    if token:
        print(f"  [debug] captcha_token 获取成功: {token[:20]}...")
    else:
        print(f"  [debug] captcha_init 响应: {json.dumps(j, ensure_ascii=False)[:200]}")
    return token


def main():
    print("=" * 40)
    print("  PikPak Refresh Token 获取工具")
    print("=" * 40)

    device_id = hashlib.md5(uuid.uuid4().hex.encode()).hexdigest()[:32]

    while True:
        username = input("账号（邮箱）: ").strip()
        password = getpass.getpass("密码: ")

        if not username or not password:
            print("账号密码不能为空，请重新输入\n")
            continue

        print("登录中...")

        # 先初始化 captcha
        captcha_token = captcha_init(device_id, "POST:/v1/auth/signin")

        headers = {"X-Device-Id": device_id}
        if captcha_token:
            headers["X-Captcha-Token"] = captcha_token

        j, err = http_post(f"{PK_USER_HOST}/v1/auth/signin", {
            "client_id": PK_CLIENT_ID,
            "client_secret": PK_CLIENT_SECRET,
            "grant_type": "password",
            "username": username,
            "password": password,
        }, extra_headers=headers)

        if err:
            print(f"登录失败: {err}")
            print("请重新输入\n")
            continue

        if "error" in j:
            print(f"登录失败: {j.get('error_description', j['error'])}")
            print(f"  [debug] 完整响应: {json.dumps(j, ensure_ascii=False)[:300]}")
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
