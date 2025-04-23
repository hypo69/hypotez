### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
Данный код реализует отправку сообщений в WhatsApp с использованием библиотеки `pywhatkit` и автоматизации действий с помощью `pyautogui` и `pynput`. Он позволяет отправлять заданное количество сообщений на указанный номер телефона в случайное время в пределах заданного интервала.

Шаги выполнения
-------------------------
1. **Импорт библиотек**: Импортируются необходимые библиотеки: `pywhatkit` для отправки сообщений, `pyautogui` для эмуляции нажатий клавиш, `pynput.keyboard` для управления клавиатурой, `emoji` для работы с эмодзи, `random` для генерации случайного времени и выбора сообщений, и `time` для временных задержек.
2. **Определение функции `send_whatsapp_message`**: Эта функция отправляет сообщение WhatsApp.
    - Она принимает номер телефона, сообщение, час и минуты в качестве аргументов.
    - Использует `pywhatkit.sendwhatmsg` для отправки сообщения через WhatsApp Web. Указывается время ожидания загрузки страницы и необходимость закрытия вкладки.
    - После отправки сообщения, код ждет 20 секунд, чтобы страница WhatsApp Web успела загрузиться.
    - Эмулирует нажатие клавиши Enter с помощью `pynput.keyboard` для отправки сообщения.
    - Выводит сообщение об успешной отправке или ошибке.
3. **Создание списка сообщений**: Определяется список `messages`, содержащий различные сообщения с эмодзи.
4. **Получение пользовательского ввода**: Запрашивается у пользователя номер телефона, количество сообщений для отправки, начальный и конечный час для отправки сообщений.
5. **Отправка сообщений в цикле**:
    - Инициализируется счетчик отправленных сообщений `message_count`.
    - В цикле, пока `message_count` меньше заданного количества сообщений:
        - Генерируется случайный час и минуты в заданном диапазоне.
        - Выбирается случайное сообщение из списка `messages`.
        - Функция `send_whatsapp_message` вызывается для отправки сообщения.
        - Счетчик отправленных сообщений увеличивается.

Пример использования
-------------------------

```python
import pywhatkit
import pyautogui
from pynput.keyboard import Key, Controller
import emoji
import random
import time

def send_whatsapp_message(phone_number, message, hour, minutes):
    """Отправляет сообщение WhatsApp с использованием pywhatkit и pyautogui."""
    try:
        pywhatkit.sendwhatmsg(phone_number, message, hour, minutes, wait_time=25, tab_close=True)
        time.sleep(20)  # Дает время для загрузки WhatsApp Web
        keyboard = Controller()
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        print("Сообщение отправлено успешно!")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")


# Банк сообщений с эмодзи
messages = [
    "Привет! Как дела? :slightly_smiling_face:",
    "Думаю о тебе! :heart:",
    "Просто хотел поздороваться! :waving_hand:",
    "Я люблю тебя :heart_exclamation:",
    emoji.emojize("Хорошего дня! :sun:")
]

# Получение пользовательского ввода
phone_number = input("Введите номер телефона с кодом страны: ")
num_messages = int(input("Введите количество сообщений для отправки: "))
start_hour = int(input("Введите начальный час (0-23): "))
end_hour = int(input("Введите конечный час (0-23): "))

message_count = 0
while message_count < num_messages:
    random_hour = random.randint(start_hour, end_hour)
    random_minutes = random.randint(0, 59)
    random_message = random.choice(messages)

    send_whatsapp_message(phone_number, random_message, random_hour, random_minutes)
    message_count += 1