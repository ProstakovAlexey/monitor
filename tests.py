#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Содержит несколько тестов, для проверки работоспособности программы после ее установки и настройки,
до подключения к IIS"""

import unittest
import getInfo
import sendRequest
import time


class case1(unittest.TestCase):
    """Класс предназначен для предварительного тестирования. Его нужно выполнить после настройки конфигурационного
    файла и запуска демоверсии сервиса по порту 8080"""
    def test1_BD_connect(self):
        """Проверяет возможность поключения к БД ТИ. Фактически проверяется правильность заполнения конфигурационного
        файла и наличие сетевой связанность с БД"""
        db, err, ftp = getInfo.readConfig()
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

    def test5_data(self):
        """Делает один запрос на реальные данные, должен вернуть errorCode=0"""
        result, err = sendRequest.sendRequest(addr='127.0.0.1', site='monitor')
        self.assertFalse(err, err)
        self.assertEqual(0, result['errorCode'], 'Должен вернуть код ошибки = 0.'
                                                 'Пришел ответ %s' % result)

    def test6_cache(self):
        """Проверяет работу кэша на IIS. Делает один запрос на реальные данные. Ждет секунду и делает втрой запрос.
        Сравнивает время в 1-м и 2-м случае. Если кэш работает, они должны совпадать."""
        # Первый запрос
        result, err = sendRequest.sendRequest(addr='127.0.0.1', site='monitor')
        self.assertFalse(err, err)
        date1 = result['date']
        # Ждем
        time.sleep(1)
        # Второй запрос
        result, err = sendRequest.sendRequest(addr='127.0.0.1', site='monitor')
        self.assertFalse(err, err)
        # Сравнение
        self.assertEqual(date1, result['date'], 'Если кэш работает, время ответа должно быть одинаковым. В первом '
                                                'запросе пришел ответ %s, во втором %s' % (date1, result['date']))
        print(result)

