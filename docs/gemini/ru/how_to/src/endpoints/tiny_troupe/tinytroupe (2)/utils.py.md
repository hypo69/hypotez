### **Инструкция: Как использовать блок кода с утилитами**
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет набор утилит и вспомогательных функций, охватывающих различные аспекты разработки, такие как обработка ввода и вывода модели, управление моделью, валидация данных, prompt engineering, работа с HTML, преобразование текста, работа с датой и временем, управление файлами конфигурации, логирование, а также сериализация и десериализация объектов JSON.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   В начале файла импортируются необходимые модули, такие как `re`, `json`, `os`, `sys`, `hashlib`, `textwrap`, `logging`, `chevron`, `copy`, `datetime`, `Path`, `configparser` и `typing`. Также инициализируется logger для ведения журнала событий.

2. **Использование утилит для обработки ввода модели**:
   - Функция `compose_initial_LLM_messages_with_templates` формирует начальные сообщения для языковой модели (LLM), используя шаблоны и параметры конфигурации.
     - Определяются пути к шаблонам системных и пользовательских сообщений.
     - Загружаются шаблоны сообщений и подставляются значения из `rendering_configs`.
     - Возвращается список сообщений в формате, необходимом для LLM.

3. **Использование утилит для обработки вывода модели**:
   - Функция `extract_json` извлекает JSON-объект из текста, удаляя все, что находится до и после JSON-объекта.
     - Используются регулярные выражения для удаления лишнего текста до и после JSON.
     - Удаляются недопустимые escape-последовательности.
     - JSON парсится и возвращается как словарь.
   - Функция `extract_code_block` извлекает блок кода из текста, обрамленного тройными обратными кавычками.
     - Используются регулярные выражения для удаления текста до и после блока кода.
     - Возвращается извлеченный блок кода.

4. **Использование утилит для управления моделью**:
   - Декоратор `repeat_on_error` позволяет повторно вызывать функцию в случае возникновения исключения.
     - Принимает количество попыток `retries` и список исключений `exceptions`.
     - В случае возникновения исключения из списка, функция вызывается повторно до указанного количества раз.

5. **Использование утилит для валидации данных**:
   - Функция `check_valid_fields` проверяет, что словарь содержит только допустимые ключи.
     - Принимает словарь `obj` и список допустимых ключей `valid_fields`.
     - Вызывает исключение `ValueError`, если найден недопустимый ключ.
   - Функция `sanitize_raw_string` очищает строку от недопустимых символов и ограничивает ее длину.
     - Кодирует строку в UTF-8, игнорируя ошибки, и декодирует обратно.
     - Обрезает строку до максимальной длины, допустимой в Python.
   - Функция `sanitize_dict` очищает словарь, используя `sanitize_raw_string` для строкового представления словаря.
     - Преобразует словарь в JSON, очищает строку и парсит обратно в словарь.

6. **Использование утилит для prompt engineering**:
   - Функция `add_rai_template_variables_if_enabled` добавляет переменные для RAI (Responsible AI) в словарь шаблонов, если соответствующие настройки включены в конфигурационном файле.
     - Проверяет, включены ли настройки предотвращения вредоносного контента и нарушения авторских прав.
     - Загружает содержимое файлов с disclaimer'ами и добавляет их в словарь.

7. **Использование утилит для работы с HTML**:
   - Функция `inject_html_css_style_prefix` добавляет префикс к атрибутам `style` в HTML-строке.
     - Находит все атрибуты `style` и добавляет к ним указанный префикс.
   - Функция `break_text_at_length` обрезает текст или JSON до указанной длины, добавляя " (...)".
     - Если входные данные - словарь, они преобразуются в JSON.
     - Если длина текста превышает `max_length`, текст обрезается и добавляется индикатор обрыва.

8. **Использование утилит для работы с датой и временем**:
   - Функция `pretty_datetime` форматирует объект `datetime` в удобочитаемую строку.
     - Использует `strftime` для форматирования даты и времени.

9. **Использование утилит для работы с текстом**:
   - Функция `dedent` удаляет отступы из текста.
     - Использует `textwrap.dedent` для удаления общих отступов.

10. **Использование утилит для работы с файлами конфигурации**:
    - Функция `read_config_file` считывает конфигурационный файл `config.ini`.
        - Сначала пытается прочитать конфигурацию из файла в директории модуля.
        - Затем пытается переопределить значения из файла в текущей рабочей директории.
        - Использует кеширование для повышения производительности.
    - Функция `pretty_print_config` выводит конфигурацию в удобочитаемом формате.
        - Перебирает секции и элементы конфигурации и выводит их на экран.

