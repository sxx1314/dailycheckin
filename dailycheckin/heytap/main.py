# -*- coding: utf-8 -*-
import json
import os
import re
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

    @staticmethod
    def lottery(session, cookie, useragent, data, referer="", extra_draw_cookie=""):
        headers = {
            "Host": "hd.oppo.com",
            "User-Agent": useragent,
            "Cookie": extra_draw_cookie + cookie,
            "Referer": referer,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "br, gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        res = session.get(url="https://hd.oppo.com/user/login", headers=headers).json()
        if res["no"] == "200":
            res = session.post(url="https://hd.oppo.com/platform/lottery", data=data, headers=headers)
            res = res.json()
            return res
        else:
            return res

    @staticmethod
    def task_finish(session, cookie, useragent, aid, t_index):
        headers = {
            "Accept": "application/json, text/plain, */*;q=0.01",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Connection": "keep-alive",
            "User-Agent": useragent,
            "Accept-Encoding": "gzip, deflate",
            "cookie": cookie,
            "Origin": "https://hd.oppo.com",
            "X-Requested-With": "XMLHttpRequest",
        }
        datas = "aid=" + str(aid) + "&t_index=" + str(t_index)
        res = session.post("https://hd.oppo.com/task/finish", data=datas, headers=headers)
        res = res.json()
        return res

    @staticmethod
    def task_award(session, cookie, useragent, aid, t_index):
        headers = {
            "Accept": "application/json, text/plain, */*;q=0.01",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Connection": "keep-alive",
            "User-Agent": useragent,
            "Accept-Encoding": "gzip, deflate",
            "cookie": cookie,
            "Origin": "https://hd.oppo.com",
            "X-Requested-With": "XMLHttpRequest",
        }
        data = "aid=" + str(aid) + "&t_index=" + str(t_index)
        res = session.post("https://hd.oppo.com/task/award", data=data, headers=headers)
        res = res.json()
        return res

    def daily_task_and_draw(self, session, cookie, useragent, draw=False):
        message = []
        try:
            act_list = [
                {
                    "act_name": "赚积分",
                    "aid": 1418,
                    "if_task": True,  # 是否有任务
                    "referer": "https://hd.oppo.com/act/m/2021/jifenzhuanpan/index.html?us=gerenzhongxin&um=hudongleyuan&uc=yingjifen",
                    "if_draw": False,  # 是否有抽奖活动，已修复抽奖，如不需要抽奖请自行修改为False
                    "extra_draw_cookie": 'app_innerutm={"uc":"yingjifen","um":"hudongleyuan","ut":"direct","us":"gerenzhongxin"};',
                    # 抽奖必要的额外cookie信息，请勿随意修改，否则可能导致不中奖
                    "lid": 1307,  # 抽奖参数
                    "draw_times": 3,  # 控制抽奖次数3
                    "end_time": "2033-8-18 23:59:59",  # 长期任务
                    "text": "每次扣取0积分，任务获取次数",
                },
                {
                    "act_name": "realme积分大乱斗-8月",
                    "aid": 1582,
                    "if_task": True,
                    "referer": "https://hd.oppo.com/act/m/2021/2021/realmejifendalu/index.html",
                    "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
                    "extra_draw_cookie": 'app_innerutm={"uc":"renwuzhongxin","um":"hudongleyuan","ut":"direct","us":"gerenzhongxin"};',
                    "lid": 1466,
                    "draw_times": 3,
                    "end_time": "2022-8-31 23:59:59",
                    "text": "每次扣取5积分，测试仍然可以中奖",
                },
                {
                    "act_name": "realme积分大乱斗-9月",
                    "aid": 1582,
                    "if_task": True,
                    "referer": "https://hd.oppo.com/act/m/2021/2021/realmejifendalu/index.html?&us=realmenewshouye&um=yaofen&ut=right&uc=realmedaluandou",
                    "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
                    "extra_draw_cookie": 'app_innerutm={"uc":"renwuzhongxin","um":"hudongleyuan","ut":"direct","us":"gerenzhongxin"};',
                    "lid": 1554,  # 抽奖接口与8月不一样，测试可以独立抽奖
                    "draw_times": 3,
                    "end_time": "2022-8-31 23:59:59",
                    "text": "每次扣取5积分",
                },
                {
                    "act_name": "realme积分大乱斗-9月(2)",
                    "aid": 1598,
                    "if_task": True,
                    "referer": "https://hd.oppo.com/act/m/2021/huantaishangchengjif/index.html?&us=realmeshouye&um=icon&ut=3&uc=realmejifendaluandou",
                    "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
                    "extra_draw_cookie": 'app_innerutm={"uc":"realmejifendaluandou","um":"icon","ut":"3","us":"realmeshouye"};',
                    "lid": 1535,
                    "draw_times": 3,
                    "end_time": "2022-8-31 23:59:59",
                    "text": "每次扣取10积分",
                },
                {
                    "act_name": "天天积分翻倍",
                    "aid": 675,
                    "if_task": False,  # 该活动没有任务
                    "referer": "https://hd.oppo.com/act/m/2019/jifenfanbei/index.html?us=qiandao&um=task",
                    "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
                    "extra_draw_cookie": 'app_innerutm={"uc":"direct","um":"zuoshangjiao","ut":"direct","us":"shouye"};',
                    "lid": 1289,
                    "draw_times": 1,
                    "end_time": "2033-8-18 23:59:59",  # 长期任务
                    "text": "每次扣取10积分",
                },
                {
                    "act_name": "智能硬件0元抽奖",
                    "aid": 1588,
                    "if_task": False,  # 该活动没有任务
                    "referer": "https://hd.oppo.com/act/m/2021/3719/index.html?us=iotchannel&um=icon",
                    "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
                    "extra_draw_cookie": 'app_innerutm={"uc":"direct","um":"icon","ut":"direct","us":"iotchannel"};',
                    "lid": 1514,
                    "draw_times": 3,
                    "end_time": "2022-8-18 23:59:59",  # 活动8-5结束，实际还能玩
                    "text": "每次扣取0积分",
                },
            ]
            for act_item in act_list:
                act_name = act_item["act_name"]
                aid = act_item["aid"]
                referer = act_item["referer"]
                if_draw = act_item["if_draw"]
                if_task = act_item["if_task"]
                end_time = act_item["end_time"]
                headers = {
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Connection": "keep-alive",
                    "User-Agent": useragent,
                    "Accept-Encoding": "gzip, deflate",
                    "cookie": cookie,
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": referer,
                }
                dated = int(time.time())
                end_time = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))  # 设置活动结束日期

                if dated < end_time:
                    if if_task:
                        res = session.get(f"https://hd.oppo.com/task/list?aid={aid}", headers=headers)
                        taskList = res.json()
                        for i, jobs in enumerate(taskList["data"]):
                            title = jobs["title"]
                            t_index = jobs["t_index"]
                            aid = t_index[: t_index.index("i")]
                            if jobs["t_status"] == 0:
                                finishmsg = self.task_finish(
                                    session=session, cookie=cookie, useragent=useragent, aid=aid, t_index=t_index
                                )
                                if finishmsg["no"] == "200":
                                    time.sleep(1)
                                    awardmsg = self.task_award(
                                        session=session, cookie=cookie, useragent=useragent, aid=aid, t_index=t_index
                                    )
                                    msg = awardmsg["msg"]
                                    message.append({"name": title, "value": msg})
                                    time.sleep(3)
                            elif jobs["t_status"] == 1:
                                awardmsg = self.task_award(
                                    session=session, cookie=cookie, useragent=useragent, aid=aid, t_index=t_index
                                )
                                msg = awardmsg["msg"]
                                message.append({"name": title, "value": msg})
                                time.sleep(3)
                            else:
                                message.append({"name": title, "value": "任务已完成"})
                    if draw:
                        if if_draw:
                            lid = act_list["lid"]
                            extra_draw_cookie = act_list["extra_draw_cookie"]
                            draw_times = act_list["draw_times"]
                            x = 0
                            while x < draw_times:
                                source_type = re.findall("source_type=(.*?);", cookie)[0]
                                s_channel = re.findall("s_channel=(.*?);", cookie)[0]
                                data = f"aid={aid}&lid={lid}&mobile=&authcode=&captcha=&isCheck=0&source_type={source_type}&s_channel={s_channel}&sku=&spu="
                                res = self.lottery(
                                    session=session,
                                    cookie=cookie,
                                    useragent=useragent,
                                    data=data,
                                    referer=referer,
                                    extra_draw_cookie=extra_draw_cookie,
                                )
                                msg = res["msg"]
                                print(res)
                                if "次数已用完" in msg:
                                    message.append({"name": f"第 {x + 1} 抽奖", "value": "抽奖次数已用完"})
                                    break
                                if "活动已结束" in msg:
                                    message.append({"name": f"第 {x + 1} 抽奖", "value": "活动已结束，终止抽奖"})
                                    break
                                goods_name = res["data"]["goods_name"]
                                if goods_name:
                                    message.append({"name": f"第 {x + 1} 抽奖", "value": str(goods_name)})
                                elif "提交成功" in msg:
                                    message.append({"name": f"第 {x + 1} 抽奖", "value": "未中奖"})
                                x += 1
                                time.sleep(5)
                else:
                    message.append({"name": act_name, "value": "活动已结束，不再执行"})
        except Exception as e:
            message.append({"name": "执行任务和抽奖", "value": str(e)})
        return message

    def main(self):
        cookie = self.check_item.get("cookie")
        useragent = self.check_item.get("useragent")
        draw = self.check_item.get("draw")
        session = self.login(cookie=cookie, useragent=useragent)
        if session:
            dayily_sign_msg = self.dayily_sign(session=session, cookie=cookie, useragent=useragent)
            daily_viewgoods_msg = self.daily_viewgoods(session=session, cookie=cookie, useragent=useragent)
            daily_sharegoods_msg = self.daily_sharegoods(session=session, cookie=cookie, useragent=useragent)
            daily_task_and_draw_msg = self.daily_task_and_draw(
                session=session, cookie=cookie, useragent=useragent, draw=draw
            )
            msg = [dayily_sign_msg, daily_viewgoods_msg, daily_sharegoods_msg] + daily_task_and_draw_msg
        else:
            msg = [{"name": "登录信息", "value": "账号登录失败"}]
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8") as f:
        datas = json.loads(f.read())
    _check_item = datas.get("HEYTAP", [])[0]
    print(HeyTap(check_item=_check_item).main())
