# -*- coding: utf-8 -*-
import sys
import codecs
import os
import csv
import datetime
import getInfo
import json

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

Пример ответа (тест):
            {
                "error": {
                    "errorCode": 0,
                    "errorMessage": ""
                },
                "result": {
                    "date": "03.12.2016 20:53:57",
                    "info": {"test": 10,}
                }
            }
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

# Нужно, чтобы отвечал в UTF-8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# Получает параметры, переданные веб-сервером
param = os.environ['PATH_INFO'].split('/')
# Пример списка с параметрами param = ('127.0.0.1', 'monitor', 'cgi.py', 'error')


def response(err, data):
    """
    Готовит структуру для ответа, если есть ошибка то добавляет ее описание.
    :param err: код ошибки
    :param data: данные ответа
    :return: err_d, res_d
    """

    result = dict(date=datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y %H:%M:%S'),
                  errorCode=err, errorMessage='')
    if err:
        # Есть ошибка, поищем сообщение о ней в файле
        result['errorMessage'] = 'Неизвестный код ошибки'
        with open('errorCode.txt', 'r', encoding='utf-8') as csvfile:
            lines = csv.reader(csvfile, delimiter=';')
            for row in lines:
                try:
                    if int(row[0]) == err:
                        # Нашли соответствие кода
                        result['errorMessage'] = row[1].strip()
                        break
                except:
                    print('В файле с кодами ошибок попалась не форматная строка. Нужно писать: 99; Описание ошибки')
    else:
        result['info'] = data
    return result


def save_json_cache(json_data):
    """
    Сохраняет в кэш результат
    :param json:
    :return:
    """
    cache_name = 'cache.json'
    with open(cache_name, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))


data_dict = dict()
err = 0
result = None


if len(param) == 3:
    # Пустой, значить надо ответить все
    # Проверить, есть ли старый кэш
    cache_name = 'cache.json'
    if os.access(cache_name, os.F_OK):
        # Прочитать его
        try:
            with open(cache_name, 'r', encoding='utf-8') as json_file:
                json_cache = json.loads(json_file.read(), encoding='utf-8')
            t = datetime.datetime.strptime(json_cache['date'], '%d.%m.%Y %H:%M:%S')
            if t + datetime.timedelta(minutes=30) < datetime.datetime.now():
                # Кэш устарел, надо сделать новый запрос и новый кэш
                data_dict, err = getInfo.getResult()
                save_json_cache(response(err, data_dict))
            else:
                # Кэш найден и он не страрый, берем его
                result = json_cache
        except:
            # Прочитать не удалось, делаем новый кэш
            data_dict, err = getInfo.getResult()
            save_json_cache(response(err, data_dict))
    else:
        # Файла кэша нет, делаем его
        data_dict, err = getInfo.getResult()
        save_json_cache(response(err, data_dict))


elif len(param) > 3:
    method = param[3]
    if method == 'test':
        # Это метод для тестирование, он всегда возвращает такой результат
        data_dict['test'] = 20
    elif method == 'error':
        err = 42
    else:
        err = 2
# Проверить, возможно результат взяли из кэше
if result:
    result = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
else:
    # Получим результат запросом
    result = json.dumps(response(err, data_dict), sort_keys=True, indent=4, separators=(',', ': '))
print("Content-Type: application/json; charset=utf-8")
print("Cache-control: max-age=1200")
print("Cache-control: min-fresh=600")
print("Content-Length:", len(result.encode('utf-8')))
print()
print(result)
