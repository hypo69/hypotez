# Модуль `gpt_traigner.py`

## Обзор

Модуль предназначен для обучения моделей GPT на основе данных, собранных из истории чатов. Он включает в себя функциональность для определения тональности разговоров, сохранения этих разговоров в формате JSONL, сбора данных из HTML-файлов, содержащих историю чатов с ChatGPT, и сохранения этих данных в различных форматах (CSV, JSONL, TXT).

## Подробнее

Модуль содержит класс `GPT_Traigner`, который выполняет основные задачи по обработке и подготовке данных для обучения моделей GPT. Он использует веб-драйвер для извлечения данных из HTML-файлов, содержащих историю чатов, и сохраняет эти данные в различных форматах для дальнейшего использования.

## Классы

### `GPT_Traigner`

**Описание**: Класс для обучения моделей GPT на основе истории чатов.

**Атрибуты**:
- `driver`: Инстанс веб-драйвера для взаимодействия с веб-страницами. Определен как `Driver(Chrome)`.
- `gs`: Инстанс класса `GptGs` для доступа к конфигурационным данным.

**Методы**:

- `__init__`: Инициализирует класс `GPT_Traigner`, создает инстанс класса `GptGs`.
- `determine_sentiment`: Определяет тональность пары реплик в разговоре.
- `save_conversations_to_jsonl`: Сохраняет пары реплик в формате JSONL.
- `dump_downloaded_conversations`: Собирает разговоры со страниц ChatGPT, сохраняет их в CSV, JSONL и TXT форматы.

## Методы класса

### `__init__`

**Назначение**: Инициализация класса `GPT_Traigner`.

```python
def __init__(self):
    """ """
    ...
    self.gs = GptGs()
```

**Как работает функция**:
- Инициализирует атрибут `gs` как экземпляр класса `GptGs`.

**Примеры**:

```python
traigner = GPT_Traigner()
```

### `determine_sentiment`

**Назначение**: Определяет тональность пары реплик в разговоре.

```python
def determine_sentiment(self, conversation_pair: dict[str, str], sentiment: str = 'positive') -> str:
    """ Determine sentiment label for a conversation pair """
    ...
    if sentiment:
        return "positive"
    else:
        return "negative"
```

**Параметры**:
- `conversation_pair` (dict[str, str]): Словарь, содержащий пару реплик (вопрос-ответ) из разговора.
- `sentiment` (str, optional): Предполагаемая тональность разговора. По умолчанию 'positive'.

**Возвращает**:
- `str`: "positive", если тональность положительная, "negative" в противном случае.

**Как работает функция**:
- Если передан аргумент `sentiment`, функция возвращает "positive". В противном случае возвращает "negative".

**Примеры**:

```python
traigner = GPT_Traigner()
conversation = {"user": "Привет!", "assistant": "Здравствуйте!"}
sentiment = traigner.determine_sentiment(conversation)
print(sentiment)  # Вывод: positive

sentiment = traigner.determine_sentiment(conversation, sentiment='')
print(sentiment) # Вывод: negative
```

### `save_conversations_to_jsonl`

**Назначение**: Сохраняет пары реплик в формате JSONL в указанный файл.

```python
def save_conversations_to_jsonl(self, data: list[dict], output_file: str):
    """ Save conversation pairs to a JSONL file """
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(j_dumps(clean_string(item)) + "\n")
```

**Параметры**:
- `data` (list[dict]): Список словарей, где каждый словарь содержит пару реплик (вопрос-ответ) из разговора.
- `output_file` (str): Путь к файлу, в который нужно сохранить данные в формате JSONL.

**Как работает функция**:
- Открывает файл в режиме записи (`'w'`) с кодировкой UTF-8.
- Итерируется по списку `data`.
- Для каждого элемента (словаря) вызывает `j_dumps` для преобразования словаря в JSON-строку.
- Очищает строку с помощью `clean_string`.
- Записывает JSON-строку в файл, добавляя символ новой строки (`\n`) для разделения записей.

**Примеры**:

