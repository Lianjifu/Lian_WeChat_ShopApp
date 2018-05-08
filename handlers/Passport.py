# coding:utf-8
import hashlib
import json
import logging
import constants
import re
import random

import config
from handlers.BaseHandler import BaseHandler
from static.data import data_login
from utils.session import Session
from utils.response_code import RET
from utils.utils import verify_request_body


class RegisterHandler(BaseHandler):
    """用户注册"""
    def post(self):
        # 校验参数
        ExpectParams = ["mobile_number"]
        RqstDt = verify_request_body(self, ExpectParams)
        if not RqstDt:
            return self.write({"errcode": RET.PARAMERR, "errmsg": "params error"})
        mobile_number = str(RqstDt.get('mobile_number'))
        if not re.match(r'^1\d{10}$',mobile_number):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号格式错误"))

        self.write(dict(errcode=RET.OK, errmsg="OK"))


class LoginHandler(BaseHandler):
    """用户登录"""
    def post(self):
        # 校验参数
        ExpectParams = ["mobile_number","sms_code"]
        RqstDt = verify_request_body(self, ExpectParams)
        if not RqstDt:
            return self.write({"errcode": RET.PARAMERR, "errmsg": "params error"})
        mobile_number = str(RqstDt.get('mobile_number'))
        sms_code = str(RqstDt.get('sms_code'))
        # # 判断短信验证码是否真确
        # if "2468" != sms_code:
        #     try:
        #         real_sms_code = self.redis.get("sms_code_%s" % mobile_number)
        #     except Exception as e:
        #         logging.error(e)
        #         return self.write(dict(errcode=RET.DBERR, errmsg="查询验证码出错"))
        #
        #     # 判断短信验证码是否过期
        #     if not real_sms_code:
        #         return self.write(dict(errcode=RET.NODATA, errmsg="验证码过期"))
        #
        #     # 对比用户填写的验证码与真实值
        #     # if real_sms_code != sms_code and  sms_code != "2468":
        #     if real_sms_code != sms_code:
        #         return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误"))
        #
        #     try:
        #         self.redis.delete("sms_code_%s" % mobile_number)
        #     except Exception as e:
        #         logging.error(e)

        # 保存数据

        # _sql = ""
        # try:
        #     user_id = self.db.execute(_sql)
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DATAEXIST, errmsg="保存数据失败"))
        #
        # token = hashlib.sha256(config.token).hexdigest()
        # # 用session记录用户的登录状态
        # session = Session(self)
        # session.data["user_id"] = user_id
        # session.data["mobile"] = mobile_number
        # session.data["token"] = token
        #
        # try:
        #     session.save()
        #     data = [{
        #             "user_id": session.data["user_id"],
        #             "token": session.data["token"]
        #         }]
        # except Exception as e:
        #     logging.error(e)

        # self.write(dict(errcode=RET.OK, errmsg="登录成功",data=data))
        print mobile_number,sms_code
        self.write(dict(errcode=RET.OK, errmsg="OK",data=data_login))


class CheckLoginHandler(BaseHandler):
    """检查登录状态"""
    def get(self):
        # get_current_user方法在基类中已实现，它的返回值是session.data（用户保存在redis中
        # 的session数据），如果为{} ，意味着用户未登录;否则，代表用户已登录
        if self.get_current_user():
            self.write({"errcode":RET.OK, "errmsg":"true", "data":{"name":self.session.data.get("name")}})
        else:
            self.write({"errcode":RET.SESSIONERR, "errmsg":"false"})

