#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sendRequest
import argparse
import logging
import time
import os


""" Отправляет запрос на получение данных из протокола. Метода получает как входной параметр, результат запроса
выдает к ком. строку. -1 - ошибка, иначе число больше или равно 0
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Программа делает запрос к сервису мониторинга ТИ')
    parser.add_argument('-a', metavar='addr', type=str, help='Имя файла или IP адрес сервера для запроса')
    parser.add_argument('-p', metavar='port', type=int, help='Порт сервера для запроса. Если через файл, то = 1')
    parser.add_argument('-s', metavar='site', type=str, help='Сайт')
    parser.add_argument('-m', metavar='method', type=str, help='Вид сведений. Возможные значения: '
                                                               'requestSmev - запросы в СМЭВ; '
                                                               'requestPGU  - заявления от ПГУ/МФЦ; '
                                                               'responsePGU - ответы на заявления ПГУ/МФЦ; '
                                                               'responseSmev - ответы на СМЭВ запросы; '
                                                               'loadToASP - получение инф. с ТИ в АСП; '
                                                               'loadToTI - отправка инф. из АСП на ТИ.')

    logging.basicConfig(filename='monitorRequest.log', filemode='a', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')
    logging.info('Программа запущена')
    args = parser.parse_args()
    logging.debug('Программа вызвана с аргументами: %s' % args)
    res = -1
    if not args.p:
        port = 80
    else:
        port = int(args.p)
    # Проверяем входные параметры
    if not (args.m in ('requestSmev', 'requestPGU', 'responsePGU', 'responseSmev', 'loadToASP', 'loadToTI')):
        print('Программа вызвана с неправильным видом сведений, используйте -h для справки')
        logging.info('Программа вызвана с неправильным видом сведений')
        exit(1)
    else:
        # Проверим, как получить результат через веб-сервис или файл
        result = None
        err = 0
        if port == 1:
            # Получаем через файл
            try:
                result = open(name=args.a, mode='r', encoding='utf-8').read()
                # Если файл старше 60 мин, то это ошибка
                if (time.time() - os.path.getmtime(args.a))/60 < 60:
                    logging.error('Файл %s старше 60 мин, не сработала передача по FTP' % args.a)
                    err = 1
            except:
                err = 1
                logging.critical('Не смог прочитать файл %s' % args.a)
        else:
            # Получаем через веб-сервис
            result, err = sendRequest.sendRequest(addr=args.a, port=port, site=args.s)
        logging.info('Получен результат: %s. Ошибки: %s' % (result, err))
        if err or result['errorCode']:
            res = -1
        else:
            res = result['info'][args.m]
    logging.info('Программа работу закончила')
    print(res)
    exit(0)
