# encoding=utf-8
import logging

from BaseHandler import BaseHandler
from server.WxPayServer import UnifiedOrder, OrderQuery, InvokePay, CloseOrder, Refund, \
    RefundQuery
from utils.response_code import RET
from server.WxPayConfig import WxPayConf


class PayHandler(BaseHandler):
    """统一支付"""
    def post(self):
        code = self.json_args("code")
        total_fee = self.json_args("product_price_total")
        # 校验参数
        if not code:
            return self.write(dict(errcode=RET.NODATA, errmsg='expire error'))
        openid = InvokePay().getOpenid(code)
        # 调用统一下单接口
        order = UnifiedOrder()
        order.parameters = {
            "openid": openid,
            "out_trade_no": WxPayConf.OUT_TRADE_NO,
            "body": "",    # 商品描述  商家名称-销售商品类目
            "total_fee": total_fee,  # 金额
        }
        prepay_result = order.getResult()
        prepay_id = prepay_result["prepay_id"]
        # 调用支付接口
        invoke_pay = InvokePay()
        invoke_pay.setPrepayId(prepay_id)
        pay_parameter = InvokePay.getParameters()
        return self.write(dict(errcode=RET.OK, errmsg="SUCEESS", data=pay_parameter))


class OrderQueryHandler(BaseHandler):
    """调用查询订单"""

    # 0 订单不成功， 1 表示订单成功， 2 表示继续等待
    def post(self):

        # TODO 传递参数
        order_query = OrderQuery()
        order_query.parameters = {
                "out_trade_no": ""
        }
        query_retult = order_query.getResult()
        if query_retult["return_code"] == "SUCCESS" and query_retult["return_msg"] == "SUCCESS":
            # 支付成功
            if query_retult["trade_state"] == "SUCCESS":
                # 返回的数据参数
                # data = {
                #     "openid": query_retult["openid"],  # 用户标识
                #     "order_status": 0,  # 自定义的订单状态 0:表示已完成
                #     "total_fee": query_retult["total_fee"], # 标价金额
                #     "cash_fee": query_retult["cash_fee"],   # 支付金额
                #     "transaction_id": query_retult["transaction_id"], # 微信订单号
                #     "out_trade_no": query_retult["out_trade_no"], # 商户订单号
                #     "time_end": query_retult["time_end"]  # 支付完成时间
                # }
                # TODO 保存下数据到数据库中（待完成）
                return self.write(dict(errcode=RET.OK, errmsg="SUCCESS"))
            # 未支付
            elif query_retult["trade_state"] == "NOATPAY":
                data = {
                    # "out_trade_no":query_retult["out_trade_no"],
                    "order_status": 1  # 自定义的订单状态 1:表示待支付
                }
                # TODO 保存下数据到数据库中（待完成）
                return self.write(dict(errcode=RET.NOTPAY, errmsg="未支付",data=data))
            # 支付失败
            else:
                # 关闭订单
                close_order = CloseOrder()
                close_retult = close_order.getResult()
                if close_retult["return_code"] == "SUCCESS":
                    return True
                else:
                    return False

        # 如果返回错误码为“此交易订单号不存在” 则直接认定失败
        if query_retult["err_code"] == "ORDERNOTEXIST":
            # 关闭订单
            close_order = CloseOrder()
            close_retult = close_order.getResult()
            if close_retult["return_code"] == "SUCCESS":
                return True
            else:
                return False
        else:
            # 如果是系统错误，则后续继续
            succCode = 2

        return False


class RefundHandler(BaseHandler):
    """调用申请退款方法"""
    def post(self):
        # TODO 传递参数
        refund = Refund()
        refund.parameters = {
            "out_trade_no": "",
            "out_refund_no": "",
            "total_fee": "",
            "refund_fee": "",
            "op_user_id": ""
        }
        refund_retult = refund.getResult()
        try:
            if refund_retult["return_code"] == "SUCCESS":
                data = {
                    "out_trade_no": refund_retult["out_trade_no"],
                    "out_refund_no": refund_retult["out_refund_no"],
                    "refund_fee": refund_retult["refund_fee"],
                }
                # TODO 保存数据到数据库中（待完成）
                return self.write(dict(errcode=RET.OK,errmsg="refund success"))
            else:
                return self.write(dict(errcode=RET.REFUNDERROR,errmsg="退款失败"))
        except Exception as e:
            logging.error(e)


class RefundQueryHandler(BaseHandler):
    """查询退款"""
    def post(self):
        # TODO 传递参数
        refund_query = RefundQuery()
        refund_query.parameters = {
            "out_refund_no": "",
            "out_trade_no": "",
        }
        refund_query_retult = refund_query.getResult()
        try:
            if refund_query["return_code"] == "SUCCESS":
                data ={
                    "out_trade_no" : refund_query_retult["out_trade_no"], # 商户订单号
                    "out_refund_no_$n": refund_query_retult["out_refund_no_$n"], # 商户退款单号
                    "refund_count": refund_query_retult["refund_count"], # 退款笔数
                    "refund_fee_$n": refund_query_retult["refund_fee_$n"], # 申请退款金额
                    # SUCCESS—退款成功  REFUNDCLOSE—退款关闭 PROCESSING—退款处理中 CHANGE—退款异常，
                    "refund_status_$n": refund_query_retult["refund_status_$n"],
                    # 1）退回银行卡：2）退回支付用户零钱: 3）退还商户: 4）退回支付用户零钱通:
                    "refund_recv_accout_$n":refund_query_retult["refund_recv_accout_$n"],
                    "refund_success_time_$n":refund_query_retult["refund_success_time_$n"]   # 退款成功时间
                }
        except Exception as e:
            logging.error(e)
            return False


class NotifyHandler(BaseHandler):
    """调用通知类"""
    def post(self):
        pass

