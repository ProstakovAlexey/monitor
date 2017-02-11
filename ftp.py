# -*- coding: utf-8 -*-
import datetime
import getInfo
import cgi
import json
import ftplib


if __name__ == "__main__":
    # Сразу заполним дату
    res = dict(date=datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y %H:%M:%S'))
    # Заполним блок с информацией и код ошибки
    res['info'], res['errorCode'] = getInfo.getResult()
    # Заполняем фразу сообщение об ошибке
    res = json.dumps(cgi.get_err_message(res), sort_keys=True, indent=4, separators=(',', ': '))
    # Прочитать конфиг для соединения с ФТП
    db, ftp, err = getInfo.readConfig()
    # Проверить отсутствие ошибок при чтение конфига
    if err:
        # Не удалось прочитать файл
        print('Не удалось прочесть конфигурационный файл')
        exit(1)
    # Устанавливаем соединение с сервером
    con = ftplib.FTP(ftp['address'], ftp['user'], ftp['password'])
    # Переходим в папку
    con.cwd('homes')
    # Передаем файл на сервер
    send = con.storbinary("STOR " + 'monitor.json', res)
    # Закрываем FTP соединение
    con.close()
    exit(0)

