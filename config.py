# coding:utf-8

import os

# Application配置参数
settings = dict(
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        # cookie_secret="FhLXI+BRRomtuaG47hoXEg3JCdi0BUi8vrpWmoxaoyI=",
        # xsrf_cookies=True,
        debug=True
    )


# 数据库配置参数
mysql_options = dict(
    host="rm-bp1woxm70a39b9lixo.mysql.rds.aliyuncs.com",
    database="ywgsh_wxshop_dev",
    user="ywgsh_wxs_root",
    password="Wxs2018",
)

# # Redis配置参数
# redis_options = dict(
#     host="127.0.0.1",
#     port=6379
# )

# 日志配置
log_path = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"

# access_token
token = "dsfdCjaTXQdX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="


