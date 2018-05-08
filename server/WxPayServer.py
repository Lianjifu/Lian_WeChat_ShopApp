# encoding=utf-8

"""
* 微信支付接口Python-SDK
* ====================
* 【请求型接口】 --WxPayClient
*  统一下单：UnifiedOrder
*  查询订单：OrderQuery
*  申请退款：Refund
*  查询退款：RefundQuery
*  对账单接口：DownloadBill
* 【相应型接口】 --WxPayServer
*  通知：Notify
"""
import hashlib
import json
import random
import uuid

from urllib import quote
import xml.etree.cElementTree as ET
import time
import datetime

import requests

from server.WxPayConfig import WxPayConf


class RequestClient(object):
    """使用urlib2发送请求"""

    def get(self, url, second=30):
        return self.postXml(None, url, second)

    def postXml(self, url, xml, second=30):
        """不使用证书"""
        req_headers = {'Content-Type': 'application/xml'}
        data = requests.request(url, data=xml, headers=req_headers, timeout=second)
        data.encoding = "utf-8"
        return data.text

    def postXmlSSL(self, xml, url, second=30):
        """使用证书"""
        # 设置证书
        # 使用证书：cert 与 key 分别属于两个.pem文件
        req_headers = {'Content-Type': 'application/xml'}
        data = requests.request(url,
                                data=xml,
                                headers=req_headers,
                                cert=(WxPayConf.SSLCERT_PATH, WxPayConf.SSLKEY_PATH),
                                timeout=second)

        data.encoding = "utf-8"
        return data.text


