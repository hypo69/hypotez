# Модуль `gpt_traigner.py`

## Обзор

Модуль `gpt_traigner.py` предназначен для сбора и обработки данных диалогов из HTML-файлов, полученных из ChatGPT, с целью обучения моделей машинного обучения. Он включает в себя функциональность извлечения текста диалогов, определения тональности и сохранения этих данных в различных форматах (CSV, JSONL и TXT) для дальнейшего использования.

## Подробней

Модуль предоставляет класс `GPT_Traigner`, который автоматизирует процесс извлечения данных из HTML-файлов, находящихся в указанной директории, и сохранения их в структурированном виде. Он использует веб-драйвер для загрузки HTML-файлов и извлечения контента. Собранные данные затем сохраняются в файлы форматов CSV, JSONL и TXT, что обеспечивает удобство для различных задач машинного обучения и анализа данных.

## Классы

### `GPT_Traigner`

**Описание**: Класс предназначен для сбора и обработки данных диалогов из HTML-файлов, полученных из ChatGPT.

**Атрибуты**:
- `driver`: Инстанс веб-драйвера (в данном случае, Chrome) для взаимодействия с веб-страницами.
- `gs`: Инстанс класса `GptGs` для доступа к путям и настройкам, связанным с Google Drive и ChatGPT.

**Методы**:
- `__init__()`: Инициализирует класс, создавая инстанс `GptGs`.
- `determine_sentiment(conversation_pair: dict[str, str], sentiment: str = 'positive') -> str`: Определяет тональность пары диалога.
- `save_conversations_to_jsonl(data: list[dict], output_file: str)`: Сохраняет пары диалогов в файл JSONL.
- `dump_downloaded_conversations()`: Собирает диалоги из HTML-файлов и сохраняет их в файлы CSV, JSONL и TXT.

### `__init__`

**Назначение**: Инициализирует класс `GPT_Traigner`.

**Параметры**:
- Нет.

**Возвращает**:
- Нет.

**Как работает функция**:
- Создает экземпляр класса `GptGs`.

### `determine_sentiment`

```python
def determine_sentiment(self, conversation_pair: dict[str, str], sentiment: str = 'positive') -> str:
    """ Определяет метку тональности для пары диалогов """
```

**Назначение**: Определяет тональность пары диалогов. В текущей реализации всегда возвращает "positive".

**Параметры**:
- `conversation_pair` (dict[str, str]): Пара диалогов (вопрос-ответ).
- `sentiment` (str, optional): Заданная тональность. По умолчанию 'positive'.

**Возвращает**:
- `str`: Строка "positive", если `sentiment` не пустая, иначе "negative".

**Как работает функция**:
- Если значение параметра `sentiment` истинно, функция возвращает строку "positive".
- В противном случае функция возвращает строку "negative".

**Примеры**:
```python
traigner = GPT_Traigner()
print(traigner.determine_sentiment({"user": "Привет", "assistant": "Здравствуйте"}, sentiment="good"))  # Вывод: positive
print(traigner.determine_sentiment({"user": "Привет", "assistant": "Здравствуйте"}, sentiment=""))      # Вывод: negative
```

### `save_conversations_to_jsonl`

```python
def save_conversations_to_jsonl(self, data: list[dict], output_file: str):
    """ Сохраняет пары диалогов в JSONL файл """
```

**Назначение**: Сохраняет список словарей, представляющих пары диалогов, в файл в формате JSONL (JSON Lines).

**Параметры**:
- `data` (list[dict]): Список словарей, где каждый словарь представляет собой пару диалогов.
- `output_file` (str): Путь к файлу, в который будут сохранены данные.

**Как работает функция**:
- Открывает файл для записи с указанной кодировкой (`utf-8`).
- Итерируется по списку `data`.
- Для каждого элемента (словаря) в списке:
    - Очищает строки в словаре с помощью функции `clean_string`.
    - Преобразует очищенный словарь в JSON-формат с помощью `j_dumps`.
    - Записывает JSON-представление словаря в файл, добавляя символ новой строки (`\n`).

