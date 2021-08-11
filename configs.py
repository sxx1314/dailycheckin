# -*- coding: utf-8 -*-
import json
import os

from dailycheckin.acfun.acfun import AcFunCheckIn
from dailycheckin.baidu_url_submit.baidu_url_submit import BaiduUrlSubmit
from dailycheckin.bilibili.bilibili import BiliBiliCheckIn
from dailycheckin.cloud189.cloud189 import Cloud189CheckIn
from dailycheckin.csdn.csdn import CSDNCheckIn
from dailycheckin.duokan.duokan import DuoKanCheckIn
from dailycheckin.fmapp.fmapp import FMAPPCheckIn
from dailycheckin.iqiyi.iqiyi import IQIYICheckIn
from dailycheckin.kgqq.kgqq import KGQQCheckIn
from dailycheckin.meizu.meizu import MeizuCheckIn
from dailycheckin.mgtv.mgtv import MgtvCheckIn
from dailycheckin.mimotion.mimotion import MiMotion
from dailycheckin.music163.music163 import Music163CheckIn
from dailycheckin.oneplusbbs.oneplusbbs import OnePlusBBSCheckIn
from dailycheckin.picacomic.picacomic import PicacomicCheckIn
from dailycheckin.pojie.pojie import PojieCheckIn
from dailycheckin.smzdm.smzdm import SmzdmCheckIn
from dailycheckin.tieba.tieba import TiebaCheckIn
from dailycheckin.v2ex.v2ex import V2exCheckIn
from dailycheckin.vqq.vqq import VQQCheckIn
from dailycheckin.weather.weather import Weather
from dailycheckin.weibo.weibo import WeiBoCheckIn
from dailycheckin.womail.womail import WoMailCheckIn
from dailycheckin.www2nzz.www2nzz import WWW2nzzCheckIn
from dailycheckin.wzyd.wzyd import WZYDCheckIn
from dailycheckin.youdao.youdao import YouDaoCheckIn
from dailycheckin.zhiyoo.zhiyoo import ZhiyooCheckIn

checkin_map = {
    "IQIYI_COOKIE_LIST": ("爱奇艺", IQIYICheckIn),
    "VQQ_COOKIE_LIST": ("腾讯视频", VQQCheckIn),
    "MGTV_PARAMS_LIST": ("芒果TV", MgtvCheckIn),
    "KGQQ_COOKIE_LIST": ("全民K歌", KGQQCheckIn),
    "MUSIC163_ACCOUNT_LIST": ("网易云音乐", Music163CheckIn),
    "BILIBILI_COOKIE_LIST": ("Bilibili", BiliBiliCheckIn),
    "YOUDAO_COOKIE_LIST": ("有道云笔记", YouDaoCheckIn),
    "FMAPP_ACCOUNT_LIST": ("Fa米家 APP", FMAPPCheckIn),
    "BAIDU_URL_SUBMIT_LIST": ("百度站点提交", BaiduUrlSubmit),
    "ONEPLUSBBS_COOKIE_LIST": ("一加手机社区官方论坛", OnePlusBBSCheckIn),
    "SMZDM_COOKIE_LIST": ("什么值得买", SmzdmCheckIn),
    "TIEBA_COOKIE_LIST": ("百度贴吧", TiebaCheckIn),
    "V2EX_COOKIE_LIST": ("V2EX 论坛", V2exCheckIn),
    "WWW2NZZ_COOKIE_LIST": ("咔叽网单", WWW2nzzCheckIn),
    "ACFUN_ACCOUNT_LIST": ("AcFun", AcFunCheckIn),
    "MIMOTION_ACCOUNT_LIST": ("小米运动", MiMotion),
    "CLOUD189_ACCOUNT_LIST": ("天翼云盘", Cloud189CheckIn),
    "POJIE_COOKIE_LIST": ("吾爱破解", PojieCheckIn),
    "MEIZU_COOKIE_LIST": ("MEIZU社区", MeizuCheckIn),
    "PICACOMIC_ACCOUNT_LIST": ("哔咔漫画", PicacomicCheckIn),
    "ZHIYOO_COOKIE_LIST": ("智友邦", ZhiyooCheckIn),
    "WEIBO_COOKIE_LIST": ("微博", WeiBoCheckIn),
    "DUOKAN_COOKIE_LIST": ("多看阅读", DuoKanCheckIn),
    "CSDN_COOKIE_LIST": ("CSDN", CSDNCheckIn),
    "WZYD_DATA_LIST": ("王者营地", WZYDCheckIn),
    "WOMAIL_URL_LIST": ("沃邮箱", WoMailCheckIn),
    "CITY_NAME_LIST": ("天气预报", Weather),
}

notice_map = {
    "FSKEY": "",
    "DINGTALK_SECRET": "",
    "DINGTALK_ACCESS_TOKEN": "",
    "BARK_URL": "",
    "SCKEY": "",
    "SENDKEY": "",
    "TG_BOT_TOKEN": "",
    "TG_USER_ID": "",
    "TG_API_HOST": "",
    "TG_PROXY": "",
    "QMSG_KEY": "",
    "QMSG_TYPE": "",
    "COOLPUSHSKEY": "",
    "COOLPUSHQQ": "",
    "COOLPUSHWX": "",
    "COOLPUSHEMAIL": "",
    "QYWX_KEY": "",
    "QYWX_CORPID": "",
    "QYWX_AGENTID": "",
    "QYWX_CORPSECRET": "",
    "QYWX_TOUSER": "",
    "PUSHPLUS_TOKEN": "",
    "PUSHPLUS_TOPIC": "",
}


def env2list(key):
    try:
        value = json.loads(os.getenv(key, []).strip()) if os.getenv(key) else []
        if isinstance(value, list):
            value = value
        else:
            value = []
    except Exception as e:
        print(e)
        value = []
    return value


def env2str(key):
    try:
        value = os.getenv(key, "") if os.getenv(key) else ""
        if isinstance(value, str):
            value = value.strip()
        elif isinstance(value, bool):
            value = value
        else:
            value = None
    except Exception as e:
        print(e)
        value = None
    return value


def get_checkin_info(data):
    result = {}
    if isinstance(data, dict):
        for one in checkin_map.keys():
            result[one.lower()] = data.get(one, [])
    else:
        for one in checkin_map.keys():
            result[one.lower()] = env2list(one)
    return result


def get_notice_info(data):
    result = {}
    if isinstance(data, dict):
        for one in notice_map.keys():
            result[one.lower()] = data.get(one, None)
    else:
        for one in notice_map.keys():
            result[one.lower()] = env2str(one)
    return result