11. **Использование утилит для логирования**:
    - Функция `start_logger` инициализирует логгер.
        - Устанавливает уровень логирования на основе конфигурации.
        - Создает обработчик консольного вывода.
        - Устанавливает форматтер для сообщений лога.

12. **Использование класса `JsonSerializableRegistry` для сериализации и десериализации JSON**:
    - Класс `JsonSerializableRegistry` предоставляет механизм для сериализации и десериализации объектов в JSON.
        - Метод `to_json` преобразует объект в JSON-представление.
        - Метод `from_json` создает экземпляр класса из JSON-представления.
        - Поддерживает наследование и пользовательские инициализаторы.

13. **Использование декоратора `post_init` для выполнения постобработки после инициализации объекта**:
    - Декоратор `post_init` позволяет выполнять дополнительную инициализацию объекта после вызова `__init__`.
        - Если у класса есть метод `_post_init`, он будет вызван после `__init__`.

14. **Использование других утилит**:
    - Функция `name_or_empty` возвращает имя объекта или пустую строку, если объект равен `None`.
    - Функция `custom_hash` генерирует хеш для объекта, предварительно преобразовав его в строку.
    - Функция `fresh_id` генерирует уникальные идентификаторы.

Пример использования
-------------------------

```python
from src.endpoints.tiny_troupe.tinytroupe.utils import (
    compose_initial_LLM_messages_with_templates,
    extract_json,
    repeat_on_error,
    check_valid_fields,
    sanitize_raw_string,
    add_rai_template_variables_if_enabled,
    break_text_at_length,
    pretty_datetime,
    read_config_file,
    JsonSerializableRegistry,
    custom_hash,
    fresh_id
)
import logging
import configparser
from datetime import datetime

# Настройка логирования
config = read_config_file(verbose=False)
logger = logging.getLogger("example")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Пример использования compose_initial_LLM_messages_with_templates
messages = compose_initial_LLM_messages_with_templates(
    system_template_name="system_prompt.md", 
    user_template_name="user_prompt.md", 
    rendering_configs={"task": "Summarize the document"}
)
print(f"Initial LLM messages: {messages}")

# Пример использования extract_json
json_string = 'Some text {"key": "value"} more text'
extracted_json = extract_json(json_string)
print(f"Extracted JSON: {extracted_json}")

# Пример использования repeat_on_error
def risky_function():
    raise ValueError("Something went wrong")

@repeat_on_error(retries=3, exceptions=[ValueError])
def safe_function():
    return risky_function()

try:
    safe_function()
except ValueError as e:
    print(f"Function failed after multiple retries: {e}")

# Пример использования check_valid_fields
data = {"name": "John", "age": 30, "city": "New York"}
valid_fields = ["name", "age"]
try:
    check_valid_fields(data, valid_fields)
except ValueError as e:
    print(f"Validation error: {e}")

# Пример использования sanitize_raw_string
raw_string = "Invalid char\x01acters"
sanitized_string = sanitize_raw_string(raw_string)
print(f"Sanitized string: {sanitized_string}")

# Пример использования add_rai_template_variables_if_enabled
template_vars = {}
updated_template_vars = add_rai_template_variables_if_enabled(template_vars)
print(f"Updated template variables: {updated_template_vars}")

# Пример использования break_text_at_length
long_text = "This is a very long text that needs to be broken."
short_text = break_text_at_length(long_text, max_length=20)
print(f"Shortened text: {short_text}")

# Пример использования pretty_datetime
now = datetime.now()
pretty_date = pretty_datetime(now)
print(f"Pretty date: {pretty_date}")

# Пример использования read_config_file
config = read_config_file(verbose=False)
print(f"Config sections: {config.sections()}")

# Пример использования JsonSerializableRegistry
class ExampleClass(JsonSerializableRegistry):
    serializable_attributes = ["name", "age"]

    def __init__(self, name, age):
        self.name = name
        self.age = age

obj = ExampleClass(name="Alice", age=25)
json_data = obj.to_json()
print(f"JSON data: {json_data}")
restored_obj = ExampleClass.from_json(json_data)
print(f"Restored object name: {restored_obj.name}, age: {restored_obj.age}")

# Пример использования custom_hash
data = {"key": "value"}
hashed_data = custom_hash(data)
print(f"Hashed data: {hashed_data}")

# Пример использования fresh_id
new_id = fresh_id()
print(f"Fresh ID: {new_id}")
```