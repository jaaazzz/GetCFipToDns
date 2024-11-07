#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time
import requests
from dns.qCloud import QcloudApiv3 # QcloudApiv3 DNSPod 的 API 更新了 By github@z0z0r4
from dns.aliyun import AliApi
from dns.huawei import HuaWeiApi
from dns.nameSilo import NameSiloClient
from log import Logger
import traceback

class Core():

    log_cf2dns = Logger('cf2dns.log', level='debug')

    def __init__(self, cloud,config):
        self.cloud = cloud
        self.config = config

    def get_optimization_ip(self):
        try:
            headers = headers = {'Content-Type': 'application/json'}
            data = {}
            response = requests.post('https://vps789.com/public/sum/cfIpApi', json=data, headers=headers)
            if response.status_code == 200:
                self.log_cf2dns.logger.info("GET OPTIMIZATION IP SUCCESS" )
                return response.json()
            else:
                self.log_cf2dns.logger.error("GET OPTIMIZATION IP ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----MESSAGE: REQUEST STATUS CODE IS NOT 200")
                return None
        except Exception as e:
            self.log_cf2dns.logger.error("GETs OPTIMIZATION IP ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----MESSAGE: " + str(e))
            return None

    #s_info已存在的ip，c_info 最新的优选cfip
    def changeDNS(self,line, s_info, c_info, domain, sub_domain):
        recordType = "A"

        lines = {"CM": "移动", "CU": "联通", "CT": "电信", "AB": "境外", "DEF": "默认"}
        line = lines[line]
        print(s_info)
        print(c_info)
        try:
            create_num = self.config['AFFECT_NUM'] - len(s_info)
            # 如果线路能解析的ip已满，就用cfip一个一个去替换原来的ip解析            
            if create_num == 0:
                for info in s_info:
                    if len(c_info) == 0:
                        break
                    cf_ip = c_info.pop(random.randint(0,len(c_info)-1))["ip"]
                    if cf_ip in str(s_info):
                        continue
                    ret = self.cloud.change_record(domain, info["recordId"], sub_domain, cf_ip, recordType, line, self.config['TTL'])
                    if(self.config['DNS_SERVER'] != 1 or ret["code"] == 0):
                        self.log_cf2dns.logger.info("CHANGE DNS SUCCESS: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----RECORDID: " + str(info["recordId"]) + "----VALUE: " + cf_ip )
                    else:
                        self.log_cf2dns.logger.error("CHANGE DNS ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----RECORDID: " + str(info["recordId"]) + "----VALUE: " + cf_ip + "----MESSAGE: " + ret["message"] )
            # 如果线路还可以解析更多的ip，就添加cfip解析，直到用完            
            elif create_num > 0:
                for i in range(create_num):
                    if len(c_info) == 0:
                        break
                    cf_ip = c_info.pop(random.randint(0,len(c_info)-1))["ip"]
                    if cf_ip in str(s_info):
                        continue
                    ret = self.cloud.create_record(domain, sub_domain, cf_ip, recordType, line, self.config['TTL'])
                    if(self.config['DNS_SERVER'] != 1 or ret["code"] == 0):
                        self.log_cf2dns.logger.info("CREATE DNS SUCCESS: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----VALUE: " + cf_ip )
                    else:
                        self.log_cf2dns.logger.error("CREATE DNS ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----RECORDID: " + str(info["recordId"]) + "----VALUE: " + cf_ip + "----MESSAGE: " + ret["message"] )
            # 如果线路能解析的ip已超出配额，就用cfip一个一个去替换原来的ip解析            
            else:
                for info in s_info:
                    if create_num == 0 or len(c_info) == 0:
                        break
                    cf_ip = c_info.pop(random.randint(0,len(c_info)-1))["ip"]
                    if cf_ip in str(s_info):
                        create_num += 1
                        continue
                    ret = self.cloud.change_record(domain, info["recordId"], sub_domain, cf_ip, recordType, line, self.config['TTL'])
                    if(self.config['DNS_SERVER'] != 1 or ret["code"] == 0):
                        self.log_cf2dns.logger.info("CHANGE DNS SUCCESS: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----RECORDID: " + str(info["recordId"]) + "----VALUE: " + cf_ip )
                    else:
                        self.log_cf2dns.logger.error("CHANGE DNS ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+line+"----RECORDID: " + str(info["recordId"]) + "----VALUE: " + cf_ip + "----MESSAGE: " + ret["message"] )
                    create_num += 1
        except Exception as e:
                self.log_cf2dns.logger.error("CHANGE DNS ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----MESSAGE: " + str(e))

    def main(self):

        recordType = "A"
        if len(self.config['DOMAINS']) > 0:
            try:
                cfips = self.get_optimization_ip()
                if cfips == None or cfips["code"] != 0:
                    self.log_cf2dns.logger.error("GET CLOUDFLARE IP ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----MESSAGE: " + str(cfips["data"]))
                    return
                cf_cmips = cfips["data"]["CM"]
                cf_cuips = cfips["data"]["CU"]
                cf_ctips = cfips["data"]["CT"]
                cf_defips = cfips["data"]["AllAvg"]
                for domain, sub_domains in self.config['DOMAINS'].items():
                    for sub_domain, lines in sub_domains.items():
                        if self.config['DNS_SERVER'] == 4 and len(lines)!=1:
                            self.log_cf2dns.logger.info("域名解析为NameSilo时，线路只能填DEF")
                            return

                        #下面5个数组存的是不同线路最新获取的优选IP列表                        
                        temp_cf_cmips = cf_cmips.copy()
                        temp_cf_cuips = cf_cuips.copy()
                        temp_cf_ctips = cf_ctips.copy()
                        temp_cf_abips = cf_ctips.copy()
                        temp_cf_defips = cf_defips.copy()
                        if self.config['DNS_SERVER'] == 1:
                            ret = self.cloud.get_record(domain, 20, sub_domain, "CNAME")
                            if ret["code"] == 0:
                                for record in ret["data"]["records"]:
                                    if record["line"] == "移动" or record["line"] == "联通" or record["line"] == "电信":
                                        retMsg = self.cloud.del_record(domain, record["id"])
                                        if(retMsg["code"] == 0):
                                            self.log_cf2dns.logger.info("DELETE DNS SUCCESS: ----Time: "  + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+record["line"] )
                                        else:
                                            self.log_cf2dns.logger.error("DELETE DNS ERROR: ----Time: "  + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----DOMAIN: " + domain + "----SUBDOMAIN: " + sub_domain + "----RECORDLINE: "+record["line"] + "----MESSAGE: " + retMsg["message"] )
                        ret = self.cloud.get_record(domain, 100, sub_domain, recordType)
                        # ret["code"] == 0 就是self.config['DNS_SERVER'] == 1
                        if self.config['DNS_SERVER'] != 1 or ret["code"] == 0 :
                            if self.config['DNS_SERVER'] == 1 and "Free" in ret["data"]["domain"]["grade"] and self.config['AFFECT_NUM'] > 2:
                                self.config['AFFECT_NUM'] = 2
                            #下面5个数组存的是已存在的DNS解析列表                            
                            cm_info = []
                            cu_info = []
                            ct_info = []
                            ab_info = []
                            def_info = []
                            for record in ret["data"]["records"]:
                                info = {}
                                info["recordId"] = record["id"]
                                info["value"] = record["value"]
                                if record["line"] == "移动":
                                    cm_info.append(info)
                                elif record["line"] == "联通":
                                    cu_info.append(info)
                                elif record["line"] == "电信":
                                    ct_info.append(info)
                                elif record["line"] == "境外":
                                    ab_info.append(info)
                                elif record["line"] == "默认":
                                    def_info.append(info)
                            for line in lines:
                                if line == "CM":
                                    self.changeDNS("CM", cm_info, temp_cf_cmips, domain, sub_domain)
                                elif line == "CU":
                                    self.changeDNS("CU", cu_info, temp_cf_cuips, domain, sub_domain)
                                elif line == "CT":
                                    self.changeDNS("CT", ct_info, temp_cf_ctips, domain, sub_domain)
                                elif line == "AB":
                                    self.changeDNS("AB", ab_info, temp_cf_abips, domain, sub_domain)
                                elif line == "DEF":
                                    self.changeDNS("DEF", def_info, temp_cf_defips, domain, sub_domain)
            except Exception as e:
                traceback.print_exc()
                self.log_cf2dns.logger.error("CHANGE DNS ERROR: ----Time: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "----MESSAGE: " + str(e))