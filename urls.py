# coding:utf8

'''web解析规则'''

from handlers import Home
from handlers import Passport
from handlers import Address
from handlers import Orders

urls = [
    (r'/api/wxshop/index',  Home.IndexHandler),
    (r"/api/wxshop/detail",  Home.DetailHandler),
    (r"/api/wxshop/register", Passport.RegisterHandler),
    (r"/api/wxshop/login", Passport.LoginHandler),
    (r"/api/wxshop/address", Address.AddressHandler),
    (r"/api/wxshop/new_address", Address.NewAddressHandler),
    (r"/api/wxshop/order",  Orders.OrderHandler),
    (r"/api/wxshop/submit_order", Orders.SubmitOrderHandler),
    # (r"/api/wxshop/ensure_order", Orders.EnsureOrderHandler),
    (r"/api/wxshop/cancel_order", Orders.CancelOrderHandler),
   ]