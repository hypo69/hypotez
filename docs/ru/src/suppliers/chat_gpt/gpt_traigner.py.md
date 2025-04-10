# Модуль для обучения GPT моделей

## Обзор

Модуль `gpt_traigner.py` предназначен для обучения моделей GPT на основе данных, собранных из истории переписки с ChatGPT. Он включает в себя функциональность для извлечения диалогов из HTML-файлов, сохранения их в различных форматах (CSV, JSONL, TXT) и последующей передачи этих данных в модель для обучения.

## Подробнее

Модуль предоставляет класс `GPT_Traigner`, который автоматизирует процесс сбора и подготовки данных для обучения GPT моделей. Он использует веб-драйвер для извлечения диалогов из HTML-файлов, а также включает методы для определения сентимента сообщений и сохранения данных в различных форматах. Код использует модуль `src.logger.logger` для логирования.

## Классы

### `GPT_Traigner`

**Описание**: Класс предназначен для сбора и подготовки данных для обучения моделей GPT. Он извлекает диалоги из HTML-файлов, сохраняет их в различных форматах (CSV, JSONL, TXT) и предоставляет методы для определения сентимента сообщений.

**Атрибуты**:

-   `driver`: Инстанс веб-драйвера (Chrome) для взаимодействия с веб-страницами.
-   `gs`: Инстанс класса `GptGs` для работы с Google Storage.

**Методы**:

-   `__init__()`: Инициализирует класс `GPT_Traigner`.
-   `determine_sentiment(conversation_pair: dict[str, str], sentiment: str = 'positive') -> str`: Определяет сентимент для пары диалогов.
-   `save_conversations_to_jsonl(data: list[dict], output_file: str)`: Сохраняет пары диалогов в файл JSONL.
-   `dump_downloaded_conversations()`: Собирает диалоги со страниц ChatGPT и сохраняет их в файлы CSV, JSONL и TXT.

### `__init__`

```python
    def __init__(self):
        """"""
        ...
        self.gs = GptGs()
```

**Назначение**: Инициализирует класс `GPT_Traigner` и создает инстанс класса `GptGs`.

**Как работает функция**:

-   Инициализирует экземпляр класса `GPT_Traigner`.
-   Создает экземпляр класса `GptGs` и сохраняет его в атрибуте `self.gs`.

**Примеры**:

```python
traigner = GPT_Traigner()
```

### `determine_sentiment`

```python
    def determine_sentiment(self, conversation_pair: dict[str, str], sentiment: str = 'positive') -> str:
        """ Determine sentiment label for a conversation pair """
        ...
        if sentiment:
            return "positive"
        else:
            return "negative"
```

**Назначение**: Определяет сентимент для пары диалогов. В текущей реализации всегда возвращает "positive", если sentiment не пустая строка, и "negative" в противном случае.

**Параметры**:

-   `conversation_pair` (dict[str, str]): Словарь, содержащий пару диалогов (например, вопрос пользователя и ответ ассистента).
-   `sentiment` (str, optional): Строка, указывающая на сентимент. По умолчанию 'positive'.

**Возвращает**:

-   `str`: "positive", если sentiment не пустая строка, иначе "negative".

**Как работает функция**:

-   Принимает словарь `conversation_pair`, содержащий пару диалогов.
-   Проверяет, является ли строка `sentiment` не пустой.
-   Возвращает "positive", если `sentiment` не пустая строка, иначе возвращает "negative".

**Примеры**:

```python
traigner = GPT_Traigner()
conversation_pair = {"user": "Hello", "assistant": "Hi"}
sentiment = "positive"
result = traigner.determine_sentiment(conversation_pair, sentiment)
print(result)  # Вывод: positive

sentiment = ""
result = traigner.determine_sentiment(conversation_pair, sentiment)
print(result)  # Вывод: negative
```

### `save_conversations_to_jsonl`

```python
    def save_conversations_to_jsonl(self, data: list[dict], output_file: str):
        """ Save conversation pairs to a JSONL file """
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(j_dumps(clean_string(item)) + "\n")
```

**Назначение**: Сохраняет список пар диалогов в файл в формате JSONL.

