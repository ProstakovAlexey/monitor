#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Извлекает из БД нужные сведения """

import platform
import pypyodbc
import os
import configparser


def readConfig(file="config.ini"):
    '''
    :param file: имя файла конфигурации
    :return: словарь настроек к БД, err
    '''
    err = 0
    BD = dict()
    if os.access(file, os.F_OK):
        # выполняется если найден конфигурационный файл
        fp = open(file, encoding='utf-8', mode='r')
        config_str = fp.read()
        fp.close()
        # удалить признак кодировки
        config_str = config_str.replace(u'\ufeff', '')
        # чтение конфигурационного файла
        Config = configparser.ConfigParser()
        Config.read_string(config_str)
        sections = Config.sections()
        # читаем все секции
        for section in sections:
            i = Config[section]
            # это секция про ИС, их может быть несколько
            if section.count('BD'):
                BD['address'] = i.get('address', fallback='')
                BD['name'] = i.get('name', fallback='')
                BD['user'] = i.get('user', fallback='sa')
                BD['port'] = i.get('port', fallback='1433')
                BD['password'] = i.get('password', fallback='111')
        # проверим заполнение сведений об БД
        if len(BD.keys()) == 0:
            print('В конфигурационном файле отсутствует обязательная секция о базн данных.')
            err += 1
        else:
            for key in BD.keys():
                if BD[key] == '':
                    print("В секции сведение о БД %s не должен быть пустой, заполните его в конфигурационном файле %s" % (key, file))
                    err += 1
    # нет конфигурационного файла
    else:
        print("Ошибка! Не найден конфигурационный файл")
        err = 1
    return BD, err


def getConnection (DB):
    """ Соединяется с БД, возвращает коннект. Если не получается, то завершает работу.
    :param DB: словарь с параметрами для соединения
    :return: коннект
    """
    # определяет, на какой ОС запущен
    osname = platform.system()
    err = None
    con = None
    con_string = None
    if osname == 'Linux':
        con_string = "DRIVER=FreeTDS; SERVER=%s; PORT=%s; DATABASE=%s; UID=sa; PWD=%s; TDS_Version=8.0; ClientCharset=UTF8; autocommit=True" \
               % (DB['address'], DB['port'], DB['name'], DB['password'])
    elif osname == 'Windows':
        # на windows 2003 тут нужно указать другую версию клиента
        con_string = 'DRIVER={SQL Server Native Client 11.0}; SERVER=%s; DATABASE=%s; UID=sa; PWD=%s' \
               % (DB['address'], DB['name'], DB['password'])
    else:
        err = 'Запущен на не известной ОС. Работает только с Linux и Windows.'
    if not err:
        try:
            # пробую соединится
            con = pypyodbc.connect(con_string)
        except:
            err = "Возникла ошибка при соединении с БД ТИ, строка соединения %s" % con_string
    return con, err


def getInfo(con):
    """
    Извлекает из БД протокол за последний час
    :param con: соединение с БД
    :return: структура данных
    """
    err = 0
    result = dict()
    # определение настроечных констант
    req = r'Регламент:'
    res = r'Запрос к методу'
    zaiv = r'к методу SetRequest'
    status = r'Статус по заявке'
    # Соединение к БД
    cur = con.cursor()
    try:
        cur.execute('select COMMENT from PROTOCOL WHERE datediff(HOUR, CHANGE_DATE, GETDATE())<=1')
    except:
        err = 1
    else:
        # Создание структуры для ответа
        result = {
            'requestSmev': 0,
            'requestPGU': 0,
            'responsePGU': 0,
            'responseSmev': 0
            }
        # В курсоре список строк протокола за последний час, переберем его
        for line in cur.fetchall():
            if line[0].find(req) > -1:
                result['requestSmev'] += 1
            elif line[0].find(res) > -1:
                result['responseSmev'] += 1
            if line[0].find(zaiv) > -1:
                result['requestPGU'] += 1
            elif line[0].find(status) > -1:
                result['responsePGU'] += 1
    return result, err


def getResult():
    """
    Использует все выше описанные функции для получения результата из БД
    :return: result, err
    """
    err_сode = 0
    result = dict()
    db, err = readConfig()
    if err:
        # Не удалось прочитать файл
        err_сode = 10
    else:
        con, err = getConnection(db)
        if err:
            # Не смог соединится с БД
            err_сode = 12
        else:
            result, err = getInfo(con)
            if err:
                # Не смог получить информацию из БД
                err_сode = 14
    return result, err_сode

