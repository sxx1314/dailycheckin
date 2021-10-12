# -*- coding: utf-8 -*-
import json
import os

import requests
from requests import utils

from dailycheckin import CheckIn


class Smzdm(CheckIn):
    name = "什么值得买"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(session):
        try:
            current = session.get(url="https://zhiyou.smzdm.com/user/info/jsonp_get_current").json()
            if current["checkin"]["has_checkin"]:
                msg = [
                    {"name": "账号信息", "value": current.get("nickname", "")},
                    {"name": "目前积分", "value": current.get("point", "")},
                    {"name": "当前经验", "value": current.get("exp", "")},
                    {"name": "当前金币", "value": current.get("gold", "")},
                    {"name": "碎银子数", "value": current.get("silver", "")},
                    {"name": "当前威望", "value": current.get("prestige", "")},
                    {"name": "当前等级", "value": current.get("level", "")},
                    {"name": "已经签到", "value": f"{current.get('checkin', {}).get('daily_checkin_num', '')} 天"},
                ]
            else:
                response = session.get(url="https://zhiyou.smzdm.com/user/checkin/jsonp_checkin").json().get("data", {})
                msg = [
                    {"name": "账号信息", "value": current.get("nickname", "")},
                    {"name": "目前积分", "value": current.get("point", "")},
                    {"name": "增加积分", "value": current.get("add_point", "")},
                    {"name": "当前经验", "value": current.get("exp", "")},
                    {"name": "当前金币", "value": current.get("gold", "")},
                    {"name": "当前威望", "value": current.get("prestige", "")},
                    {"name": "当前等级", "value": current.get("rank", "")},
                    {"name": "已经签到", "value": f"{response.get('checkin_num', {})} 天"},
                ]
        except Exception as e:
            msg = [
                {"name": "签到信息", "value": "签到失败"},
                {"name": "错误信息", "value": str(e)},
            ]
        return msg

    def main(self):
        smzdm_cookie = {item.split("=")[0]: item.split("=")[1] for item in self.check_item.get("cookie").split("; ")}
        session = requests.session()
        requests.utils.add_dict_to_cookiejar(session.cookies, smzdm_cookie)
        session.headers.update(
            {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Host": "zhiyou.smzdm.com",
                "Referer": "https://www.smzdm.com/",
                "Sec-Fetch-Dest": "script",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            }
        )
        msg = self.sign(session=session)
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8") as f:
        datas = json.loads(f.read())
    _check_item = datas.get("SMZDM", [])[0]
    print(Smzdm(check_item=_check_item).main())
