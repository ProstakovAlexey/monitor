#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Содержит несколько тестов, для проверки работоспособности программы после ее установки и настройки,
до подключения к IIS"""

import unittest
import getInfo
import sendRequest


class case1(unittest.TestCase):
    """Класс предназначен для предварительного тестирования. Его нужно выполнить после настройки конфигурационного
    файла и запуска демоверсии сервиса по порту 8080"""
    def test1_BD_connect(self):
        """Проверяет возможность поключения к БД ТИ. Фактически проверяется правильность заполнения конфигурационного
        файла и наличие сетевой связанность с БД"""
        db, err = getInfo.readConfig()
        self.assertFalse(err, 'Ошибка при проверки конфигурационного файла: %s' % err)
        con, err = getInfo.getConnection(db)
        self.assertFalse(err, 'Ошибка при соединении с БД: %s' % err)
        cur = con.cursor()
        cur.execute('select top 10 min(id) from PROTOCOL')
        self.assertTrue(cur.fetchone()[0], 'Не удалось извлечь данные протокола')
        con.close()

    def test2_testRequestOk(self):
        """Делает специальный тестовый запрос, его результат всегда 20"""
        result, err = sendRequest.sendRequest(addr='127.0.0.1', site='monitor', method='test')
        self.assertFalse(err, err)
        self.assertEqual(20, result['info']['test'], 'Этот специальный тестовый метод должен был вернуть 20. '
                                                     'Пришел ответ %s' % result)

    def test3_testRequestERR(self):
        """Делает запрос на специальный метод, должен получить код ошибки 42"""
        result, err = sendRequest.sendRequest(addr='127.0.0.1', site='monitor', method='error')
        self.assertFalse(err, err)
        self.assertEqual(42, result['errorCode'], 'Этот запрос с неверными параметрами, должен вернуть код 42. '
                                                  'Пришел ответ %s' % result)

    def test4_testRequestERR(self):
        """Делает запрос на несуществующий метод, должен вернуть код 2"""
        result, err = sendRequest.sendRequest(addr='127.0.0.1', site='monitor', method='err')
        self.assertFalse(err, err)
        self.assertEqual(2, result['errorCode'], 'Этот запрос на несуществующий метод, должен вернуть код 2. '
                                                 'Пришел ответ %s' % result)



