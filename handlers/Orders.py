# encoding=utf-8
import logging
# import time
# import random

from static.data import data_submit_order, data_order
# from utils.commons import required_login
from handlers.BaseHandler import BaseHandler
from utils.response_code import RET
from utils.utils import verify_request_body



class OrderHandler(BaseHandler):
    """订单"""
    def post(self):
        ExpectParams = ["user_id", "token"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write({"errcode": RET.PARAMERR, "errmsg": "params error"})
        user_id = str(RqstDt.get('user_id'))
        token = str(RqstDt.get('token'))
        # # 校验参数
        # if not all(user_id, token):
        #     return self.write({"errcode": RET.PARAMERR, "errmsg": "params error"})
        #
        # try:
        #     real_token = self.session.data['token']
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DBERR, errmsg='get token error'))
        #
        # # 判断token是否过期
        # if not real_token:
        #     return self.write(dict(errcode=RET.NODATA, errmsg='token expire'))
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
        #     return self.write(dict(errcode=RET.DBERR, errmsg="get data error"))
        # data = []
        # for row in ret:
        #     d = {
        #         "order_id": row.get("order_id"),
        #         "order_status": row.get("order_status"),
        #         "link_address": row.get("link_ddress"),
        #         "defult_address": row.get("defult_address")
        #     }
        # data.append(d)

        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
        print user_id, token, "+++order+++"
        self.write(dict(errcode=RET.OK, errmsg="OK", data=data_order))


class SubmitOrderHandler(BaseHandler):
    """提交订单"""
    # @required_login
    def post(self):
        # product_id = str(RqstDt.get('product_id'))
        # product_name = str(RqstDt.get('product_name'))
        # product_price = str(RqstDt.get('product_price'))
        # product_num = str(RqstDt.get('product_num'))

        user_id = self.json_args.get("user_id")
        token = self.json_args.get("token")
        product_price_total = self.json_args.get("product_price_total")
        addr_info = self.json_args.get("addr_info")
        delivery_price = self.json_args.get("delivery_price")
        product_order_list = self.json_args.get("product_order_list")


        # try:
        #     real_token = self.session.data['token']
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DBERR, errmsg="get token error"))
        #
        # # 判断token是否过期
        # if not real_token:
        #     return self.write(dict(errcode=RET.NODATA, errmsg="token expire"))
        #
        # # 校验token
        # if  real_token != token:
        #     return self.write(dict(errcode=RET.DBERR,errmsg="token error"))

        # # 保存订单数据
        # _sql = ""
        # try:
        #     self.db.execute(_sql)
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DATAEXIST, errmsg="save fail"))

        # # 校验库存是否充足
        # # 从数据库中查询库存量
        # _sql = ""
        # try:
        #     stock_num = self.db.query(_sql)
        #     if goods_num > stock_num:
        #         return self.write(dict(errcode=RET.DATAERR, errmsg="low stock_num"))
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DBERR, errmsg="get stock_num error"))
        # if not stock_num:
        #     return self.write(dict(errcode=RET.NODATA, errmsg="no data"))
        # datetime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        # order_id = datetime + "%05d"%random.randint(1, 10000)
        # data ={
        #     "order_id" :order_id
        # }

        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
        print user_id,token, product_price_total, addr_info, product_order_list,delivery_price,"=====order====="
        self.write(dict(errcode=RET.OK, errmsg="OK", data=data_submit_order))


class CancelOrderHandler(BaseHandler):
    """取消订单"""
    def post(self):

        # 校验参数
        ExpectParams = ["user_id","token","order_id"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write({"errcode": RET.PARAMERR, "errmsg": "params error"})
        user_id = str(RqstDt.get('user_id'))
        token = str(RqstDt.get('token'))
        order_id = str(RqstDt.get('order_id'))
        # try:
        #     real_token = self.session.data['token']
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DBERR, errmsg="get token error"))

        # # 判断token是否过期
        # if not real_token:
        #     return self.write(dict(errcode=RET.NODATA, errmsg="token expire"))
        #
        # # 校验access_token
        # if  real_token != token:
        #     return self.write(dict(errcode=RET.DBERR,errmsg="token error"))

        # # 逻辑删除订单
        # _sql = ""
        # try:
        #     self.db.execute(_sql)
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DATAEXIST, errmsg="delete fail"))
        print user_id,token,order_id
        self.write(dict(errcode=RET.OK, errmsg="OK"))