**Примеры**:
```python
from pathlib import Path
from src.utils.jjson import j_dumps
from src.utils.string import clean_string

# Пример данных
data = [{"user": "Привет!", "assistant": "Здравствуйте."}, {"user": "Как дела?", "assistant": "Всё хорошо."}]
output_file = "conversations.jsonl"

# Сохранение данных в файл
traigner = GPT_Traigner()
traigner.save_conversations_to_jsonl(data, output_file)

# Проверка содержимого файла (пример)
with open(output_file, 'r', encoding='utf-8') as f:
    print(f.readline())  # {"user": "Привет!", "assistant": "Здравствуйте."}
```

### `dump_downloaded_conversations`

```python
def dump_downloaded_conversations(self):
    """ Собирает диалоги со страницы chatgpt """
```

**Назначение**: Извлекает диалоги из HTML-файлов, находящихся в указанной директории, и сохраняет их в форматах CSV, JSONL и TXT.

**Как работает функция**:
1. Определяет директорию, содержащую HTML-файлы с диалогами.
2. Получает список всех HTML-файлов в этой директории.
3. Итерируется по каждому HTML-файлу:
   - Формирует URI файла.
   - Использует `self.driver.get_url()` для загрузки HTML-контента файла в веб-драйвер.
   - Использует `self.driver.execute_locator()` с локаторами `locator.user` и `locator.assistant` для извлечения элементов, содержащих сообщения пользователя и ассистента, соответственно.
   - Извлекает текст из найденных элементов и сохраняет их в списки `user_content` и `assistant_content`.
   - Проверяет, что оба списка `user_content` и `assistant_content` не пусты. Если они пусты, логирует ошибку и переходит к следующему файлу.
   - Объединяет содержимое списков `user_content` и `assistant_content` в пары "вопрос-ответ".
   - Формирует DataFrame из каждой пары, добавляя информацию о ролях ("user", "assistant") и тональности ("neutral").
   - Накапливает DataFrame'ы в списке `all_data`.
4. После обработки всех файлов:
   - Объединяет все DataFrame'ы из `all_data` в один DataFrame `all_data_df`.
   - Сохраняет `all_data_df` в CSV-файл.
   - Сохраняет `all_data_df` в JSONL-файл.
   - Извлекает весь текст из колонки 'content' DataFrame'а, объединяет в одну строку и сохраняет в TXT-файл.

**Примеры**:

```python
from pathlib import Path
import pandas as pd
from src.utils.jjson import j_loads_ns
from src.webdriver.driver import Driver, Chrome
from src.logger.logger import logger
from src import gs
from itertools import zip_longest
from src.utils.jjson import clean_string
class MockDriver:
    def __init__(self):
        pass
    def get_url(self, file_uri:str):
        print (f'Чтение файла {file_uri}')
    def execute_locator(self, locator:dict):
        if locator == 'user':
            return ['text user 1', 'text user 2']
        else:
            return ['text bot 1', 'text bot 2']
class MockGs:
    def __init__(self):
        self.path = MockPath()
class MockPath:
    def __init__(self):
        self.google_drive = 'path'
class MockGPT_Traigner(GPT_Traigner):
    driver = MockDriver()
    gs = MockGs()
    def __init__(self):
        pass

    def determine_sentiment(self, conversation_pair: dict[str, str], sentiment: str = 'positive') -> str:
        return 'positive'
output_file_csv = Path('./all_conversations.csv')
output_file_json = Path('./all_conversations.jsonl')
output_file_txt = Path('./raw_conversations.txt')
if output_file_csv.exists():
    output_file_csv.unlink()
if output_file_json.exists():
    output_file_json.unlink()
if output_file_txt.exists():
    output_file_txt.unlink()
traigner = MockGPT_Traigner()
traigner.dump_downloaded_conversations()
print (f'Файл csv существует {output_file_csv.exists()}')
print (f'Файл json существует {output_file_json.exists()}')
print (f'Файл txt существует {output_file_txt.exists()}')
```

## Примеры

```python
traigner = GPT_Traigner()
traigner.dump_downloaded_conversations()
```

## Запуск кода

```python
traigner = GPT_Traigner()
traigner.dump_downloaded_conversations()
model = Model()
model.stream_w(data_file_path=Path(gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.csv'))
```
Здесь создается экземпляр класса `GPT_Traigner`, вызывается метод `dump_downloaded_conversations()` для извлечения и сохранения данных диалогов. Затем создается экземпляр класса `Model` и вызывается метод `stream_w()` для обработки CSV-файла с данными диалогов.