# Модуль GPT_Traigner

## Обзор

Модуль `GPT_Traigner` используется для сбора и обработки диалогов, полученных из ChatGPT.  Он предоставляет возможности для анализа настроения в диалоге, сохранения диалогов в формате JSONL и CSV, а также для дальнейшей обработки данных с помощью модели OpenAI.

## Подробней

Модуль `GPT_Traigner` использует вебдрайвер для извлечения данных из HTML-файлов, содержащих диалоги ChatGPT. Он анализирует текст диалогов, определяет настроение для каждого сообщения (положительное, отрицательное или нейтральное) и сохраняет обработанные данные в виде CSV и JSONL файлов. 

## Классы

### `GPT_Traigner`

**Описание**: Класс `GPT_Traigner` содержит логику для работы с данными ChatGPT. 

**Наследует**: Не наследует.

**Атрибуты**:

 - `driver` (Driver): Экземпляр вебдрайвера для работы с HTML-файлами.

**Методы**:

 - `__init__`: Конструктор класса. Инициализирует драйвер, атрибуты класса и gs (экземпляр класса `GptGs` для взаимодействия с Google Drive).
 - `determine_sentiment`: Определяет настроение сообщения в диалоге.
 - `save_conversations_to_jsonl`: Сохраняет диалоги в файл JSONL.
 - `dump_downloaded_conversations`: Считывает диалоги из HTML-файлов, анализирует их, определяет настроение и сохраняет обработанные данные.

## Методы класса

### `__init__`

```python
    def __init__(self):
        """"""
        ...\n        self.gs = GptGs()
```

**Назначение**: Инициализирует класс `GPT_Traigner`.

**Параметры**: 

 -  None

**Возвращает**: None

**Вызывает исключения**: None

**Как работает**:

 - Инициализирует драйвер для взаимодействия с HTML-файлами.
 - Инициализирует атрибут `gs` для взаимодействия с Google Drive.

### `determine_sentiment`

```python
    def determine_sentiment(self, conversation_pair: dict[str, str], sentiment: str = 'positive') -> str:
        """ Determine sentiment label for a conversation pair """
        ...\n        if sentiment:\n            return "positive"\n        else:\n            return "negative"
```

**Назначение**: Определяет настроение сообщения в диалоге.

**Параметры**:

 - `conversation_pair` (dict[str, str]): Словарь, содержащий текст диалога.
 - `sentiment` (str, optional):  Используется для определения настроения. По умолчанию "positive".

**Возвращает**: 

 - `str`: "positive" или "negative" в зависимости от настроения.

**Вызывает исключения**: None

**Как работает**:

 - Анализирует текст сообщения в диалоге.
 - Возвращает "positive" или "negative" в зависимости от определения настроения.

### `save_conversations_to_jsonl`

```python
    def save_conversations_to_jsonl(self, data: list[dict], output_file: str):
        """ Save conversation pairs to a JSONL file """
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(j_dumps(clean_string(item)) + "\\n")
```

**Назначение**: Сохраняет диалоги в файл JSONL.

**Параметры**:

 - `data` (list[dict]): Список словарей, содержащих диалоги.
 - `output_file` (str): Путь к выходному файлу JSONL.

**Возвращает**: None

**Вызывает исключения**: None

**Как работает**:

 - Сохраняет каждый диалог из списка в файл JSONL в формате JSON.

### `dump_downloaded_conversations`

```python
    def dump_downloaded_conversations(self):
        """ Collect conversations from the chatgpt page """
        ...\n        conversation_directory = Path(gs.path.google_drive / \'chat_gpt\' / \'conversation\')\n        html_files = conversation_directory.glob("*.html")\n\n        all_data = []\n        counter: int = 0  # <- counter\n\n        for local_file_path in html_files:\n            # Get the HTML content\n            file_uri = local_file_path.resolve().as_uri()\n            self.driver.get_url(file_uri)\n            \n            user_elements = self.driver.execute_locator(locator.user)\n            assistant_elements = self.driver.execute_locator(locator.assistant)\n            \n            user_content = [element.text for element in user_elements] if isinstance(user_elements, list) else [user_elements.text] if user_elements  else None\n            assistant_content = [element.text for element in assistant_elements] if isinstance(assistant_elements, list) else [assistant_elements.text] if assistant_elements  else None\n\n            if not user_content and not assistant_content:\n                logger.error(f"Где данные?")\n                continue\n\n            for user_text, assistant_text in zip_longest(user_content, assistant_content):\n                if user_text and assistant_text:\n                    data = {\n                        \'role\': [\'user\', \'assistant\'],\n                        \'content\': [clean_string(user_text), clean_string(assistant_text)],\n                        \'sentiment\': [\'neutral\', \'neutral\']\n                    }\n                    all_data.append(pd.DataFrame(data))\n                    print(f\'{counter} - {local_file_path}\')\n                    counter += 1\n\n        if all_data:\n            all_data_df = pd.concat(all_data, ignore_index=True)\n\n            # Save all accumulated results to a single CSV file\n            csv_file_path = gs.path.google_drive / \'chat_gpt\' / \'conversation\' / \'all_conversations.csv\'\n            all_data_df.to_csv(csv_file_path, index=False, encoding=\'utf-8\')\n\n            # Save all accumulated results to a single JSONL file\n            jsonl_file_path = gs.path.google_drive / \'chat_gpt\' / \'conversation\' / \'all_conversations.jsonl\'\n            all_data_df.to_json(jsonl_file_path, orient=\'records\', lines=True, force_ascii=False)\n            \n            # Save raw conversations to a single line without formatting\n            raw_conversations = \' \'.join(all_data_df[\'content\'].dropna().tolist())\n            raw_file_path = gs.path.google_drive / \'chat_gpt\' / \'conversation\' / \'raw_conversations.txt\'\n            with open(raw_file_path, \'w\', encoding=\'utf-8\') as raw_file:\n                raw_file.write(raw_conversations)
```

**Назначение**: Считывает диалоги из HTML-файлов, анализирует их, определяет настроение и сохраняет обработанные данные.

**Параметры**: None

**Возвращает**: None

**Вызывает исключения**: None

**Как работает**:

 - Получает список HTML-файлов из папки `conversation` на Google Drive.
 - Для каждого файла:
    - Открыть HTML-файл.
    - Извлечь текст сообщений пользователя и ассистента (ChatGPT) с помощью вебдрайвера.
    - Определить настроение для каждого сообщения (по умолчанию "neutral").
    - Сохранить обработанные данные в список `all_data`.
 - Если список `all_data` не пустой, то:
    - Объединить данные из списка в единый DataFrame.
    - Сохранить DataFrame в CSV-файл `all_conversations.csv`.
    - Сохранить DataFrame в JSONL-файл `all_conversations.jsonl`.
    - Сохранить все сообщения из диалогов в текстовый файл `raw_conversations.txt`.

## Параметры класса

 - `driver` (Driver): Экземпляр вебдрайвера для работы с HTML-файлами.
 - `gs` (GptGs): Экземпляр класса `GptGs` для взаимодействия с Google Drive.

## Примеры

```python
# Создание экземпляра класса GPT_Traigner
traigner = GPT_Traigner()

# Обработка диалогов из HTML-файлов
traigner.dump_downloaded_conversations()