#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time
import requests
from dns.qCloud import QcloudApiv3 # QcloudApiv3 DNSPod 的 API 更新了 By github@z0z0r4
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
#免费的DNSPod相同线路最多支持2条解析
AFFECT_NUM = 2

#解析生效时间，默认为600秒 如果不是DNS付费版用户 不要修改!!!
TTL = 600

#腾讯云后台获取 https://console.cloud.tencent.com/cam/capi
SECRETID = 'LTAI5txxxxxxxxxxxxxxxxxcRDH'
SECRETKEY = 'LOixxxxxxxxxxxxxxxxx4mzcGR'

if __name__ == '__main__':
    config = {'DOMAINS':DOMAINS,"AFFECT_NUM":AFFECT_NUM,"TTL":TTL,"DNS_SERVER":1}
    cloud = QcloudApiv3(SECRETID, SECRETKEY)
    core = Core(cloud,config)
    core.main()