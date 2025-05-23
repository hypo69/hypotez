# WhatsApp бот для отправки сообщений

## Обзор

Данный модуль содержит код для автоматизированной отправки сообщений в WhatsApp. 

**Описание работы бота:**

- Бот работает с использованием веб-версии WhatsApp и отправляет сообщения по расписанию, используя библиотеку `pywhatkit`.
- Пользователь может задать количество сообщений, которые нужно отправить, и временной диапазон для отправки.
- Бот генерирует случайные сообщения из заданного списка и отправляет их по заданному номеру телефона.
- Бот использует библиотеки `pyautogui`, `pynput` и `emoji` для имитации ввода с клавиатуры и добавления эмодзи в сообщения.

**Основные возможности:**

- Автоматизированная отправка сообщений в WhatsApp.
- Настройка количества отправляемых сообщений.
- Настройка временного диапазона для отправки.
- Генерация случайных сообщений из списка.
- Добавление эмодзи в сообщения.

## Как использовать бота

**1. Установка необходимых пакетов:**

```bash
pip install pywhatkit pyautogui pynput emoji
```

**2. Запуск скрипта:**

```bash
python имя_файла.py
```

**3. Ввод данных:**

- Введите номер телефона получателя (с кодом страны).
- Введите количество сообщений, которые нужно отправить.
- Введите начальный и конечный час временного диапазона для отправки.

## Классы

### `WhatsappBot`

**Описание**: Класс для автоматической отправки сообщений в WhatsApp.

**Атрибуты**:

- `phone_number` (str): Номер телефона получателя (с кодом страны).
- `num_messages` (int): Количество сообщений, которые нужно отправить.
- `start_hour` (int): Начальный час временного диапазона для отправки.
- `end_hour` (int): Конечный час временного диапазона для отправки.
- `messages` (list): Список сообщений, которые будут отправляться.

**Методы**:

- `send_whatsapp_message(phone_number: str, message: str, hour: int, minutes: int) -> None`: Отправляет сообщение в WhatsApp.
- `run() -> None`: Запускает бота и отправляет сообщения по расписанию.

## Методы класса

### `send_whatsapp_message`

```python
def send_whatsapp_message(
    phone_number: str,
    message: str,
    hour: int,
    minutes: int,
) -> None:
    """
    Отправляет сообщение в WhatsApp.

    Args:
        phone_number (str): Номер телефона получателя (с кодом страны).
        message (str): Текст сообщения.
        hour (int): Час отправки сообщения (0-23).
        minutes (int): Минуты отправки сообщения (0-59).

    Raises:
        Exception: Если возникает ошибка при отправке сообщения.

    Example:
        >>> send_whatsapp_message('+79991234567', 'Hello, world!', 12, 30)
    """
    ...
```

**Назначение**: Функция отправляет сообщение в WhatsApp по заданному номеру телефона, в заданное время.

**Параметры**:

- `phone_number` (str): Номер телефона получателя (с кодом страны).
- `message` (str): Текст сообщения.
- `hour` (int): Час отправки сообщения (0-23).
- `minutes` (int): Минуты отправки сообщения (0-59).

**Возвращает**:

- `None`:  Функция не возвращает значений.

**Вызывает исключения**:

- `Exception`: Если возникает ошибка при отправке сообщения.

**Пример**:

```python
send_whatsapp_message('+79991234567', 'Hello, world!', 12, 30)
```

### `run`

```python
def run() -> None:
    """
    Запускает бота и отправляет сообщения по расписанию.

    Raises:
        Exception: Если возникает ошибка при выполнении бота.

    Example:
        >>> bot.run()
    """
    ...
```

**Назначение**: Функция запускает бота и отправляет сообщения по расписанию.

**Параметры**:

- `None`:  Функция не принимает параметров.

**Возвращает**:

- `None`:  Функция не возвращает значений.

**Вызывает исключения**:

- `Exception`: Если возникает ошибка при выполнении бота.

**Пример**:

```python
bot.run()
```

## Параметры класса

- `phone_number` (str): Номер телефона получателя (с кодом страны).
- `num_messages` (int): Количество сообщений, которые нужно отправить.
- `start_hour` (int): Начальный час временного диапазона для отправки.
- `end_hour` (int): Конечный час временного диапазона для отправки.
- `messages` (list): Список сообщений, которые будут отправляться.

## Примеры

```python
# Создание инстанса бота
bot = WhatsappBot(
    phone_number='+79991234567',
    num_messages=5,
    start_hour=10,
    end_hour=18,
    messages=[
        'Hello, world!',
        'How are you?',
        'What\'s up?',
        'Good day!',
        'See you later!',
    ],
)

# Запуск бота
bot.run()