```python
from pathlib import Path
traigner = GPT_Traigner()
data = [{"user": "Привет!", "assistant": "Здравствуйте!"}, {"user": "Как дела?", "assistant": "Все хорошо!"}]
output_file = Path("conversations.jsonl")
traigner.save_conversations_to_jsonl(data, str(output_file))
```

### `dump_downloaded_conversations`

**Назначение**: Собирает разговоры со страниц ChatGPT, извлекая данные из HTML-файлов, и сохраняет их в форматах CSV, JSONL и TXT.

```python
def dump_downloaded_conversations(self):
    """ Collect conversations from the chatgpt page """
    ...
    conversation_directory = Path(gs.path.google_drive / 'chat_gpt' / 'conversation')
    html_files = conversation_directory.glob("*.html")

    all_data = []
    counter: int = 0  # <- counter

    for local_file_path in html_files:
        # Get the HTML content
        file_uri = local_file_path.resolve().as_uri()
        self.driver.get_url(file_uri)
        
        user_elements = self.driver.execute_locator(locator.user)
        assistant_elements = self.driver.execute_locator(locator.assistant)
        
        user_content = [element.text for element in user_elements] if isinstance(user_elements, list) else [user_elements.text] if user_elements  else None
        assistant_content = [element.text for element in assistant_elements] if isinstance(assistant_elements, list) else [assistant_elements.text] if assistant_elements  else None

        if not user_content and not assistant_content:
            logger.error(f"Где данные?")
            continue

        for user_text, assistant_text in zip_longest(user_content, assistant_content):
            if user_text and assistant_text:
                data = {
                    'role': ['user', 'assistant'],
                    'content': [clean_string(user_text), clean_string(assistant_text)],
                    'sentiment': ['neutral', 'neutral']
                }
                all_data.append(pd.DataFrame(data))
                print(f'{counter} - {local_file_path}')
                counter += 1

    if all_data:
        all_data_df = pd.concat(all_data, ignore_index=True)

        # Save all accumulated results to a single CSV file
        csv_file_path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.csv'
        all_data_df.to_csv(csv_file_path, index=False, encoding='utf-8')

        # Save all accumulated results to a single JSONL file
        jsonl_file_path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.jsonl'
        all_data_df.to_json(jsonl_file_path, orient='records', lines=True, force_ascii=False)
        
        # Save raw conversations to a single line without formatting
        raw_conversations = ' '.join(all_data_df['content'].dropna().tolist())
        raw_file_path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'raw_conversations.txt'
        with open(raw_file_path, 'w', encoding='utf-8') as raw_file:
            raw_file.write(raw_conversations)
```

**Как работает функция**:

1.  **Подготовка**:
    *   Определяет директорию, где хранятся HTML-файлы с разговорами, используя `gs.path.google_drive / 'chat_gpt' / 'conversation'`.
    *   Получает список всех HTML-файлов в этой директории, используя `conversation_directory.glob("*.html")`.
    *   Инициализирует пустой список `all_data` для хранения данных из всех файлов.
    *   Инициализирует счетчик `counter` для отслеживания обработанных файлов.

