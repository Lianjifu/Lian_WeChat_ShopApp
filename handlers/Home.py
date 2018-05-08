# coding:utf-8
import json
import logging
import constants
from handlers.BaseHandler import BaseHandler
from static.data import data_index, data_detail

from utils.response_code import RET
from utils.utils import f_rsp, verify_request_body


class IndexHandler(BaseHandler):
    """提供首页展示信息"""
    def post(self):
        # get data display
        # _sql_home = "SELECT banner_img_url, bg_img_url FROM wxshop_home_img"
        # _sql_scenic = "SELECT scenic_id, product_img_url, scenic_city,scenic_selected,scenic_city_code FROM wxshop_scenic"

        # try:
        #     ret_home = self.db.query(_sql_home)
        #     ret_scenic = self.db.query(_sql_scenic)
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DBERR, errmsg="get scenic data error"))
        # if not ret_scenic or not ret_home:
        #     return self.write(dict(errcode=RET.NODATA, errmsg="no data"))
        # data = []
        # for row in ret_scenic:
        #     d = {
        #             "scenic_id": row.get("scenic_id"),
        #             "scenic_img_url": row.get("scenic_img_url"),
        #             "scenic_city":row.get("scenic_city"),
        #             "scenic_selected": row.get("scenic_selected"),
        #             "scenic_city_code": row.get("scenic_city_code")
        #     }
        #     data.append(d)
        # for r in ret_home:
        #     i = {
        #         "banner_img_url": r.get("banner_img_url"),
        #         "bg_img_url": r.get("bg_img_url")
        #     }
        #     data.append(i)

        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))

        self.write(dict(errcode=RET.OK, errmsg="OK", data=data_index))


class DetailHandler(BaseHandler):
    """商品的详情页"""
    def post(self):
        data = []
        # TODO 从body中获取数据
        ExpectParams = ["scenic_id"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write({"errcode": RET.PARAMERR, "errmsg": "params error"})
        scenic_id = str(RqstDt.get('scenic_id'))

        # try:
        #     _sql = "SELECT pi_product_id ,pi_product_name, pi_product_price,pi_product_type,pi_inventory_num FROM \
        #             wxshop_scenic as ws INNER JOIN wxshop_product_info as wpi ON ws.prodcut_id = wpi.pi_product_id WHERE scenic_id=%s"
        #     ret = self.db.query(_sql, scenic_id)
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DBERR, errmsg="get data error"))
        # if not ret:
        #     return self.write(dict(errcode=RET.NODATA, errmsg="no data "))
        #
        # for row in ret:
        #     d = {
        #         "scenic_id": scenic_id,
        #         "product_id": row.get("pi_product_id"),
        #         "product_name": row.get("pi_product_name"),
        #         "product_price": row.get("pi_product_price"),
        #         "product_type": row.get("pi_product_type"),
        #         "inventory_num": row.get("pi_inventory_num")
        #     }
        #     data.append(d)
        # try:
        #     product_id = row.get("pi_product_id")
        #     _sql_img = "SELECT pi_img_url FROM wxshop_product_img as wpim INNER JOIN  wxshop_product_info as wpin \
        #                 ON wpim.pi_product_img_url_id = wpin.pi_img_id WHERE pi_product_id = %s"
        #     ret_img = self.db.query(_sql_img, product_id)
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DBERR, errmsg="get data error"))
        #
        # if not ret_img:
        #     return self.write(dict(errcode=RET.NODATA, errmsg="no data "))
        #
        # for ri in ret_img:
        #     r = {
        #         "product_img_url": ri.get("pi_img_url")
        #     }
        #     data.append(r)


        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
        print scenic_id
        self.write(dict(errcode=RET.OK, errmsg="OK", data=data_detail))