# Модуль для отправки сообщений в WhatsApp

## Обзор

Модуль предназначен для автоматической отправки сообщений в WhatsApp с использованием библиотек `pywhatkit`, `pyautogui` и `pynput`. Он позволяет отправлять заданное количество сообщений на указанный номер телефона в случайное время в заданном интервале.

## Подробней

Этот модуль предоставляет функцию для отправки сообщений в WhatsApp, а также пример использования этой функции для отправки нескольких сообщений на указанный номер телефона в случайное время в заданном интервале.
Модуль использует библиотеки `pywhatkit` для отправки сообщений через WhatsApp Web, `pyautogui` для автоматического нажатия клавиши Enter и `pynput` для управления клавиатурой.
Также модуль содержит базу сообщений с эмодзи, из которой случайным образом выбираются сообщения для отправки.

## Функции

### `send_whatsapp_message`

```python
def send_whatsapp_message(phone_number, message, hour, minutes):
    """Sends a WhatsApp message using pywhatkit and pyautogui."""
```

**Назначение**: Отправляет сообщение WhatsApp с использованием библиотек `pywhatkit` и `pyautogui`.

**Параметры**:
- `phone_number` (str): Номер телефона получателя с кодом страны.
- `message` (str): Текст сообщения для отправки.
- `hour` (int): Час отправки сообщения (0-23).
- `minutes` (int): Минута отправки сообщения (0-59).

**Возвращает**:
- `None`

**Вызывает исключения**:
- `Exception`: В случае возникновения ошибки при отправке сообщения.

**Как работает функция**:
1. Использует `pywhatkit.sendwhatmsg` для отправки сообщения через WhatsApp Web.
2. Ждет 20 секунд для загрузки WhatsApp Web.
3. Использует `pynput.keyboard.Controller` для эмуляции нажатия клавиши Enter, что необходимо для отправки сообщения.
4. Выводит сообщение об успешной отправке или сообщение об ошибке в случае неудачи.

### Базовый пример отправки сообщения

```python
phone_number = "+79991234567"
message = "Hello from Python!"
hour = 15
minutes = 30

send_whatsapp_message(phone_number, message, hour, minutes)
```
Отправляет сообщение "Hello from Python!" на номер +79991234567 в 15:30.

### Пример автоматической отправки нескольких сообщений

```python
# Get user inputs
phone_number = input("Enter the phone number with country code: ")
num_messages = int(input("Enter the number of messages to send: "))
start_hour = int(input("Enter the start hour (0-23): "))
end_hour = int(input("Enter the end hour (0-23): "))

message_count = 0
while message_count < num_messages:
    random_hour = random.randint(start_hour, end_hour)
    random_minutes = random.randint(0, 59)
    random_message = random.choice(messages)

    send_whatsapp_message(phone_number, random_message, random_hour, random_minutes)
    message_count += 1
```

**Как работает пример**:
1. Запрашивает у пользователя номер телефона, количество сообщений для отправки, начальный и конечный час для отправки сообщений.
2. В цикле, пока количество отправленных сообщений меньше заданного:
   - Генерирует случайный час и минуту в заданном интервале.
   - Выбирает случайное сообщение из списка `messages`.
   - Вызывает функцию `send_whatsapp_message` для отправки сообщения.
   - Увеличивает счетчик отправленных сообщений.

### Переменные модуля

- `messages` (list): Список сообщений с эмодзи, которые могут быть отправлены.
  ```python
    messages = [
        "Hello! How are you? :slightly_smiling_face:",
        "Thinking of you! :heart:",
        "Just wanted to say hi! :waving_hand:",
        "I love you :heart_exclamation:",
        emoji.emojize("Have a wonderful day! :sun:")
    ]
  ```
```python
phone_number = input("Enter the phone number with country code: ")
num_messages = int(input("Enter the number of messages to send: "))
start_hour = int(input("Enter the start hour (0-23): "))
end_hour = int(input("Enter the end hour (0-23): "))

message_count = 0
while message_count < num_messages:
    random_hour = random.randint(start_hour, end_hour)
    random_minutes = random.randint(0, 59)
    random_message = random.choice(messages)

    send_whatsapp_message(phone_number, random_message, random_hour, random_minutes)
    message_count += 1
```
## Пример использования

Запуск модуля запросит у пользователя номер телефона, количество сообщений для отправки, начальный и конечный час отправки. Затем модуль начнет отправлять случайные сообщения из списка в случайное время в заданном интервале.
```