### **Анализ кода модуля `smtp.py`**

## \\file /src/utils/smtp.py

Модуль предоставляет функциональность для отправки и получения электронных писем с использованием протоколов SMTP и IMAP. Включает функции для отправки писем через SMTP и получения писем через IMAP.

**Качество кода**:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование `logger` для логирования ошибок.
  - Обработка исключений при отправке и получении писем.
  - Использование `MIMEText` для создания email сообщений.
  - Использование переменных окружения для хранения учетных данных.
- **Минусы**:
  - Не все переменные аннотированы типами.
  - Docstring в Google Style не соответствует принятому стандарту оформления в проекте.
  - Отсутствует описание модуля в принятом формате.

**Рекомендации по улучшению**:

1.  **Документация модуля**:
    - Добавить описание модуля в соответствии со стандартом оформления документации в проекте.

2.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это необходимо.

3.  **Docstring**:
    - Перефразировать и привести Docstring в соответствие с требованиями, принятыми в проекте.
    - Перевести docstring на русский язык.
    - Описать все входные параметры и возвращаемые значения.
    - Добавить примеры использования для каждой функции.
    - Добавить информацию о возможных исключениях, которые могут быть вызваны.

4.  **Безопасность**:
    - Убедиться, что все учетные данные (пароли, имена пользователей) хранятся в переменных окружения и не закодированы в коде.

5.  **Форматирование**:
    - Использовать одинарные кавычки для строк.

**Оптимизированный код**:

```python
## \file /src/utils/smtp.py
# -*- coding: utf-8 -*-

"""
Модуль для работы с отправкой и получением email сообщений
=========================================================

Модуль содержит функции для отправки и получения электронных писем с использованием протоколов SMTP и IMAP.
Функции позволяют отправлять письма через SMTP и получать письма через IMAP.

Пример использования
----------------------

>>> from src.utils.smtp import send, receive
>>> # Отправка письма
>>> result = send(subject='Тема письма', body='Текст письма', to='recipient@example.com')
>>> if result:
>>>     print('Письмо успешно отправлено')
>>> else:
>>>     print('Ошибка при отправке письма')
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
    """
    Отправляет email сообщение.

    Args:
        subject (str): Тема письма. По умолчанию ''.
        body (str): Тело письма. По умолчанию ''.
        to (str): Адрес получателя. По умолчанию 'one.last.bit@gmail.com'.

    Returns:
        bool: True, если письмо успешно отправлено, иначе False.

    Raises:
        smtplib.SMTPException: Если произошла ошибка при отправке письма.

    Example:
        >>> send(subject='Тестовое письмо', body='Это тестовое письмо.', to='test@example.com')
        True
    """
    try:
        # Create SMTP connection
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
        logger.error(f'Ошибка при отправке email. Тема: {subject}. Текст: {body}. Ошибка: {ex}', exc_info=True)  # Логируем ошибку
        return False


def receive(imap_server: str, user: str, password: str, folder: str = 'inbox') -> Optional[List[Dict[str, str]]]:
    """
    Получает email сообщения из указанной папки на IMAP сервере.

    Args:
        imap_server (str): Адрес IMAP сервера.
        user (str): Имя пользователя для входа на сервер.
        password (str): Пароль для входа на сервер.
        folder (str): Название папки для получения писем. По умолчанию 'inbox'.

    Returns:
        Optional[List[Dict[str, str]]]: Список словарей, где каждый словарь содержит информацию об одном email сообщении
        (тема, отправитель, тело). Возвращает None в случае ошибки.

    Raises:
        imaplib.IMAP4.error: Если произошла ошибка при подключении или аутентификации на IMAP сервере.
        Exception: Если произошла ошибка при обработке email сообщений.

    Example:
        >>> emails = receive(imap_server='imap.example.com', user='user@example.com', password='password', folder='INBOX')
        >>> if emails:
        >>>     for email in emails:
        >>>         print(f"Тема: {email['subject']}")
        >>>         print(f"Отправитель: {email['from']}")
        >>>         print(f"Тело: {email['body']}")
        >>> else:
        >>>     print("Не удалось получить email сообщения.")
    """
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(user, password)
        mail.select(folder)

        status, data = mail.search(None, 'ALL')
        email_ids = data[0].split()

        emails: List[Dict[str, str]] = []
        for email_id in email_ids:
            status, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            email_data: Dict[str, str] = {
                'subject': msg['subject'],
                'from': msg['from'],
                'body': msg.get_payload(decode=True, _charset="utf-8").decode("utf-8", "ignore")  # Decode & handle potential errors
            }
            emails.append(email_data)

        mail.close()
        mail.logout()
        return emails

    except Exception as ex:
        logger.error(f'Произошла ошибка при получении email сообщений: {ex}', exc_info=True)  # Логируем ошибку
        return None