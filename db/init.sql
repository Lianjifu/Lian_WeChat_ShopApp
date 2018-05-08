
CREATE TABLE `ywgsh_wxshop_dev`.`wxshop_home_img` (
  `home_id` INT NOT NULL AUTO_INCREMENT,
  `banner_img_url` VARCHAR(256) NULL,
  `bg_img_url` VARCHAR(256) NULL,
  PRIMARY KEY (`home_id`));


CREATE TABLE `ywgsh_wxshop_dev`.`wxshop_scenic` (
  `scenic_id` INT NOT NULL AUTO_INCREMENT COMMENT '景区id',
  `scenic_img_url` VARCHAR(256) NOT NULL COMMENT '景区图片',
  `scenic_city` VARCHAR(45) NOT NULL COMMENT '景区城市',
  `scenic_city_code` VARCHAR(45) NOT NULL COMMENT '景区城市代码',
  `scenic_selected` TINYINT NOT NULL DEFAULT 0 COMMENT '是否景区精选，0-不是，1-是' ,
  PRIMARY KEY (`scenic_id`));

CREATE TABLE `ywgsh_wxshop_dev`.`wxshop_user_profile` (
  `up_user_id` INT NOT NULL AUTO_INCREMENT,
  `up_mobile` CHAR(11) NOT NULL COMMENT '手机号',
  `up_avatar` VARCHAR(128) NULL COMMENT '用户头像',
  `up_ctime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `up_utime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`up_user_id`),
  UNIQUE INDEX `up_mobile_UNIQUE` (`up_mobile` ASC));


CREATE TABLE `ywgsh_wxshop_dev`.`wxshop_order_info` (
  `oi_order_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '订单id',
  `oi_user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户id',
  `oi_goods_id` BIGINT UNSIGNED NOT NULL COMMENT '商品id',
  `oi_goods_name` VARCHAR(45) NOT NULL COMMENT '商品名称',
  `oi_goods_price` INT UNSIGNED NOT NULL COMMENT '商品价格',
  `oi_goods_num` INT UNSIGNED NOT NULL COMMENT '商品数量',
  `oi_goods_price_total` INT NOT NULL COMMENT '商品总价',
  `oi_addr_info` VARCHAR(256) NOT NULL COMMENT '地址信息',
  `oi_status` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '订单状态,0-未付款，1-待收货，2-已完成',
  `oi_ctime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `oi_utime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`oi_order_id`));


CREATE TABLE `ywgsh_wxshop_dev`.`wxshop_address_info` (
  `ai_addr_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '地址id',
  `ai_user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `ai_token` VARCHAR(100) NOT NULL COMMENT 'token值',
  `ai_link_addr` VARCHAR(100) NOT NULL COMMENT '联系人地址',
  `ai_link_man` VARCHAR(45) NOT NULL COMMENT '联系人',
  `ai_link_phone` CHAR(11) NOT NULL COMMENT '联系人手机号',
  `ai_default_addr` TINYINT NOT NULL DEFAULT 0 COMMENT '是否默认地址，0-不是，1-是',
  PRIMARY KEY (`ai_addr_id`));


CREATE TABLE `ywgsh_wxshop_dev`.`wxshop_goods_info` (
  `gi_goods_id` INT NOT NULL AUTO_INCREMENT,
  `gi_goods_name` VARCHAR(45) NOT NULL COMMENT '商品名称',
  `gi_goods_price` INT NOT NULL COMMENT '商品价格',
  `gi_goods_type` VARCHAR(45) NOT NULL COMMENT '商品类型',
  `gi_goods_num` INT NOT NULL COMMENT '商品数量',
  `gi_goods_img_url` VARCHAR(45) NOT NULL COMMENT '商品图片',
  PRIMARY KEY (`gi_goods_id`));


CREATE TABLE `ywgsh_wxshop_dev`.`wxshop_express` (
  `e_express_id` INT NOT NULL,
  `e_province` VARCHAR(45) NOT NULL COMMENT '省份',
  `e_express` VARCHAR(45) NOT NULL COMMENT '运费',
  PRIMARY KEY (`e_express_id`));


CREATE TABLE `ywgsh_wxshop_dev`.`wxshop_user_sms` (
  `us_id` INT NOT NULL AUTO_INCREMENT,
  `us_mobile` INT(11) NOT NULL,
  `us_sms` INT(6) NOT NULL,
  PRIMARY KEY (`us_id`));
