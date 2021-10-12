# -*- coding: utf-8 -*-
import json
import os
import time

import requests

from dailycheckin import CheckIn


class HeyTap(CheckIn):
    name = "欢太商城"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def login(cookie, useragent):
        session = requests.Session()
        headers = {
            "Host": "www.heytap.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "User-Agent": useragent,
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "gzip, deflate, br",
            "cookie": cookie,
        }
        response = session.get(url="https://www.heytap.com/cn/oapi/users/web/member/info", headers=headers)
        response.encoding = "utf-8"
        try:
            result = response.json()
            if result["code"] == 200:
                return session
            else:
                print(f"【登录失败】: {result['errorMessage']}")
        except Exception as e:
            print(f"【登录失败】:{e}")
        return False

    @staticmethod
    def task_center(session, cookie, useragent):
        headers = {
            "Host": "store.oppo.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "User-Agent": useragent,
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "gzip, deflate, br",
            "cookie": cookie,
            "referer": "https://store.oppo.com/cn/app/taskCenter/index",
        }
        response = session.get(url="https://store.oppo.com/cn/oapi/credits/web/credits/show", headers=headers)
        result = response.json()
        return result

    @staticmethod
    def cashing_credits(session, useragent, cookie, info_marking, info_type, info_credits):
        headers = {
            "Host": "store.oppo.com",
            "clientPackage": "com.oppo.store",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "User-Agent": useragent,
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "gzip, deflate, br",
            "cookie": cookie,
            "Origin": "https://store.oppo.com",
            "X-Requested-With": "com.oppo.store",
            "referer": "https://store.oppo.com/cn/app/taskCenter/index?us=gerenzhongxin&um=hudongleyuan&uc=renwuzhongxin",
        }

        data = f"marking={info_marking}&type={info_type}&amount={info_credits}"
        res = session.post(
            url="https://store.oppo.com/cn/oapi/credits/web/credits/cashingCredits", data=data, headers=headers
        )
        res = res.json()
        if res["code"] == 200:
            return True
        else:
            return False

    def dayily_sign(self, session, cookie, useragent):
        try:
            dated = time.strftime("%Y-%m-%d")
            headers = {
                "Host": "store.oppo.com",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Content-Type": "application/x-www-form-urlencoded",
                "Connection": "keep-alive",
                "User-Agent": useragent,
                "Accept-Language": "zh-cn",
                "Accept-Encoding": "gzip, deflate, br",
                "cookie": cookie,
                "referer": "https://store.oppo.com/cn/app/taskCenter/index",
            }
            result = self.task_center(session=session, cookie=cookie, useragent=useragent)
            status = result["data"]["userReportInfoForm"]["status"]
            if status == 0:
                res = result["data"]["userReportInfoForm"]["gifts"]
                for data in res:
                    if data["date"] == dated:
                        qd = data
                        if not qd["today"]:
                            data = "amount=" + str(qd["credits"])
                            response = session.post(
                                url="https://store.oppo.com/cn/oapi/credits/web/report/immediately",
                                headers=headers,
                                data=data,
                            )
                            res = response.json()
                            if res["code"] == 200:
                                return {"name": "每日签到成功", "value": res["data"]["message"]}
                            else:
                                return {"name": "每日签到失败", "value": str(res)}
                        else:
                            if len(str(qd["type"])) < 1:
                                data = "amount=" + str(qd["credits"])
                            else:
                                data = (
                                    "amount="
                                    + str(qd["credits"])
                                    + "&type="
                                    + str(qd["type"])
                                    + "&gift="
                                    + str(qd["gift"])
                                )
                            response1 = session.post(
                                url="https://store.oppo.com/cn/oapi/credits/web/report/immediately",
                                headers=headers,
                                data=data,
                            )
                            res1 = response1.json()
                            if res1["code"] == 200:
                                return {"name": "每日签到成功", "value": res1["data"]["message"]}
                            else:
                                return {"name": "每日签到失败", "value": str(res1)}
            else:
                return {"name": "每日签到", "value": "已经签到过了"}
            time.sleep(1)
        except Exception as e:
            return {"name": "每日签到", "value": f"错误，原因为: {e}"}

    def daily_viewgoods(self, session, cookie, useragent):
        try:
            headers = {
                "clientPackage": "com.oppo.store",
                "Host": "msec.opposhop.cn",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Content-Type": "application/x-www-form-urlencoded",
                "Connection": "keep-alive",
                "User-Agent": "okhttp/3.12.12.200sp1",
                "Accept-Encoding": "gzip",
                "cookie": cookie,
            }
            res = self.task_center(session=session, cookie=cookie, useragent=useragent)
            res = res["data"]["everydayList"]
            for data in res:
                if data["name"] == "浏览商品":
                    qd = data
                    if qd["completeStatus"] == 0:
                        shop_list = session.get(
                            "https://msec.opposhop.cn/goods/v1/SeckillRound/goods/115?pageSize=10&currentPage=1"
                        )
                        res = shop_list.json()
                        if res["meta"]["code"] == 200:
                            for skuinfo in res["detail"]:
                                skuid = skuinfo["skuid"]
                                requests.get(
                                    "https://msec.opposhop.cn/goods/v1/info/sku?skuId=" + str(skuid), headers=headers
                                )
                                time.sleep(5)
                            res2 = self.cashing_credits(
                                session=session,
                                cookie=cookie,
                                useragent=useragent,
                                info_marking=qd["marking"],
                                info_type=qd["type"],
                                info_credits=qd["credits"],
                            )
                            if res2:
                                return {"name": "浏览商品", "value": f"任务完成!积分领取+{qd['credits']}"}
                            else:
                                return {"name": "浏览商品", "value": f"领取积分奖励出错"}
                        else:
                            return {"name": "浏览商品", "value": f"错误，获取商品列表失败"}
                    elif qd["completeStatus"] == 1:
                        res2 = self.cashing_credits(
                            session=session,
                            cookie=cookie,
                            useragent=useragent,
                            info_marking=qd["marking"],
                            info_type=qd["type"],
                            info_credits=qd["credits"],
                        )
                        if res2:
                            return {"name": "浏览商品", "value": f"任务完成!积分领取+{qd['credits']}"}
                        else:
                            return {"name": "浏览商品", "value": f"领取积分奖励出错"}
                    else:
                        return {"name": "浏览商品", "value": f"任务已完成!"}
        except Exception as e:
            return {"name": "浏览商品", "value": f"错误，原因为: {e}"}

    def daily_sharegoods(self, session, cookie, useragent):
        try:
            headers = {
                "clientPackage": "com.oppo.store",
                "Host": "msec.opposhop.cn",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Content-Type": "application/x-www-form-urlencoded",
                "Connection": "keep-alive",
                "User-Agent": "okhttp/3.12.12.200sp1",
                "Accept-Encoding": "gzip",
                "cookie": cookie,
            }
            day_sign_list = self.task_center(session=session, cookie=cookie, useragent=useragent)
            res = day_sign_list
            res = res["data"]["everydayList"]
            for data in res:
                if data["name"] == "分享商品到微信":
                    qd = data
                    if qd["completeStatus"] == 0:
                        count = qd["readCount"]
                        endcount = qd["times"]
                        while count <= endcount:
                            session.get(
                                url="https://msec.opposhop.cn/users/vi/creditsTask/pushTask?marking=daily_sharegoods",
                                headers=headers,
                            )
                            count += 1
                        res2 = self.cashing_credits(
                            session=session,
                            cookie=cookie,
                            useragent=useragent,
                            info_marking=qd["marking"],
                            info_type=qd["type"],
                            info_credits=qd["credits"],
                        )
                        if res2:
                            return {"name": "分享商品", "value": f"任务完成!积分领取+{qd['credits']}"}
                        else:
                            return {"name": "分享商品", "value": f"领取积分奖励出错!"}
                    elif qd["completeStatus"] == 1:
                        res2 = self.cashing_credits(
                            session=session,
                            cookie=cookie,
                            useragent=useragent,
                            info_marking=qd["marking"],
                            info_type=qd["type"],
                            info_credits=qd["credits"],
                        )
                        if res2:
                            return {"name": "分享商品", "value": f"任务完成!积分领取+{qd['credits']}"}
                        else:
                            return {"name": "分享商品", "value": f"领取积分奖励出错!"}
                    else:
                        return {"name": "分享商品", "value": f"任务已完成!"}
        except Exception as e:
            return {"name": "分享商品", "value": f"错误，原因为: {e}"}

    def main(self):
        cookie = self.check_item.get("cookie")
        useragent = self.check_item.get("useragent")
        session = self.login(cookie=cookie, useragent=useragent)
        if session:
            dayily_sign_msg = self.dayily_sign(session=session, cookie=cookie, useragent=useragent)
            daily_viewgoods_msg = self.daily_viewgoods(session=session, cookie=cookie, useragent=useragent)
            daily_sharegoods_msg = self.daily_sharegoods(session=session, cookie=cookie, useragent=useragent)
            msg = [dayily_sign_msg, daily_viewgoods_msg, daily_sharegoods_msg]
        else:
            msg = [{"name": "登录信息", "value": "账号登录失败"}]
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8") as f:
        datas = json.loads(f.read())
    _check_item = datas.get("HEYTAP", [])[0]
    print(HeyTap(check_item=_check_item).main())
