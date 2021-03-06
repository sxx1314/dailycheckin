# -*- coding: utf-8 -*-
import json
import os
from urllib import parse

import requests

from dailycheckin import CheckIn


class WZYD(CheckIn):
    name = "王者营地"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(data):
        response = requests.post(url="https://ssl.kohsocialapp.qq.com:10001/play/h5sign", data=data).json()
        try:
            if response["result"] == 0:
                msg = "签到成功"
            else:
                msg = response["returnMsg"]
        except:
            msg = "请求失败,请检查接口"
        return msg

    def main(self):
        wzyd_data = self.check_item.get("data")
        data = {k: v[0] for k, v in parse.parse_qs(wzyd_data).items()}
        try:
            user_id = data.get("userId", "")
        except Exception as e:
            print(f"获取账号信息失败: {e}")
            user_id = "未获取到账号信息"
        sign_msg = self.sign(data=data)
        msg = [
            {"name": "帐号信息", "value": user_id},
            {"name": "签到信息", "value": sign_msg},
        ]
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8") as f:
        datas = json.loads(f.read())
    _check_item = datas.get("WZYD", [])[0]
    print(WZYD(check_item=_check_item).main())