2.  **Обработка файлов**:
    *   Итерируется по каждому `local_file_path` в списке `html_files`.
    *   Преобразует путь к файлу в URI (Uniform Resource Identifier), чтобы его можно было открыть в браузере: `file_uri = local_file_path.resolve().as_uri()`.
    *   Открывает HTML-файл в браузере, используя веб-драйвер: `self.driver.get_url(file_uri)`.
    *   Извлекает элементы, соответствующие репликам пользователя и ассистента, с использованием локаторов, определенных в `locator.user` и `locator.assistant`:
        *   `user_elements = self.driver.execute_locator(locator.user)`
        *   `assistant_elements = self.driver.execute_locator(locator.assistant)`
    *   Извлекает текстовое содержимое из найденных элементов. Если `user_elements` или `assistant_elements` являются списком, извлекает текст из каждого элемента списка. Если это единичный элемент, извлекает текст из него. Если элементы не найдены, присваивает `None`:

        ```python
        user_content = [element.text for element in user_elements] if isinstance(user_elements, list) else [user_elements.text] if user_elements  else None
        assistant_content = [element.text for element in assistant_elements] if isinstance(assistant_elements, list) else [assistant_elements.text] if assistant_elements  else None
        ```
    *   Проверяет, что из файла были извлечены какие-либо данные. Если `user_content` и `assistant_content` пусты, логирует ошибку и переходит к следующему файлу:

        ```python
        if not user_content and not assistant_content:
            logger.error(f"Где данные?")
            continue
        ```
    *   Итерируется по парам реплик пользователя и ассистента, используя `zip_longest` для обработки случаев, когда количество реплик пользователя и ассистента не совпадает:

        ```python
        for user_text, assistant_text in zip_longest(user_content, assistant_content):
            if user_text and assistant_text:
                data = {
                    'role': ['user', 'assistant'],
                    'content': [clean_string(user_text), clean_string(assistant_text)],
                    'sentiment': ['neutral', 'neutral']
                }
                all_data.append(pd.DataFrame(data))
                print(f'{counter} - {local_file_path}')
                counter += 1
        ```

        *   Для каждой пары реплик создается словарь `data`, содержащий роли (`user`, `assistant`), содержимое реплик (очищенное с помощью `clean_string`) и тональность (`neutral`).
        *   Этот словарь преобразуется в DataFrame с помощью `pd.DataFrame(data)` и добавляется в список `all_data`.
        *   Выводит сообщение в консоль с номером обработанного файла и его путем.
        *   Увеличивает счетчик `counter`.

3.  **Сохранение данных**:
    *   После обработки всех файлов, проверяет, что были собраны какие-либо данные: `if all_data:`.
    *   Объединяет все DataFrame из списка `all_data` в один DataFrame с помощью `pd.concat(all_data, ignore_index=True)`.
    *   Определяет пути для сохранения данных в форматах CSV, JSONL и TXT:

        ```python
        csv_file_path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.csv'
        jsonl_file_path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.jsonl'
        raw_file_path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'raw_conversations.txt'
        ```
    *   Сохраняет данные в формате CSV:

        ```python
        all_data_df.to_csv(csv_file_path, index=False, encoding='utf-8')
        ```
    *   Сохраняет данные в формате JSONL:

        ```python
        all_data_df.to_json(jsonl_file_path, orient='records', lines=True, force_ascii=False)
        ```
    *   Сохраняет данные в формате TXT:

        ```python
        raw_conversations = ' '.join(all_data_df['content'].dropna().tolist())
        with open(raw_file_path, 'w', encoding='utf-8') as raw_file:
            raw_file.write(raw_conversations)
        ```

        *   Извлекает содержимое всех реплик из столбца `'content'` DataFrame, удаляя пропущенные значения (`dropna()`), и объединяет их в одну строку через пробел.
        *   Записывает эту строку в файл `raw_file_path`.

**Примеры**:

```python
traigner = GPT_Traigner()
traigner.dump_downloaded_conversations()
```

## Параметры класса

- `driver`: Инстанс веб-драйвера для управления браузером. Используется Chrome.
- `gs`: Инстанс класса `GptGs` для доступа к конфигурационным данным.

## Примеры

```python
from pathlib import Path
from src.suppliers.chat_gpt.gpt_traigner import GPT_Traigner

# Пример создания экземпляра класса GPT_Traigner
traigner = GPT_Traigner()

# Пример определения тональности разговора
conversation = {"user": "Привет!", "assistant": "Здравствуйте!"}
sentiment = traigner.determine_sentiment(conversation)
print(f"Sentiment: {sentiment}")

# Пример сохранения разговоров в файл JSONL
data = [{"user": "Привет!", "assistant": "Здравствуйте!"}, {"user": "Как дела?", "assistant": "Все хорошо!"}]
output_file = Path("conversations.jsonl")
traigner.save_conversations_to_jsonl(data, str(output_file))

# Пример сбора и сохранения разговоров из HTML-файлов
#traigner.dump_downloaded_conversations()  # Закомментировано, чтобы не запускать функцию автоматически