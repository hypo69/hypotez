# Модуль для отправки сообщений в WhatsApp

## Обзор

Модуль предоставляет функции для отправки сообщений в WhatsApp с использованием библиотек `pywhatkit` и `pyautogui`. Он позволяет автоматически отправлять сообщения на определенный номер телефона в заданное время. 

## Детали

Модуль использует библиотеку `pywhatkit` для отправки сообщений в WhatsApp. Он также использует `pyautogui` для имитации нажатия клавиши Enter, чтобы отправить сообщение после того, как WhatsApp Web загрузится. 

## Функции

### `send_whatsapp_message(phone_number, message, hour, minutes)`

**Назначение**: Функция отправляет сообщение в WhatsApp на указанный номер телефона в заданное время.

**Параметры**:

- `phone_number` (str): Номер телефона получателя с кодом страны.
- `message` (str): Сообщение, которое нужно отправить.
- `hour` (int): Час отправки сообщения (0-23).
- `minutes` (int): Минута отправки сообщения (0-59).

**Возвращаемое значение**:

- `None`

**Исключения**:

- `Exception`: Если возникает ошибка при отправке сообщения.

**Как работает функция**:

1. Функция использует `pywhatkit.sendwhatmsg` для отправки сообщения в WhatsApp. 
2. Она устанавливает время ожидания (`wait_time`) в 25 секунд, чтобы дать WhatsApp Web время загрузиться.
3. После этого функция использует `pyautogui` для имитации нажатия клавиши Enter, чтобы отправить сообщение.
4. Если происходит ошибка, функция выводит сообщение об ошибке.

**Примеры**:

```python
# Отправить сообщение на номер +1234567890 в 10:30 утра
send_whatsapp_message('+1234567890', 'Hello, how are you?', 10, 30)
```

## Переменные

### `messages`

**Описание**: Список сообщений, которые могут быть отправлены. Сообщения содержат смайлики.

**Пример**:

```python
messages = [
    "Hello! How are you? :slightly_smiling_face:",
    "Thinking of you! :heart:",
    "Just wanted to say hi! :waving_hand:",
    "I love you :heart_exclamation:",
    emoji.emojize("Have a wonderful day! :sun:")
]
```

## Пример использования

```python
# Получить номер телефона от пользователя
phone_number = input("Enter the phone number with country code: ")

# Получить количество сообщений от пользователя
num_messages = int(input("Enter the number of messages to send: "))

# Получить начальный и конечный час отправки сообщений
start_hour = int(input("Enter the start hour (0-23): "))
end_hour = int(input("Enter the end hour (0-23): "))

# Счетчик отправленных сообщений
message_count = 0

# Цикл отправки сообщений
while message_count < num_messages:
    # Выбрать случайное время отправки
    random_hour = random.randint(start_hour, end_hour)
    random_minutes = random.randint(0, 59)

    # Выбрать случайное сообщение из списка
    random_message = random.choice(messages)

    # Отправить сообщение
    send_whatsapp_message(phone_number, random_message, random_hour, random_minutes)

    # Увеличить счетчик отправленных сообщений
    message_count += 1
```