import logging
import copy
import sys
import json

import requests


class NameSiloClient:


    def __init__(self, key) -> None:
        self._api_key = key


    def get_record(self, domain, length, sub_domain, record_type):

        try:
            url = f"https://www.namesilo.com/api/dnsListRecords?version=1&type=json&key={self._api_key}&domain={domain}"
            response = requests.get(url)
            response_body = response.json()
            if response.status_code == 200:
                res={}
                res["code"]=0
                res["data"]={}
                res["data"]["records"]=[]
                for record in response_body["reply"]["resource_record"]:
                    if record["type"] == record_type:
                        if sub_domain == "@":
                            if record["host"] == domain :
                                res["data"]["records"].append({'id':record["record_id"],'value':record['value'],'line':'默认'})
                        else:
                            if sub_domain+"."+domain == record["host"]:
                                res["data"]["records"].append({'id':record["record_id"],'value':record['value'],'line':'默认'})
                return res
            else:
                raise Exception('namesilo接口错误')

        except Exception as e:
            raise Exception('namesilo接口错误')
            
    def delete_record(self, domain,recordId):

        try:
            url = f"https://www.namesilo.com/api/dnsDeleteRecord?version=1&type=json&key={self._api_key}&domain={domain}&rrid={recordId}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception('namesilo接口错误')
        except Exception as e:
            raise Exception('namesilo接口错误')

    def create_record(self, domain, sub_domain, value, record_type,line, ttl):
        try:
            url = f"https://www.namesilo.com/api/dnsAddRecord?version=1&type=json&key={self._api_key}&domain={domain}&rrtype={record_type}&rrhost={sub_domain}&rrvalue={value}&rrttl={ttl}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception('namesilo接口错误')
        except Exception as e:
            raise Exception('namesilo接口错误')

    def change_record(self, domain, record_id, sub_domain,value, record_type, line,ttl):
        if sub_domain == "@":
            sub_domain = ""
        try:
            url = f"https://www.namesilo.com/api/dnsUpdateRecord?version=1&type=json&key={self._api_key}&domain={domain}&rrid={record_id}&rrhost={sub_domain}&rrvalue={value}&rrttl={ttl}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception('namesilo接口错误')
        except Exception as e:
            raise Exception('namesilo接口错误')