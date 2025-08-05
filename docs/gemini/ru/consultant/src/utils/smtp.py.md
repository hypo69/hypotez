### **Анализ кода модуля `src.utils.smtp`**

2. **Качество кода**:
   - **Соответствие стандартам**: 7/10
   - **Плюсы**:
     - Код хорошо структурирован и включает функции для отправки и получения электронной почты.
     - Используется логирование ошибок с помощью модуля `logger` из `src.logger.logger`.
     - Присутствует обработка исключений для предотвращения сбоев.
     - Конфиденциальные данные (логин и пароль) получаются из переменных окружения, что повышает безопасность.
   - **Минусы**:
     - Отсутствует docstring модуля в соответствии с правилами форматирования проекта.
     - В коде используются двойные кавычки.

3. **Рекомендации по улучшению**:
   - Добавить docstring модуля в соответствии с форматом, принятым в проекте.
   - В docstring для модуля и функций добавить примеры использования.
   - Использовать одинарные кавычки вместо двойных.
   - Добавить аннотации типов для переменных `email_ids` и `emails` в функции `receive`.

4. **Оптимизированный код**:

```python
## \file /src/utils/smtp.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с SMTP и IMAP
====================================

Модуль предоставляет функциональность для отправки и получения электронной почты с использованием SMTP и IMAP серверов.
Он включает функции для отправки электронных писем через SMTP и получения электронных писем через IMAP.

Пример использования:
----------------------

>>> from src.utils.smtp import send, receive
>>> send(subject='Test Email', body='This is a test email', to='recipient@example.com')
True

>>> receive(imap_server='imap.example.com', user='username', password='password', folder='INBOX')
[{'subject': 'Test Email', 'from': 'sender@example.com', 'body': 'This is a test email'}]

.. module:: src.utils.smtp
"""

import smtplib
import imaplib
import email
import os
from email.mime.text import MIMEText
from typing import List, Dict, Optional

from src.logger.logger import logger

# --- Configuration ---
# DO NOT HARDCODE CREDENTIALS HERE!  Use environment variables instead.
_connection: Dict[str, Optional[str | int]] = {
    'server': os.environ.get('SMTP_SERVER', 'smtp.example.com'),
    'port': int(os.environ.get('SMTP_PORT', 587)),
    'user': os.environ.get('SMTP_USER'),
    'password': os.environ.get('SMTP_PASSWORD'),
    'receiver': os.environ.get('SMTP_RECEIVER', 'one.last.bit@gmail.com')
}


def send(subject: str = '', body: str = '', to: str = 'one.last.bit@gmail.com') -> bool:
    """Отправляет электронное письмо. Возвращает True в случае успеха, False в противном случае. Логирует ошибки.

    Args:
        subject (str): Тема письма.
        body (str): Тело письма.
        to (str): Адрес получателя.

    Returns:
        bool: True, если письмо отправлено успешно, иначе False.

    Example:
        >>> send(subject='Test Email', body='This is a test email', to='recipient@example.com')
        True
    """
    try:
        # Создание SMTP соединения
        smtp = smtplib.SMTP(_connection['server'], _connection['port'])
        smtp.ehlo()
        smtp.starttls()
        smtp.login(_connection['user'], _connection['password'])

        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = _connection['user']
        message['To'] = to

        smtp.sendmail(_connection['user'], to, message.as_string())
        smtp.quit()
        return True

    except Exception as ex:
        logger.error(f'Ошибка при отправке email. Тема: {subject}. Текст: {body}. Ошибка: {ex}', exc_info=True)
        return False


def receive(imap_server: str, user: str, password: str, folder: str = 'inbox') -> Optional[List[Dict[str, str]]]:
    """Получает электронные письма. Возвращает список словарей с данными писем в случае успеха, None в противном случае. Логирует ошибки.

    Args:
        imap_server (str): Адрес IMAP сервера.
        user (str): Имя пользователя для входа на сервер.
        password (str): Пароль для входа на сервер.
        folder (str): Папка для чтения писем (по умолчанию 'inbox').

    Returns:
        Optional[List[Dict[str, str]]]: Список словарей, где каждый словарь содержит данные одного письма (тема, отправитель, текст). Возвращает None в случае ошибки.

    Example:
        >>> receive(imap_server='imap.example.com', user='username', password='password', folder='INBOX')
        [{'subject': 'Test Email', 'from': 'sender@example.com', 'body': 'This is a test email'}]
    """
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(user, password)
        mail.select(folder)

        status, data = mail.search(None, 'ALL')
        email_ids: List[bytes] = data[0].split()

        emails: List[Dict[str, str]] = []
        for email_id in email_ids:
            status, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            email_data = {
                'subject': msg['subject'],
                'from': msg['from'],
                'body': msg.get_payload(decode=True, _charset="utf-8").decode('utf-8', 'ignore')  # Decode & handle potential errors
            }
            emails.append(email_data)

        mail.close()
        mail.logout()
        return emails

    except Exception as ex:
        logger.error(f'Ошибка при получении email: {ex}', exc_info=True)
        return None