# encoding=utf-8
import logging
from handlers.BaseHandler import BaseHandler
from utils.utils import  verify_request_body
from utils.response_code import RET

class PayHandler(BaseHandler):
    """支付"""
    def post(self):
        # api_log_start(PayHandler)
        ExpectParams = ["user_id", "token", "order_id"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            logging.error("params error")
            return self.write({"errcode": RET.PARAMERR, "errmsg": "params error"})
        user_id = str(RqstDt.get('user_id'))
        token = str(RqstDt.get('token'))
        order_id = str(RqstDt.get('order_id'))

        print user_id, token, order_id
        self.write(dict(errcode=RET.OK, errmsg="OK"))
