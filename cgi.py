# -*- coding: utf-8 -*-
import sys
import codecs
import os
import csv
import datetime
import getInfo
import json
import time

"""
Веб-сервис, возвращает по нему результат (виды сведений) или ошибку.
Виды сведений:
    - requestSmev - кол-во отравленных в СМЭВ запросов
    - requestPGU - кол-во принятых с ПГУ/МФЦ заявлений
    - responsePGU - кол-во возвращенных на ПГУ/МФЦ статусов
    - responseSmev - кол-во ответов на СМЭВ запросы
    - test - тестовый запрос, позвращает результат = 10
    - loadToASP - Выгрузка с ТИ
    - loadToTI - загрузка на ТИ

Нормальный вызов - http://127.0.0.1/monitor/cgi.py
Ошибка - http://127.0.0.1/monitor/cgi.py/error
Тестовый вызов - http://127.0.0.1/monitor/cgi.py/test

Пример ответа (данные):
            {
                "date": "16.01.2017 13:40:53",
                "errorCode": 0,
                "errorMessage": "",
                "info": {
                    "requestPGU": 584,
                    "requestSmev": 534,
                    "responsePGU": 0,
                    "responseSmev": 0,
                    "loadToASP": 0,
                    "loadToTI": 0
                  }
            }
"""


def get_err_message(dict_res):
    """
    Получает готовый словарь результата, заполняет в нем сообщение об ошибки
    :param dict_res:
    :return: возвращает словарь с проставив в него сообщение об ошибке
    """
    if dict_res['errorCode'] == 0:
        dict_res['errorMessage'] = ""
    else:
        dict_res['errorMessage'] = 'Неизвестный код ошибки'
        with open('errorCode.txt', 'r', encoding='utf-8') as csvfile:
            lines = csv.reader(csvfile, delimiter=';')
            for row in lines:
                try:
                    if int(row[0]) == err:
                        # Нашли соответствие кода
                        dict_res['errorMessage'] = row[1].strip()
                        break
                except:
                    print('В файле с кодами ошибок попалась не форматная строка. Нужно писать: 99; Описание ошибки')
    return dict_res


def response():
    """
    Готовит ответ в полном формате и записывает его в кэш
    :return: возвращает словарь данными
    """
    # Сразу заполним дату
    res = dict(date=datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y %H:%M:%S'))
    # Заполним блок с информацией и код ошибки
    res['info'], res['errorCode'] = getInfo.getResult()
    # Заполним сообщение об ошибке
    res = get_err_message(res)
    # Сохранить в кэш
    save_json_cache(res)
    return res


def save_json_cache(json_data):
    """
    Сохраняет в кэш результат
    :param json:
    :return:
    """
    # Делаю абсолютный путь, исходя из того, где лежит данный файл
    cache_name = os.path.join(os.getcwd(), 'cache.json')
    with open(cache_name, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    # Нужно, чтобы отвечал в UTF-8
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    # Получает параметры, переданные веб-сервером.
    # Пример списка с параметрами param = ('127.0.0.1', 'monitor', 'cgi.py', 'error')
    param = os.environ['PATH_INFO'].split('/')
    err = 0
    result = None
    # Пустой, значить надо ответить все
    if len(param) == 3:
        cache_name = 'cache.json'
        # Проверить, есть ли кэш и не старше ли он 10 минут
        if os.access(cache_name, os.F_OK) and ((time.time() - os.path.getmtime(cache_name))/60 < 10):
            # Прочитать его
            try:
                with open(cache_name, 'r', encoding='utf-8') as json_file:
                    result = json.loads(json_file.read(), encoding='utf-8')
            except:
                # При чтении файла или его разборе в XML возникли ошибки, кэш кто-то подпортил. Получим новый результат.
                result = response()
        else:
            # Получаем ответ, при получении он так же записывается в кэш
            result = response()
    # Есть какие-то параметры
    elif len(param) > 3:
        method = param[3]
        # Это метод для тестирование, он всегда возвращает результат = 20
        if method == 'test':
            result = dict(date=datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y %H:%M:%S'),
                          errorCode=0,
                          info=dict(test=20)
                          )
            result = get_err_message(result)
        # Это метод для тестирования всегда возращает ошибку с кодом 42
        elif method == 'error':
            result = dict(date=datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y %H:%M:%S'),
                          errorCode=42
                          )
            result = get_err_message(result)
        # Неизвестный метод, код ошибки 2
        else:
            result = dict(date=datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y %H:%M:%S'),
                          errorCode=2
                          )
            result = get_err_message(result)

    # Преобразуем результат в строку
    result = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
    # Добавляем заголовки
    print("Content-Type: application/json; charset=utf-8")
    print("Content-Length:", len(result.encode('utf-8')))
    print("Cache-control:", "no-cache")
    print()
    # Возврат результата
    print(result)
