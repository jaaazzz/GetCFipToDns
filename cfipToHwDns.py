#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time
import requests
from dns.huawei import HuaWeiApi
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

#如果使用华为云解析 需要从API凭证-项目列表中获取
REGION_HW = 'cn-east-3'

#解析生效时间，默认为600秒
TTL = 600

#华为云后台获取 https://support.huaweicloud.com/devg-apisign/api-sign-provide-aksk.html
SECRETID = 'LTxxxxxxxxxxxxxxWcRDH'
SECRETKEY = 'LOitxxxxxxxxxxxxxxxxxxmzcGR'

if __name__ == '__main__':
    config = {'DOMAINS':DOMAINS,"AFFECT_NUM":AFFECT_NUM,"TTL":TTL,"DNS_SERVER":3}
    cloud = HuaWeiApi(SECRETID, SECRETKEY, REGION_HW)
    core = Core(cloud,config)
    core.main()
