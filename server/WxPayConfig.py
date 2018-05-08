# encoding=utf-8
"""
*   配置账号信息
"""
import random
import time

import datetime


class WxPayConf(object):
    """配置账号信息"""
    # ===============【基本信息设置】===================
    AppId = ""
    AppSecret = ""
    MchId = ""
    # 商户支付密钥key
    Merchant_key = ""
    # ===============【异步通知url设置】================
    NOTIFY_URL = "http://"
    # ================【证书路径】======================
    #
    # 证书路径，应该填写绝对路径（仅退款、撤销订单时需要）
    SSLCERT_PATH = "../cert/apiclient_cert.pem"
    SSLKEY_PATH = "../cert/apiclient_key.pem"
    # ================【curl超时设置】==================
    CURL_TIMEOUT = 30

    # 商户订单 时间+随机数
    now = datetime.fromtimestamp(time.time(), tz=time.timezone('Asia/Shanghai'))
    OUT_TRADE_NO = '{0}{1}{2}'.format(MchId, now.strftime('%Y%m%d%H%M%S'), random.randint(1000, 10000))

