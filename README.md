﻿Monitor. Система мониторинга ТИ 
===============================
Программа Monitor предназначена для мониторинга точки интеграции(ТИ) совместно с системой Zabbix. Может сообщать следующие параметры ТИ:

    - кол-во СМЭВ запросов, направленных ТИ;
    - кол-во предоставленных ТИ ответов на СМЭВ запросы, пришедших из сторонних ИС;
    - кол-во заявлений ПГУ/МФЦ полученных ТИ;
    - кол-во ответов на заявления ПГУ/МФЦ;
	- кол-во обращений для получение инф. с ТИ в АСП;
	- кол-во обращений для отправка инф. из АСП на ТИ.

Программа написана на языке python3 и использует для работы веб-сервер IIS. Я постарался писать код максимально просто и понятно, снабжая его комментариями. 
Надеюсь, что будут желающие в нем разбираться, вносить изменения. Так же программа снабжена документацией, написанной на sphinx, ее откоплированный вариант лежит в папке doc\build\html\.
Перед использование рекомендую ознакомится с документацией, она совсем не большая.

Замечания и пожелания по работе, а так же исправления можете высылать мне на электронную почту.

С уважением, Простаков Алексей.
alexey@tulalinux.ru

 

