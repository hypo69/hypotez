### **Системные инструкции для обработки кода проекта `hypotez`**

=========================================================================================

Описание функциональности и правил для генерации, анализа и улучшения кода. Направлено на обеспечение последовательного и читаемого стиля кодирования, соответствующего требованиям.

---

### **Основные принципы**

#### **1. Общие указания**:
- Соблюдай четкий и понятный стиль кодирования.
- Все изменения должны быть обоснованы и соответствовать установленным требованиям.

#### **2. Комментарии**:
- Используй `#` для внутренних комментариев.
- Документация всех функций, методов и классов должна следовать такому формату: 
    ```python
        def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
            """ 
            Args:
                param (str): Описание параметра `param`.
                param1 (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.
    
            Returns:
                dict | None: Описание возвращаемого значения. Возвращает словарь или `None`.
    
            Raises:
                SomeError: Описание ситуации, в которой возникает исключение `SomeError`.

            Ехаmple:
                >>> function('param', 'param1')
                {'param': 'param1'}
            """
    ```
- Комментарии и документация должны быть четкими, лаконичными и точными.

#### **3. Форматирование кода**:
- Используй одинарные кавычки. `a:str = 'value'`, `print('Hello World!')`;
- Добавляй пробелы вокруг операторов. Например, `x = 5`;
- Все параметры должны быть аннотированы типами. `def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:`;
- Не используй `Union`. Вместо этого используй `|`.

#### **4. Логирование**:
- Для логгирования Всегда Используй модуль `logger` из `src.logger.logger`.
- Ошибки должны логироваться с использованием `logger.error`.
Пример:
    ```python
        try:
            ...
        except Exception as ex:
            logger.error('Error while processing data', ех, exc_info=True)
    ```
#### **5 Не используй `Union[]` в коде. Вместо него используй `|`
Например:
```python
x: str | int ...
```




---

### **Основные требования**:

#### **1. Формат ответов в Markdown**:
- Все ответы должны быть выполнены в формате **Markdown**.

#### **2. Формат комментариев**:
- Используй указанный стиль для комментариев и документации в коде.
- Пример:

```python
from typing import Generator, Optional, List
from pathlib import Path


def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    chunk_size: int = 8192,
) -> Generator[str, None, None] | str | None:
    """
    Считывает содержимое файла (или файлов из каталога) с использованием генератора для экономии памяти.

    Args:
        file_path (str | Path): Путь к файлу или каталогу.
        as_list (bool): Если `True`, возвращает генератор строк.
        extensions (Optional[List[str]]): Список расширений файлов для чтения из каталога.
        chunk_size (int): Размер чанков для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или `None` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text...
    """
    ...
```
- Всегда делай подробные объяснения в комментариях. Избегай расплывчатых терминов, 
- таких как *«получить»* или *«делать»*. Вместо этого используйте точные термины, такие как *«извлечь»*, *«проверить»*, *«выполнить»*.
- Вместо: *«получаем»*, *«возвращаем»*, *«преобразовываем»* используй имя объекта *«функция получае»*, *«переменная возвращает»*, *«код преобразовывает»* 
- Комментарии должны непосредственно предшествовать описываемому блоку кода и объяснять его назначение.

#### **3. Пробелы вокруг операторов присваивания**:
- Всегда добавляйте пробелы вокруг оператора `=`, чтобы повысить читаемость.
- Примеры:
  - **Неправильно**: `x=5`
  - **Правильно**: `x = 5`

#### **4. Использование `j_loads` или `j_loads_ns`**:
- Для чтения JSON или конфигурационных файлов замените стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
- Пример:

```python
# Неправильно:
with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Правильно:
data = j_loads('config.json')
```

#### **5. Сохранение комментариев**:
- Все существующие комментарии, начинающиеся с `#`, должны быть сохранены без изменений в разделе «Улучшенный код».
- Если комментарий кажется устаревшим или неясным, не изменяйте его. Вместо этого отметьте его в разделе «Изменения».

