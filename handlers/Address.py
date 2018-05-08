# encoding=utf-8
import logging
from handlers.BaseHandler import BaseHandler
from static.data import data_address,data_new_address
from utils.response_code import RET
from utils.utils import verify_request_body


class AddressHandler(BaseHandler):
    """地址"""
    def post(self):
        # TODO 从body中获取数据
        ExpectParams = ["user_id", "token"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write({"errcode": RET.PARAMERR, "errmsg": "params error"})
        user_id = str(RqstDt.get('user_id'))
        token = str(RqstDt.get('token'))

        # try:
        #     real_token = self.session.data['token']
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DBERR, errmsg='get token error'))
        #
        # # 判断token是否过期
        # if not real_token:
        #     return self.write(dict(errcodw=RET.NODATA, errmsg='token expire'))
        #
        # # 校验token
        # if real_token != token:
        #     return self.write(dict(errcode=RET.DBERR, errmsg="token error"))

        # # 从mysql数据库中取数据
        # _sql = ""
        # try:
        #     ret = self.db.query(_sql)
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DBERR,errmsg="get data error"))
        # data = []
        # for row in ret:
        #     d = {
        #         "link_man": row.get("lin_kman"),
        #         "link_phone":row.get("link_phone"),
        #         "link_address": row.get("link_ddress"),
        #         "defult_address":row.get("defult_address")
        #     }
        # data.append(d)

        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
        print user_id,token
        self.write(dict(errcode=RET.OK, errmsg="OK", data=data_address))

class NewAddressHandler(BaseHandler):
    """添加新地址"""
    def post(self):
        # TODO 从body中获取数据

        ExpectParams = ["user_id", "token", "addr_province", "addr_city", "addr_xian", "addr_street", "addr_detail","link_man","link_phone","defult_address"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write({"errcode": RET.PARAMERR, "errmsg": "params error"})
        user_id = str(RqstDt.get('user_id'))
        token = str(RqstDt.get('token'))
        addr_province = str(RqstDt.get('addr_province'))
        addr_city = str(RqstDt.get('addr_city'))
        addr_xian = str(RqstDt.get('addr_xian'))
        addr_street = str(RqstDt.get('addr_street'))
        addr_detail = str(RqstDt.get('addr_detail'))
        link_man = str(RqstDt.get('link_man'))
        link_phone = str(RqstDt.get('link_phone'))
        defult_address = str(RqstDt.get('defult_address'))


        # link_address = addr_province + addr_city + addr_xian + addr_street + addr_detail
        #
        # # TODO 根据省份判断快递费
        #
        # # 保存数据
        # _sql = ""
        # try:
        #     ret = self.db.query(_sql)
        # except Exception as e:
        #     logging(e)
        #     return self.write(dict(errcode=RET.DBERR, errmsg="save data error"))

        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
        print user_id,token,addr_province,addr_city,addr_xian,addr_street,addr_detail,defult_address,link_man,link_phone
        self.write(dict(errcode=RET.OK, errmsg="OK", data=data_new_address))