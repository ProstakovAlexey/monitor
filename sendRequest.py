#!/usr/bin/python3
# -*- coding: utf-8 -*-

import http.client
import sys
import json


def sendRequest(addr, site, method=None, port=80):
    """
    :param addr: адрес сервиса
    :param port: порт
    :param site: название сайта
    :param method: метод
    :return: словарь ответа, описание ошибки
    """
    err = None
    result = None
    con = http.client.HTTPConnection(addr, port)
    # пытаемся отправить запрос
    if method:
        url = '/%s/cgi.py/%s' % (site, method)
    else:
        url = '/%s/cgi.py' % site
    try:
        con.request("GET", url)
        result = con.getresponse().read()
        result = result.decode('utf-8')
        result = json.loads(result, encoding='utf-8')
    except:
        Type, Value, Trace = sys.exc_info()
        err = """Не удалось обратится к сервису, возникли ошибки.
        Тип: %s,
        Значение:%s,
        Трассировка: %s""" % (Type, Value, Trace)
    return result, err