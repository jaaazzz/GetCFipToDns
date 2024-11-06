import logging
import copy
import sys
import json

import requests


class NameSiloClient:


    def __init__(self, key) -> None:
        self._api_key = key


    def get_record(self, domain):

        try:
            url = f"https://www.namesilo.com/api/dnsListRecords?version=1&type=json&key={self._api_key}&domain={domain}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None
            
    def delete_record(self, domain,recordId):

        try:
            url = f"https://www.namesilo.com/api/dnsDeleteRecord?version=1&type=json&key={self._api_key}&domain={domain}&rrid={recordId}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None

    def create_record(self, domain, sub_domain, value, record_type, ttl):
        try:
            url = f"https://www.namesilo.com/api/dnsAddRecord?version=1&type=json&key={self._api_key}&domain={domain}&rrtype={record_type}&rrhost={sub_domain}&rrvalue={value}&rrttl={ttl}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None

    def change_record(self, domain, record_id, sub_domain, value, ttl):
        try:
            url = f"https://www.namesilo.com/api/dnsUpdateRecord?version=1&type=json&key={self._api_key}&domain={domain}&rrid={record_id}&rrhost={sub_domain}&rrvalue={value}&rrttl={ttl}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None