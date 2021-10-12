# -*- coding: utf-8 -*-
import json
import os

import requests

from dailycheckin import CheckIn


class CSDN(CheckIn):
    name = "CSDN"

    def __init__(self, check_item):
        self.check_item = check_item
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74",
        }

    def sign(self, cookies):
        response = requests.get(
            url="https://me.csdn.net/api/LuckyDraw_v2/signIn", headers=self.headers, cookies=cookies
        ).json()
        if response.get("code") == 200:
            msg = response.get("data").get("msg")
        else:
            msg = "签到失败"
            print(response)
        return msg

    def draw(self, cookies):
        response = requests.get(
            url="https://me.csdn.net/api/LuckyDraw_v2/goodluck", headers=self.headers, cookies=cookies
        ).json()
        if response.get("code") == 200:
            msg = response.get("data").get("msg")
        else:
            msg = "抽奖失败"
        return msg

    def main(self):
        csdn_cookie = {item.split("=")[0]: item.split("=")[1] for item in self.check_item.get("cookie").split("; ")}
        try:
            user_name = csdn_cookie.get("UserName", "")
        except Exception as e:
            print(f"获取账号信息失败: {e}")
            user_name = "未获取到账号信息"
        sign_msg = self.sign(cookies=csdn_cookie)
        draw_msg = self.draw(cookies=csdn_cookie)
        msg = [
            {"name": "帐号信息", "value": user_name},
            {"name": "签到信息", "value": sign_msg},
            {"name": "抽奖结果", "value": draw_msg},
        ]
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8") as f:
        datas = json.loads(f.read())
    _check_item = datas.get("CSDN", [])[0]
    print(CSDN(check_item=_check_item).main())