#### **6. Обработка `...` в коде**:
- Оставляйте `...` как указатели в коде без изменений.
- Не документируйте строки с `...`.
```

#### **7. Аннотации**
Для всех переменных должны быть определены аннотации типа. 
Для всех функций все входные и выходные параметры аннотириваны
Для все параметров должны быть аннотации типа.


### **8. webdriver**
В коде используется webdriver. Он импртируется из модуля `webdriver` проекта `hypotez`
```python
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
driver = Driver(Firefox)

Пoсле чего может использоваться как

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```

### Анализ кода `hypotez/src/endpoints/bots/whatsapp/whatsapp_sender.py`

#### 1. Блок-схема:

```mermaid
graph TD
    A[Начало: Получение пользовательских данных (номер телефона, количество сообщений, часы начала и конца)] --> B{Ввод номера телефона};
    B --> C{Ввод количества сообщений};
    C --> D{Ввод часа начала (0-23)};
    D --> E{Ввод часа окончания (0-23)};
    E --> F{Инициализация счетчика сообщений (message_count = 0)};
    F --> G{Цикл: message_count < num_messages};
    G -- Да --> H{Выбор случайного часа (start_hour, end_hour)};
    G -- Нет --> K[Конец];
    H --> I{Выбор случайной минуты (0-59)};
    I --> J{Выбор случайного сообщения из списка messages};
    J --> L[Вызов send_whatsapp_message(phone_number, random_message, random_hour, random_minutes)];
    L --> M{Увеличение счетчика сообщений (message_count += 1)};
    M --> G;
    
    subgraph Функция send_whatsapp_message
    SA[Начало функции: send_whatsapp_message(phone_number, message, hour, minutes)] --> SB{Отправка сообщения через pywhatkit.sendwhatmsg};
    SB -- Успешно --> SC[Ожидание загрузки WhatsApp Web (time.sleep(20))];
    SB -- Ошибка --> SE[Вывод сообщения об ошибке];
    SC --> SD[Эмуляция нажатия Enter с помощью pyautogui];
    SD --> SF[Вывод сообщения об успешной отправке];
    SF --> SG[Конец функции];
    SE --> SG;
    end
```

#### 2. Диаграмма:

```mermaid
graph TD
    A[whatsapp_sender.py] --> B(pywhatkit);
    A --> C(pyautogui);
    A --> D(pynput.keyboard);
    A --> E(emoji);
    A --> F(random);
    A --> G(time);
    
    B --> |Используется для| H[Отправки сообщений в WhatsApp];
    C --> |Используется для| I[Эмуляции нажатия клавиши Enter];
    D --> |Используется для| J[Управления клавиатурой];
    E --> |Используется для| K[Использования эмодзи в сообщениях];
    F --> |Используется для| L[Выбора случайных значений (часа, минуты, сообщения)];
    G --> |Используется для| M[Ожидания загрузки страницы];
```

**Объяснение зависимостей:**
- `pywhatkit`: Эта библиотека используется для автоматизации отправки сообщений в WhatsApp через веб-интерфейс.
- `pyautogui`: Эта библиотека используется для управления мышью и клавиатурой, в данном случае для эмуляции нажатия клавиши Enter.
- `pynput.keyboard`: Этот модуль используется для управления клавиатурой, конкретно для нажатия и отпускания клавиши Enter.
- `emoji`: Эта библиотека используется для работы с эмодзи в сообщениях.
- `random`: Этот модуль используется для генерации случайных чисел и выбора случайных сообщений из списка.
- `time`: Этот модуль используется для задержки выполнения программы, чтобы дать время для загрузки WhatsApp Web.

#### 3. Объяснение:

```python
import pywhatkit
import pyautogui
from pynput.keyboard import Key, Controller
import emoji
import random
import time

def send_whatsapp_message(phone_number: str, message: str, hour: int, minutes: int) -> None:
    """Sends a WhatsApp message using pywhatkit and pyautogui.
    Args:
        phone_number (str): The phone number to send the message to.
        message (str): The message to send.
        hour (int): The hour to send the message (0-23).
        minutes (int): The minutes to send the message (0-59).

    Returns:
        None: This function does not return anything.

    Raises:
        Exception: If there is an error sending the message.

    Example:
        >>> send_whatsapp_message("+1234567890", "Hello!", 10, 30)
        Message sent successfully!
    """
    try:
        pywhatkit.sendwhatmsg(phone_number, message, hour, minutes, wait_time=25, tab_close=True)
        time.sleep(20)  # Give time for WhatsApp Web to load
        keyboard = Controller()
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error sending message: {e}")


