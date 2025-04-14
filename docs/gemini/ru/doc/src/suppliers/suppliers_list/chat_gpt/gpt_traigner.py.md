# Модуль для обучения GPT моделей на основе данных из ChatGPT

## Обзор

Модуль предназначен для обучения моделей GPT на основе данных, полученных из истории разговоров ChatGPT. Он включает в себя функциональность для извлечения данных из HTML-файлов, сохранения их в различных форматах (CSV, JSONL, TXT) и использования для обучения моделей.

## Подробнее

Модуль `gpt_traigner.py` предоставляет класс `GPT_Traigner`, который автоматизирует процесс сбора, обработки и подготовки данных для обучения GPT моделей. Он использует Selenium WebDriver для извлечения данных из HTML-файлов с историей разговоров ChatGPT, а также библиотеки `pandas` для обработки и сохранения данных в различных форматах.

## Классы

### `GPT_Traigner`

**Описание**: Класс для обучения GPT моделей на основе данных из ChatGPT.

**Атрибуты**:

- `driver`: Инстанс веб-драйвера для взаимодействия с веб-страницами. Определен как `Driver(Chrome)`.
- `gs`: Инстанс класса `GptGs`, используемый для доступа к путям и настройкам, связанным с Google Drive и ChatGPT.

**Методы**:

- `__init__`: Инициализирует класс `GPT_Traigner`.
- `determine_sentiment`: Определяет метку настроения для пары реплик в разговоре.
- `save_conversations_to_jsonl`: Сохраняет пары реплик в файл JSONL.
- `dump_downloaded_conversations`: Собирает реплики из HTML-файлов ChatGPT и сохраняет их в CSV, JSONL и TXT форматы.

#### `__init__`

```python
    def __init__(self):
        """"""
        ...
        self.gs = GptGs()
```

**Назначение**: Инициализирует класс `GPT_Traigner`, создает экземпляр класса `GptGs`.

**Как работает функция**:
- Инициализирует экземпляр класса `GptGs` и присваивает его атрибуту `self.gs`.

#### `determine_sentiment`

```python
    def determine_sentiment(self, conversation_pair: dict[str, str], sentiment: str = 'positive') -> str:
        """ Determine sentiment label for a conversation pair """
        ...
        if sentiment:
            return "positive"
        else:
            return "negative"
```

**Назначение**: Определяет метку настроения для пары реплик в разговоре.

**Параметры**:
- `conversation_pair` (dict[str, str]): Словарь, содержащий пару реплик (например, вопрос и ответ).
- `sentiment` (str, optional): Строка, указывающая на настроение. По умолчанию `'positive'`.

**Возвращает**:
- `str`: Метка настроения (`"positive"` или `"negative"`).

**Как работает функция**:
- Если параметр `sentiment` не пустой, возвращает строку `"positive"`.
- В противном случае возвращает строку `"negative"`.

#### `save_conversations_to_jsonl`

```python
    def save_conversations_to_jsonl(self, data: list[dict], output_file: str):
        """ Save conversation pairs to a JSONL file """
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(j_dumps(clean_string(item)) + "\n")
```

**Назначение**: Сохраняет список словарей с репликами в файл JSONL.

**Параметры**:
- `data` (list[dict]): Список словарей, каждый из которых представляет собой пару реплик.
- `output_file` (str): Путь к файлу, в который будут сохранены данные.

**Как работает функция**:
- Открывает файл с именем `output_file` для записи в режиме UTF-8.
- Итерируется по списку `data`, преобразует каждый элемент в JSON-строку с помощью `j_dumps(clean_string(item))` и записывает ее в файл, добавляя символ новой строки (`\n`) в конце каждой записи. Функция `clean_string` используется для очистки строки от лишних символов.

#### `dump_downloaded_conversations`

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

**Назначение**: Собирает реплики из HTML-файлов ChatGPT и сохраняет их в CSV, JSONL и TXT форматы.

**Как работает функция**:
1. Определяет директорию с HTML-файлами разговоров ChatGPT.
2. Получает список всех HTML-файлов в этой директории.
3. Итерируется по списку HTML-файлов:
   - Формирует URI файла.
   - Открывает каждый HTML-файл в браузере с использованием `self.driver.get_url(file_uri)`.
   - Извлекает элементы пользователя и ассистента с использованием локаторов `locator.user` и `locator.assistant`.
   - Извлекает текст из найденных элементов и сохраняет его в списки `user_content` и `assistant_content`.
   - Проверяет, что оба списка не пусты. Если они пусты, логирует ошибку и переходит к следующему файлу.
   - Итерируется по парам текстов пользователя и ассистента, используя `zip_longest`.
   - Создает словарь `data`, содержащий роли (`user`, `assistant`), контент (тексты пользователя и ассистента) и метки настроения (`neutral`).
   - Добавляет данные в список `all_data` в виде DataFrame.
4. Если `all_data` не пуст:
   - Объединяет все DataFrame в один DataFrame `all_data_df`.
   - Сохраняет DataFrame в CSV-файл (`all_conversations.csv`).
   - Сохраняет DataFrame в JSONL-файл (`all_conversations.jsonl`).
   - Извлекает контент из столбца `'content'`, удаляет пропущенные значения, объединяет все тексты в одну строку и сохраняет в TXT-файл (`raw_conversations.txt`).

## Переменные

- `locator`: Словарь с локаторами элементов для поиска на веб-странице, загруженный из файла `chat.json`.
- `traigner`: Экземпляр класса `GPT_Traigner`.
- `model`: Экземпляр класса `Model` из модуля `src.ai.openai.model`.

## Примеры

```python
traigner = GPT_Traigner()
traigner.dump_downloaded_conversations()
model = Model()
model.stream_w(data_file_path=Path(gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.csv'))
```

В данном примере создается экземпляр класса `GPT_Traigner`, вызывается метод `dump_downloaded_conversations` для сбора и сохранения данных разговоров, создается экземпляр класса `Model` и вызывается метод `stream_w` для обучения модели на основе сохраненных данных.