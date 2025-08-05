# Модуль отправки сообщений WhatsApp

## Обзор

Этот модуль предоставляет функции для отправки сообщений WhatsApp с использованием библиотек `pywhatkit`, `pyautogui` и `pynput`. Он позволяет отправлять сообщения с задержкой, используя эмодзи и случайные сообщения из списка.

## Подробности

Модуль использует `pywhatkit` для отправки сообщения, `pyautogui` для имитации нажатия клавиши Enter на клавиатуре и `pynput` для управления клавиатурой.

## Функции

### `send_whatsapp_message(phone_number, message, hour, minutes)`

**Назначение**: Отправляет сообщение в WhatsApp с использованием `pywhatkit`.

**Параметры**:
- `phone_number` (str): Номер телефона получателя с кодом страны.
- `message` (str): Сообщение, которое нужно отправить.
- `hour` (int): Час отправки сообщения (0-23).
- `minutes` (int): Минута отправки сообщения (0-59).

**Возвращает**:
- None

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при отправке сообщения.

**Как работает функция**:
- Функция использует `pywhatkit.sendwhatmsg` для отправки сообщения.
- Она задает время отправки с учетом `hour` и `minutes`.
- Использует `time.sleep` для паузы, чтобы дать время WhatsApp Web загрузиться.
- Использует `pyautogui` для имитации нажатия клавиши Enter для отправки сообщения.

**Примеры**:
```python
send_whatsapp_message('+79111111111', 'Hello, how are you?', 10, 30)  # Отправка сообщения в 10:30
```

## Примеры

### Отправка сообщения в WhatsApp с задержкой и эмодзи

```python
import pywhatkit
import pyautogui
from pynput.keyboard import Key, Controller
import emoji
import random
import time

# ... (определение функции send_whatsapp_message) ...

# Создание списка сообщений с эмодзи
messages = [
    "Hello! How are you? :slightly_smiling_face:",
    "Thinking of you! :heart:",
    "Just wanted to say hi! :waving_hand:",
    "I love you :heart_exclamation:",
    emoji.emojize("Have a wonderful day! :sun:")
]

# Получение данных от пользователя
phone_number = input("Enter the phone number with country code: ")
num_messages = int(input("Enter the number of messages to send: "))
start_hour = int(input("Enter the start hour (0-23): "))
end_hour = int(input("Enter the end hour (0-23): "))

# Отправка сообщений в цикле
message_count = 0
while message_count < num_messages:
    random_hour = random.randint(start_hour, end_hour)
    random_minutes = random.randint(0, 59)
    random_message = random.choice(messages)

    send_whatsapp_message(phone_number, random_message, random_hour, random_minutes)
    message_count += 1
```