**Параметры**:

-   `data` (list[dict]): Список словарей, где каждый словарь представляет собой пару диалогов.
-   `output_file` (str): Путь к файлу, в который будут сохранены данные.

**Как работает функция**:

-   Открывает файл `output_file` для записи в кодировке UTF-8.
-   Итерируется по списку `data`.
-   Для каждого элемента (словаря) в списке:
    -   Очищает строку, используя `clean_string(item)`.
    -   Преобразует словарь в JSON-строку с помощью `j_dumps()`.
    -   Записывает JSON-строку в файл, добавляя символ новой строки `\n`.

**Примеры**:

```python
traigner = GPT_Traigner()
data = [{"user": "Hello", "assistant": "Hi"}, {"user": "How are you?", "assistant": "I'm fine."}]
output_file = "conversations.jsonl"
traigner.save_conversations_to_jsonl(data, output_file)
```

### `dump_downloaded_conversations`

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

            for user_text, assistant_text in zip_longest(user_content, assistant_content):\
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

**Назначение**: Собирает диалоги со страниц ChatGPT, извлекая их из HTML-файлов, и сохраняет полученные данные в форматах CSV, JSONL и TXT.

**Как работает функция**:

1.  Определяет директорию, в которой хранятся HTML-файлы с диалогами.
2.  Собирает список всех HTML-файлов в этой директории.
3.  Инициализирует пустой список `all_data` для хранения извлеченных диалогов и счетчик `counter`.
4.  Итерируется по каждому HTML-файлу:
    -   Формирует URI файла.
    -   Использует `self.driver.get_url(file_uri)` для открытия HTML-файла в браузере, управляемом веб-драйвером.
    -   Использует `self.driver.execute_locator(locator.user)` и `self.driver.execute_locator(locator.assistant)` для извлечения элементов, содержащих сообщения пользователя и ассистента, соответственно. Локаторы для этих элементов определены в `locator`.
    -   Извлекает текст из найденных элементов и сохраняет их в списки `user_content` и `assistant_content`. Если элементы не найдены, то `user_content` и `assistant_content` устанавливаются в `None`.
    -   Проверяет, что хотя бы один из списков `user_content` или `assistant_content` содержит данные. Если оба списка пусты, логирует ошибку и переходит к следующему файлу.
    -   Итерируется по парам сообщений пользователя и ассистента, используя `zip_longest` для обработки ситуаций, когда один из участников диалога прислал больше сообщений, чем другой.
    -   Для каждой пары сообщений создает словарь `data`, содержащий роли (user, assistant), контент (тексты сообщений) и сентимент (neutral).
    -   Преобразует словарь `data` в DataFrame и добавляет его в список `all_data`.
    -   Выводит в консоль номер обработанного файла и путь к нему.
    -   Увеличивает счетчик `counter`.
5.  После обработки всех файлов:
    -   Проверяет, что список `all_data` не пуст.
    -   Объединяет все DataFrame из списка `all_data` в один DataFrame `all_data_df`.
    -   Сохраняет `all_data_df` в CSV-файл (`all_conversations.csv`).
    -   Сохраняет `all_data_df` в JSONL-файл (`all_conversations.jsonl`).
    -   Извлекает все тексты сообщений из столбца `content` DataFrame, объединяет их в одну строку `raw_conversations` и сохраняет в TXT-файл (`raw_conversations.txt`).

**Параметры**:

-   Отсутствуют.

**Возвращает**:

-   Отсутствует.

**Используемые веб-элементы и локаторы**:

-   `locator.user`: Локатор для элементов, содержащих сообщения пользователя.
-   `locator.assistant`: Локатор для элементов, содержащих сообщения ассистента.

**Примеры**:

```python
traigner = GPT_Traigner()
traigner.dump_downloaded_conversations()
```

## Параметры класса

-   `locator`: JSON, загруженный из файла `chat.json`, содержащий локаторы для элементов на странице ChatGPT.

## Примеры

```python
# Пример использования класса GPT_Traigner
traigner = GPT_Traigner()
traigner.dump_downloaded_conversations()

model = Model()
model.stream_w(data_file_path=Path(gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.csv'))
```