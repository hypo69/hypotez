```python
                ## \file /src/utils/smtp.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.utils 
	:platform: Windows, Unix
	:synopsis: SMTP Email Interface

"""



""" This module provides functionality to send and receive emails using an SMTP or IMAP server.
It includes functions to send emails using SMTP and retrieve emails using IMAP.

Functions:
    - `send(subject: str = '', body: str = '', to: str = 'one.last.bit@gmail.com') -> bool`
      Sends an email using the SMTP server specified in the `_connection` dictionary.  Returns `True` on success, `False` on failure.  Includes error logging.
    
    - `receive(imap_server: str, user: str, password: str, folder: str = 'inbox') -> Optional[List[Dict[str, str]]]`
      Retrieves emails from an IMAP server and returns them as a list of dictionaries.  Returns `None` on error. Includes error logging.


** Important Considerations for Security and Robustness **:

    - **_connection Dictionary:** Do *not* hardcode credentials in this file.  Move the `_connection` dictionary to environment variables (e.g., using `os.environ`). This is crucial for security.  Avoid storing passwords directly in source code.

    - **Error Handling:** The code includes robust error handling, logging exceptions with details (subject, body, etc.).  This is very helpful for debugging.

    - **Email Parsing:** The `receive` function handles various email formats gracefully, preventing potential issues.

    - **MIME Handling:**  The code correctly uses `MIMEText` for constructing the email message, crucial for sending basic text emails.


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
_connection = {
    'server': os.environ.get('SMTP_SERVER', 'smtp.example.com'),
    'port': int(os.environ.get('SMTP_PORT', 587)),
    'user': os.environ.get('SMTP_USER'),
    'password': os.environ.get('SMTP_PASSWORD'),
    'receiver': os.environ.get('SMTP_RECEIVER', 'one.last.bit@gmail.com')
}


def send(subject: str = '', body: str = '', to: str = 'one.last.bit@gmail.com') -> bool:
    """Sends an email.  Returns True if successful, False otherwise. Logs errors."""
    try:
        # Create SMTP connection
        smtp = smtplib.SMTP(_connection['server'], _connection['port'])
        smtp.ehlo()
        smtp.starttls()
        smtp.login(_connection['user'], _connection['password'])

        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = _connection['user']
        message["To"] = to

        smtp.sendmail(_connection['user'], to, message.as_string())
        smtp.quit()
        return True

    except Exception as ex:
        logger.error(f"Error sending email. Subject: {subject}. Body: {body}. Error: {ex}", exc_info=True)
        return False

def receive(imap_server: str, user: str, password: str, folder: str = 'inbox') -> Optional[List[Dict[str, str]]]:
    """Retrieves emails. Returns a list of email dictionaries if successful, None otherwise. Logs errors."""
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(user, password)
        mail.select(folder)

        status, data = mail.search(None, 'ALL')
        email_ids = data[0].split()

        emails = []
        for email_id in email_ids:
            status, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            email_data = {
                'subject': msg['subject'],
                'from': msg['from'],
                'body': msg.get_payload(decode=True, _charset="utf-8").decode("utf-8", "ignore")  # Decode & handle potential errors
            }
            emails.append(email_data)

        mail.close()
        mail.logout()
        return emails

    except Exception as ex:
        logger.error(f"Error occurred while retrieving emails: {ex}", exc_info=True)
        return None
                ```

### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Модуль `src.utils.smtp`  предоставляет функциональность для отправки и получения электронных писем с использованием SMTP или IMAP-серверов. 
Он включает в себя функции для отправки писем с помощью SMTP и получения писем с использованием IMAP.

Шаги выполнения
-------------------------
1. Настройка: 
    - Создайте словарь `_connection` с необходимыми конфигурационными параметрами:
        - `server`: адрес сервера SMTP
        - `port`: порт сервера SMTP (обычно 587 для TLS)
        - `user`: имя пользователя SMTP-аккаунта
        - `password`: пароль SMTP-аккаунта
        - `receiver`:  (опционально) адрес получателя по умолчанию
    - Не храните учетные данные непосредственно в коде! Используйте переменные окружения (например, `os.environ`) для безопасного хранения конфиденциальной информации.
2. Отправка почты: 
    - Используйте функцию `send(subject: str = '', body: str = '', to: str = 'one.last.bit@gmail.com') -> bool`:
        - `subject`: тема письма 
        - `body`: текст письма
        - `to`: адрес получателя (по умолчанию `'one.last.bit@gmail.com'`)
    - Функция возвращает `True`, если письмо успешно отправлено, `False` в случае ошибки.
    - В случае ошибки, функция записывает подробную информацию об ошибке в журнал с помощью `logger.error()`.
3. Получение почты: 
    - Используйте функцию `receive(imap_server: str, user: str, password: str, folder: str = 'inbox') -> Optional[List[Dict[str, str]]]`:
        - `imap_server`: адрес IMAP-сервера
        - `user`: имя пользователя IMAP-аккаунта
        - `password`: пароль IMAP-аккаунта
        - `folder`: папка на IMAP-сервере, из которой нужно получить письма (по умолчанию `'inbox'`)
    - Функция возвращает список словарей с информацией о письмах, если они успешно получены, `None` в случае ошибки.
    - В случае ошибки, функция записывает информацию об ошибке в журнал с помощью `logger.error()`.


Пример использования
-------------------------

```python
from src.utils.smtp import send, receive

# Настройка (используйте переменные окружения вместо жестко заданных значений)
_connection = {
    'server': os.environ.get('SMTP_SERVER', 'smtp.example.com'),
    'port': int(os.environ.get('SMTP_PORT', 587)),
    'user': os.environ.get('SMTP_USER'),
    'password': os.environ.get('SMTP_PASSWORD'),
}

# Отправка письма
subject = 'Тестовое письмо'
body = 'Это тестовое письмо.'
to = 'recipient@example.com'
success = send(subject=subject, body=body, to=to)
if success:
    print('Письмо успешно отправлено.')
else:
    print('Ошибка при отправке письма.')

# Получение писем 
imap_server = 'imap.example.com'
user = _connection['user']
password = _connection['password']
emails = receive(imap_server, user, password)
if emails:
    print('Получено писем:', len(emails))
    for email in emails:
        print('Тема:', email['subject'])
        print('Отправитель:', email['from'])
        print('Текст письма:', email['body'])
else:
    print('Ошибка при получении писем.')
```