#!/usr/bin/python

import consul
import syslog
import os
import subprocess


class PreInit(object):
    """
    This class to put scheme into the Consul key/value storage for Keepalived and Consul template.
    @param env CONSUL_SERVICE_NAME - the dns name of consul service. Default: consul

    @param env VIRTUAL_IP - floating IP that each LoadBlaancer will share.
    """
    consul_service = os.environ.get("CONSUL_ADDR", "consul")
    ha_main_key = "services/"
    ha_key = ha_main_key + "lwm2ms/weight"
    kv_data = {
        ha_main_key: [
            {"vip": os.environ.get("VIRTUAL_IP", "192.168.1.100")},
            {"mqtt/": [
                {"tcp_check": "3"},
                {"ports": "1883"},
                {"weight": "100"},
            ]},
            {"lwm2ms/": [
                {"misc_check": "/etc/keepalived/coap_check.sh"},
                {"tcp_check": "3"},
                {"weight": "100"},
                {"ports": "8080/5683/5684"},
            ]},
            {"feed/": [
                {"tcp_check": "3"},
                {"weight": "100"},
                {"ports": "15672"},
            ]},
            {"kibana/": [
                {"tcp_check": "3"},
                {"ports": "5601"},
                {"weight": "100"},
            ]},
            {"uchiwa/": [
                {"tcp_check": "3"},
                {"ports": "3000"},
                {"weight": "100"},
            ]},
        ],
    }

    def __init__(self):
        self.consul_cluster_client = None
        self.run()

    def run(self):
        self.consul_cluster_client = consul.Consul(self.consul_service)
        self._init_ha_kv()

    def _init_ha_kv(self):
        """posts kv to the consul storage"""
        try:
            ha_kv = self.consul_cluster_client.kv.get(self.ha_key)[1]
            if not ha_kv:
                for item in self.kv_data[self.ha_main_key]:
                    key = item.keys()[0]
                    value = item[key]
                    if isinstance(value, list):
                        for sub_item in value:
                            sub_key = sub_item.keys()[0]
                            sub_value = sub_item[sub_key]
                            self._put_data(key + sub_key, sub_value)
                    else:
                        self._put_data(key, value)
            else:
                syslog.syslog(syslog.LOG_INFO,
                              "HA KV Pre-init: HAProxy key/value " + self.ha_main_key + " already exists.")
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, "HA KV Pre-init:_init_ha_kv Error: " + e.__str__())

    def _put_data(self, key, value):
        return self.consul_cluster_client.kv.put(self.ha_main_key + key, str(value), cas=0)


if __name__ == "__main__":
    f = PreInit()