# Message bank with emojis
messages: list[str] = [
    "Hello! How are you? :slightly_smiling_face:",
    "Thinking of you! :heart:",
    "Just wanted to say hi! :waving_hand:",
    "I love you :heart_exclamation:",
    emoji.emojize("Have a wonderful day! :sun:")
]

# Get user inputs
phone_number: str = input("Enter the phone number with country code: ")
num_messages: int = int(input("Enter the number of messages to send: "))
start_hour: int = int(input("Enter the start hour (0-23): "))
end_hour: int = int(input("Enter the end hour (0-23): "))

message_count: int = 0
while message_count < num_messages:
    random_hour: int = random.randint(start_hour, end_hour)
    random_minutes: int = random.randint(0, 59)
    random_message: str = random.choice(messages)

    send_whatsapp_message(phone_number, random_message, random_hour, random_minutes)
    message_count += 1
```

**Импорты:**
- `pywhatkit`: Используется для отправки сообщений WhatsApp.
- `pyautogui`: Используется для автоматизации действий с клавиатурой, в частности, для нажатия клавиши Enter.
- `pynput.keyboard`: Используется для программного управления клавиатурой.
- `emoji`: Используется для работы с эмодзи в текстовых сообщениях.
- `random`: Используется для генерации случайных значений, таких как выбор случайного сообщения или времени отправки.
- `time`: Используется для добавления задержек в выполнение кода.

**Функция `send_whatsapp_message`:**
- Аргументы:
    - `phone_number` (str): Номер телефона получателя.
    - `message` (str): Текст сообщения.
    - `hour` (int): Час отправки сообщения (0-23).
    - `minutes` (int): Минуты отправки сообщения (0-59).
- Возвращаемое значение: `None`.
- Назначение: Отправляет сообщение WhatsApp с использованием библиотеки `pywhatkit`. После отправки, ждет некоторое время, чтобы страница WhatsApp Web успела загрузиться, затем эмулирует нажатие клавиши Enter для отправки сообщения. Если происходит ошибка, выводит сообщение об ошибке.
- Пример: `send_whatsapp_message("+1234567890", "Hello!", 10, 30)`

**Переменные:**
- `messages` (list[str]): Список сообщений для отправки, содержащий эмодзи.
- `phone_number` (str): Номер телефона, введенный пользователем.
- `num_messages` (int): Количество сообщений для отправки, введенное пользователем.
- `start_hour` (int): Начальный час для отправки сообщений, введенный пользователем.
- `end_hour` (int): Конечный час для отправки сообщений, введенный пользователем.
- `message_count` (int): Счетчик отправленных сообщений.
- `random_hour` (int): Случайный час для отправки сообщения.
- `random_minutes` (int): Случайная минута для отправки сообщения.
- `random_message` (str): Случайное сообщение из списка `messages`.

**Потенциальные ошибки и области для улучшения:**
- Отсутствует обработка ошибок при вводе данных пользователем (например, если пользователь вводит нечисловое значение для количества сообщений).
- Время ожидания (time.sleep) фиксировано, что может быть недостаточно в случае медленного интернет-соединения.
- Не предусмотрена возможность использования прокси или других способов обхода блокировок.
- Нет логирования с использованием модуля `logger` из `src.logger.logger`.
- Отсутствуют аннотации типов для всех переменных.

**Взаимосвязи с другими частями проекта:**
- Данный файл (`whatsapp_sender.py`) является частью модуля `whatsapp` в директории `src/endpoints/bots`. Он предназначен для автоматизации отправки сообщений WhatsApp.
- В текущем виде файл не использует другие части проекта, но его можно интегрировать с другими компонентами, например, с системой логирования или с модулем для управления конфигурацией.