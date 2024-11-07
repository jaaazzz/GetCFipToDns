#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time
import requests
from dns.nameSilo import NameSiloClient
from dns.core import Core
from log import Logger
import traceback


#CM:移动 CU:联通 CT:电信  AB:境外 DEF:默认
#需要动态解析到Cf优选ip的域名和子域名#NameSilo不支持多线解析，只能选DEF默认线路
DOMAINS = {
    "vps789.com": {"@": ["DEF"],"www":["DEF"]},
    "vpsxxx777.com": {"@": ["DEF"]},
}

#解析生效条数
AFFECT_NUM = 2

#解析生效时间，NameSilo最少为3600
TTL = 3600

#NameSilo后台获取 https://www.namesilo.com/account/api-manager NameSilo只用填SECRETKEY即可
SECRETKEY = '72xxxxxxxxxxxxa332'

if __name__ == '__main__':
    config = {'DOMAINS':DOMAINS,"AFFECT_NUM":AFFECT_NUM,"TTL":TTL,"DNS_SERVER":4}
    cloud = NameSiloClient(SECRETKEY)
    core = Core(cloud,config)
    core.main()