class CommonUtil(object):
    """所有接口的基类"""

    def trimString(self, value):
        if value is not None and len(value) == 0:
            value = None
        return value

    def creatNoncestr(self):
        """产生随机字符串"""
        return str(uuid.uuid4()).replace('-', '')

    def formatted_parameter(self, paraMap, urlencode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = quote(paraMap[k] if urlencode else paraMap[k])
            buff.append("{0}={1}".format(k, v))
        return "&".join(buff)

    def create_sign(self, param):
        """生成签名"""
        # 按字典序排序参数
        String = self.formatted_parameter(param, False)
        # 添加商户key
        String = "{0}&key={1}".format(String, WxPayConf.Merchant_key)
        # MD5 加密
        String = hashlib.md5(String).hexdigest()
        sign_ = String.upper()
        return sign_

    def dict_to_xml(self, dict_data):
        """dict转xml"""
        xml = ["<xml>"]
        for k, v in dict_data.iteritems():
            xml.append("<{0}>{1}</{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xml_to_dict(self, xml_data):
        """将xml转为dict"""
        xml_dict = {}
        root = ET.fromstring(xml_data)
        for child in root:
            xml_data[child.tag] = child.text
        return xml_dict

    def postXmlCurl(self, xml, url, second=30):
        """以post方式提交xml到对应的接口url"""
        return RequestClient().postXml(xml, url, second=second)

    def postXmlSSLCurl(self, xml, url, second=30):
        """使用证书，以post方式提交xml到对应的接口url"""
        return RequestClient().postXmlSSL(xml, url, second=second)


class InvokePay(CommonUtil):
    """调用支付接口"""
    code = None
    openid = None  # 用户的openid
    parameters = None  # jsapi参数，格式为json
    prepay_id = None  # 使用统一支付接口得到预支付id
    curl_timeout = None  # curl超时时间

    def __init__(self, timeout=WxPayConf.CURL_TIMEOUT):
        self.curl_timeout = timeout

    def create_url_for_openid(self,code):
        """生成可以获得openid的url"""
        data = {
            "appid": WxPayConf.AppId,
            "secret": WxPayConf.AppSecret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        biz_String = self.formatted_parameter(data, False)
        return "https://api.weixin.qq.com/sns/jscode2session?" + biz_String

    def getOpenid(self,code):
        """通过curl向微信提交code，以获取openid"""
        url = self.create_url_for_openid(code)
        data = RequestClient.get(url)
        self.openid = json.loads(data)["openid"]
        return self.openid

    def setPrepayId(self, prepayId):
        """设置prepay_id"""
        self.prepay_id = prepayId

    def getParameters(self):
        """设置jsapi的参数"""
        paySign_data = {
            "appid": WxPayConf.AppId,
            "timeStamp": int(time.time()),
            "nonceStr": self.creatNoncestr(),
            "package": "prepay_id={0}".format(self.prepay_id),
            "signType": "MD5"
        }
        sign = self.create_sign(paySign_data)
        paySign_data['sign'] = sign
        paySign_data.pop("appid")
        paySign_data['paySign'] = paySign_data

        self.parameters = json.dumps(paySign_data)
        return self.parameters


class WxPayClient(CommonUtil):
    """请求型接口的基类"""
    response = None  # 微信返回的响应
    url = None  # 接口链接
    curl_timeout = None  # curl超时时间

    def __init__(self):
        self.parameters = {}  # 请求参数，类型为关联数组
        self.result = {}  # 返回参数，类型为关联数组

    def setParameter(self, parameter, parameterValue):
        """设置请求参数"""
        self.parameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createXml(self):
        """设置标配的请求参数，生成签名，生成接口参数xml"""
        self.parameters["appid"] = WxPayConf.AppId  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf.MchId  # 商户号
        self.parameters["nonce_str"] = self.creatNoncestr()  # 随机字符串
        self.parameters["sign"] = self.create_sign(self.parameters)  # 签名
        return self.dict_to_xml(self.parameters)

    def postXml(self):
        """post请求xml"""
        xml = self.createXml()
        self.response = self.postXmlCurl(self.url, xml, self.curl_timeout)
        return self.response

    def postXmlSSL(self):
        """使用证书post请求xml"""
        xml = self.createXml()
        self.response = self.postXmlSSLCurl(self.url, xml, self.curl_timeout)
        return self.response

    def getResult(self):
        """获取结果，默认不使用证书"""
        self.postXml()
        self.result = self.xml_to_dict(self.response)
        return self.result


class UnifiedOrder(WxPayClient):
    """统一支付接口类"""

    def __init__(self, timeout=WxPayConf.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        self.curl_timeout = timeout
        super(UnifiedOrder, self).__init__()

    def createXml(self):
        """生成接口参数xml"""

        if any(self.parameters[key] is None for key in
               ("openid", "out_trade_no", "body", "total_fee")):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf.AppId
        self.parameters["mch_id"] = WxPayConf.MchId
        self.parameters["nonce_str"] = self.creatNoncestr()
        self.parameters["spbill_create_ip"] = "127.0.0.1"  # 终端IP
        self.parameters["notify_url"] = "http://"  # 通知地址
        self.parameters["trade_type"] = "JSAPI"  #
        self.parameters["sign"] = self.create_sign(self.parameters)

        self.xml = self.dict_to_xml(self.parameters)
        return self.xml

    def getPrepayId(self):
        """获取prepay_id"""
        self.postXml()
        self.result = self.xml_to_dict(self.response)
        if self.result["return_code"].upper() == "SUCCESS" and self.result["result_code"].upper() == "SUCCESS":
            prepay_id = self.result["prepay_id"]
            return prepay_id
        else:
            return None


class OrderQuery(WxPayClient):
    """查询订单"""

    def __init__(self, timeout=WxPayConf.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/orderquery"
        # 设置curl超时时间
        self.curl_timeout = timeout
        super(OrderQuery, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        # 检测必填参数
        if all(self.parameters.get(key) is None for key in ("out_trade_no", "transaction_id",)):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf.AppId  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf.MchId  # 商户号
        self.parameters["nonce_str"] = self.creatNoncestr()  # 随机字符串
        self.parameters["out_trade_no"] = ""  # 商户订单号
        self.parameters["sign"] = self.create_sign(self.parameters)  # 签名
        xml = self.dict_to_xml(self.parameters)
        return xml


class CloseOrder(WxPayClient):
    def __init__(self, timeout=WxPayConf.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/closeorder"
        # 设置curl超时时间
        self.curl_timeout = timeout
        super(CloseOrder, self).__init__()

    def createXml(self):
        """生成接口参数xml"""

        self.parameters["appid"] = WxPayConf.AppId  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf.MchId  # 商户号
        self.parameters["nonce_str"] = self.creatNoncestr()  # 随机字符串
        self.parameters["out_trade_no"] = ""  # 商户订单号
        self.parameters["sign"] = self.create_sign(self.parameters)  # 签名
        return self.dict_to_xml(self.parameters)


class Refund(WxPayClient):
    """申请退款类"""

    def __init__(self, timeout=WxPayConf.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/secapi/pay/refund"
        # 设置curl超时时间
        self.curl_timeout = timeout
        super(Refund, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in
               ("out_trade_no", "out_refund_no", "total_fee", "refund_fee")):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf.AppId  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf.MchId  # 商户号
        self.parameters["nonce_str"] = self.creatNoncestr()  # 随机字符串
        self.parameters["sign"] = self.create_sign(self.parameters)  # 签名
        return self.dict_to_xml(self.parameters)

    def getResult(self):
        """ 获取结果，使用证书通信(需要双向证书)"""
        self.postXmlSSL()
        self.result = self.xml_to_dict(self.response)
        return self.result


class RefundQuery(WxPayClient):
    """查询退款接口"""

    def __init__(self, timeout=WxPayConf.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/refundquery"
        # 设置curl超时时间
        self.curl_timeout = timeout
        super(RefundQuery, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in
               ("out_refund_no", "out_trade_no", "transaction_id", "refund_id")):
            raise ValueError("missing parameter")
        self.parameters["appid"] = WxPayConf.AppId  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf.MchId  # 商户号
        self.parameters["nonce_str"] = self.creatNoncestr()  # 随机字符串
        self.parameters["sign"] = self.create_sign(self.parameters)  # 签名
        return self.dict_to_xml(self.parameters)

    def getResult(self):
        """ 获取结果，使用证书通信(需要双向证书)"""
        self.postXmlSSL()
        self.result = self.xml_to_dict(self.response)
        return self.result


class DownloadBill(WxPayClient):
    """对账单接口"""

    def __init__(self, timeout=WxPayConf.CURL_TIMEOUT):
        # 设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/downloadbill"
        # 设置curl超时时间
        self.curl_timeout = timeout
        super(DownloadBill, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in ("bill_date",)):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf.AppId  # 公众账号ID
        self.parameters["mch_id"] = WxPayConf.MchId  # 商户号
        self.parameters["nonce_str"] = self.creatNoncestr()  # 随机字符串
        self.parameters["sign"] = self.create_sign(self.parameters)  # 签名
        return self.dict_to_xml(self.parameters)

    def getResult(self):
        """获取结果，默认不使用证书"""
        self.postXml()
        self.result = self.xml_to_dict(self.response)
        return self.result


class WxPayServer(CommonUtil):
    """响应型接口基类"""
    SUCCESS, FAIL = "SUCCESS", "FAIL"

    def __init__(self):
        self.data = {}  # 接收到的数据，类型为关联数组
        self.returnParameters = {}  # 返回参数，类型为关联数组

    def save_data(self, xml):
        """将微信的请求xml转换成字典，以方便数据处理"""
        self.data = self.xml_to_dict(xml)

    def check_sign(self):
        """校验签名"""
        tmpData = dict(self.data)  # make a copy to save sign
        del tmpData['sign']
        sign = self.create_sign(tmpData)  # 本地签名
        if self.data['sign'] == sign:
            return True
        return False

    def get_data(self):
        """获取微信的请求数据"""
        return self.data

    def set_return_parameter(self, parameter, parameterValue):
        """设置返回微信的xml数据"""
        self.returnParameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createXml(self):
        """生成接口参数xml"""
        return self.dict_to_xml(self.returnParameters)

    def returnXml(self):
        """将xml数据返回微信"""
        returnXml = self.createXml()
        return returnXml


class Notify(WxPayServer):
    """通用通知接口"""
