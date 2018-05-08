# coding:utf-8

import logging
import random
import re

from BaseHandler import BaseHandler

from constants import SMS_CODE_EXPIRES_SECONDS
from utils.response_code import RET


class SMSCodeHandler(BaseHandler):
    """短信验证码"""
    def post(self):
        # 获取参数
        mobile_number = self.json_args.get("mobile_number")

        # 参数校验
        # if mobile and piccode and piccode_id
        if not mobile_number:
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数错误"))
        if not re.match(r"^1\d{10}$", mobile_number):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="手机号格式错误"))

        # 产生随机短信验证码
        sms_code = "%06d" % random.randint(1, 1000000)
        try:
            self.redis.setex("sms_code_%s" % mobile_number, SMS_CODE_EXPIRES_SECONDS, sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="数据库出错"))

        # # 发送短信验证码
        # try:
        #     result = ccp.sendTemplateSMS(mobile_number, [sms_code, SMS_CODE_EXPIRES_SECONDS/60], 1)
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.THIRDERR, errmsg="发送短信失败"))
        # if result:
        #     self.write(dict(errcode=RET.OK, errmsg="发送成功"))
        # else:
        #     self.write(dict(errcode=RET.UNKOWNERR, errmsg="发送失败"))