# -*- coding: utf-8 -*-
import sys
import codecs
import os
import csv
import datetime
import getInfo

"""
Веб-сервис, принимает название вида сведений как GET параметр,
возвращает по нему результат или ошибку. Возможные виды сведений
requestSmev - кол-во отравленных в СМЭВ запросов
requestPGU - кол-во принятых с ПГУ/МФЦ заявлений
responsePGU - кол-во возвращенных на ПГУ/МФЦ статусов
responseSmev - кол-во ответов на СМЭВ запросы
test - тестовый запрос, позвращает результат = 10

Пример ответа (тест) http://127.0.0.1/monitor?method=test:
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
Пример ответа (данные) http://127.0.0.1/monitor:
            {
                "date": "16.01.2017 13:40:53",
                "errorCode": 0,
                "errorMessage": "",
                "info": {
                    "requestPGU": 584,
                    "requestSmev": 534,
                    "responsePGU": 0,
                    "responseSmev": 0
                  }
            }
"""


sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
param = os.environ['REQUEST_URI'].split('/')

#param = ('127.0.0.1', 'monitor', 'app.py', 'error')


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
                    print('В файле с кодами ошибок попалась не форматная строка. Нужно писать: 99; Описание ошибоки')
    else:
        result['info'] = data
    return result


# возможно пришло 3 параметра
# Нормальный вызов - http://127.0.0.1/monitor/app.py/
# Тестовый вызов - http://127.0.0.1/monitor/app.py/test
# Ошибка - http://127.0.0.1/monitor/app.py/err
data_dict = dict()
err = 0

if len(param) == 3:
    # Пустой, значить надо ответить все
    data_dict, err = getInfo.getResult()
elif len(param) > 3:
    method = param[3]
    if method == 'test':
        # Это метод для тестирование, он всегда возвращает такой результат
        data_dict['test'] = 20
    elif method == 'error':
        err = 42
    else:
        err = 2

result = str(response(err, data_dict)).replace('\'', '\"')
print("Content-Type: application/json; charset=utf-8")
print("Cache-control: max-age=600")
print("Content-Length:", len(result.encode('utf-8')))
print()
print(result)
