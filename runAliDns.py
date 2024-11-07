#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time
import requests
from dns.aliyun import AliApi
from dns.core import Core
from log import Logger
import traceback


#CM:移动 CU:联通 CT:电信  AB:境外 DEF:默认
#需要动态解析到Cf优选ip的域名和子域名
DOMAINS = {
    "vps789.com": {"@": ["CM","CU","CT"],"www": ["CM","CU","CT"]},
    "vpsxxx777.com": {"@": ["CM","CU","CT"]}
}

#解析生效条数
AFFECT_NUM = 2

#如果使用阿里云解析 REGION出现错误再修改 默认不需要修改 https://help.aliyun.com/document_detail/198326.html
REGION_ALI = 'cn-hongkong'

#解析生效时间，默认为600秒
TTL = 600

#阿里云后台获取 https://help.aliyun.com/document_detail/53045.html  注意需要添加DNS控制权限 AliyunDNSFullAccess
SECRETID = 'LTAIxxxxxxxxxxxxxxxxxxxWcRDH'
SECRETKEY = 'LOitxxxxxxxxxxxxxxxxxxxzcGR'

if __name__ == '__main__':
    config = {'DOMAINS':DOMAINS,"AFFECT_NUM":AFFECT_NUM,"TTL":TTL,"DNS_SERVER":2}
    cloud = AliApi(SECRETID, SECRETKEY,REGION_ALI)
    core = Core(cloud,config)
    core.main()
    