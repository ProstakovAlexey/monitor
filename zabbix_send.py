# -*- coding: utf-8 -*-
from zabbix.api import ZabbixAPI
from pyzabbix import ZabbixMetric, ZabbixSender

# Create ZabbixAPI class instance
zapi = ZabbixAPI(url='http://192.168.0.18/zabbix/', user='Prostakov', password='fish13')

# Get all monitored hosts
result1 = zapi.host.get(monitored_hosts=1, output='extend')

packet = [
  ZabbixMetric('lip', 'trap', "2"),

]

result = ZabbixSender(use_config=True).send(packet)

# Filter results
hostnames1 = [host['host'] for host in result1]
print(hostnames1)