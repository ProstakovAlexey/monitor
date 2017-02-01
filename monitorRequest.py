#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sendRequest
import argparse
import logging


""" Отправляет запрос на получение данных из протокола. Метода получает как входной параметр, результат запроса
выдает к ком. строку. -1 - ошибка, иначе число больше или равно 0
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Программа делает запрос к сервису мониторинга ТИ')
    parser.add_argument('-a', metavar='addr', type=str, help='Имя или IP адрес сервера для запроса')
    parser.add_argument('-p', metavar='port', type=int, help='Порт сервера для запроса')
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
        result, err = sendRequest.sendRequest(addr=args.a, port=port, site=args.s)
        logging.info('Получен результат от сервиса: %s. Ошибки: %s' % (result, err))
        if err or result['errorCode']:
            res = -1
        else:
            res = result['info'][args.m]
    logging.info('Программа работу закончила')
    print(res)
    exit(0)
