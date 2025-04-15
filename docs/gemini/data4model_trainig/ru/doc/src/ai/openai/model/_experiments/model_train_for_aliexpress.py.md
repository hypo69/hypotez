# Модуль для обучения моделей OpenAI и Gemini на данных AliExpress

## Обзор

Модуль предназначен для обучения моделей OpenAI и Google Gemini на основе данных, полученных с AliExpress. Он включает в себя функциональность для рекурсивного поиска файлов с названиями продуктов, чтения текстовых файлов, преобразования CSV в JSON и словари, а также взаимодействия с моделями OpenAI и Gemini.

## Подробней

Этот модуль используется для автоматизации процесса обучения моделей искусственного интеллекта, используемых для анализа и обработки данных с платформы AliExpress. Он позволяет загружать данные о названиях продуктов, передавать их в модели OpenAI и Gemini для обработки и получения ответов. В результате, обученные модели могут быть использованы для различных задач, таких как генерация контента, анализ тональности и классификация продуктов.

## Функции

### `recursively_get_filenames`

```python
recursively_get_filenames(path: str, file_extension: str) -> list:
    """
    Функция рекурсивно получает список имен файлов с указанным расширением из заданной директории.

    Args:
        path (str): Путь к директории.
        file_extension (str): Расширение файлов для поиска.

    Returns:
        list: Список имен файлов с указанным расширением.
    """
    ...
```

**Назначение**: Рекурсивно получает список имен файлов с указанным расширением из заданной директории.

**Параметры**:
- `path` (str): Путь к директории.
- `file_extension` (str): Расширение файлов для поиска.

**Возвращает**:
- `list`: Список имен файлов с указанным расширением.

**Как работает функция**:
- Функция принимает путь к директории и расширение файла в качестве аргументов.
- Она рекурсивно проходит по всем поддиректориям в указанной директории.
- Для каждого файла проверяет, соответствует ли его расширение заданному.
- Если расширение соответствует, добавляет имя файла в список результатов.
- Возвращает список имен файлов.

**Примеры**:

```python
from pathlib import Path
# Предположим, что в директории 'mydir' есть файлы 'file1.txt', 'file2.txt' и 'file3.csv'
path = Path('mydir')
file_extension = 'txt'
result = recursively_get_filenames(path, file_extension)
print(result)  # Вывод: ['file1.txt', 'file2.txt']
```

### `read_text_file`

```python
read_text_file(file_path: str) -> str:
    """
    Функция считывает содержимое текстового файла и возвращает его в виде строки.

    Args:
        file_path (str): Путь к текстовому файлу.

    Returns:
        str: Содержимое текстового файла в виде строки.
    """
    ...
```

**Назначение**: Считывает содержимое текстового файла и возвращает его в виде строки.

**Параметры**:
- `file_path` (str): Путь к текстовому файлу.

**Возвращает**:
- `str`: Содержимое текстового файла в виде строки.

**Как работает функция**:
- Функция принимает путь к файлу в качестве аргумента.
- Открывает файл в режиме чтения ('r') с кодировкой 'utf-8'.
- Читает все содержимое файла и возвращает его в виде строки.

**Примеры**:

```python
from pathlib import Path
# Предположим, что файл 'myfile.txt' содержит текст "Hello, world!"
file_path = Path('myfile.txt')
content = read_text_file(file_path)
print(content)  # Вывод: Hello, world!
```

### `csv2json_csv2dict`

```python
csv2json_csv2dict(file_path: str) -> list[dict]:
    """
    Функция преобразует CSV файл в список словарей.

    Args:
        file_path (str): Путь к CSV файлу.

    Returns:
        list[dict]: Список словарей, представляющих строки CSV файла.
    """
    ...
```

**Назначение**: Преобразует CSV файл в список словарей.

**Параметры**:
- `file_path` (str): Путь к CSV файлу.

**Возвращает**:
- `list[dict]`: Список словарей, представляющих строки CSV файла.

**Как работает функция**:
- Функция принимает путь к CSV файлу в качестве аргумента.
- Открывает CSV файл.
- Читает CSV файл, используя модуль CSV.
- Преобразует каждую строку CSV файла в словарь, используя первую строку CSV файла в качестве ключей.
- Возвращает список словарей, представляющих строки CSV файла.

**Примеры**:

```python
from pathlib import Path
# Предположим, что файл 'myfile.csv' содержит следующие данные:
# name,age
# John,30
# Jane,25
file_path = Path('myfile.csv')
data = csv2json_csv2dict(file_path)
print(data)
# Вывод: [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
```

### `OpenAIModel`

```python
class OpenAIModel:
    """
    Класс для взаимодействия с моделью OpenAI.

    Attributes:
        system_instruction (str): Инструкция для системы OpenAI.

    Methods:
        ask(prompt: str) -> str: Отправляет запрос в модель OpenAI и возвращает ответ.
    """

    def __init__(self, system_instruction: str):
        """
        Инициализирует экземпляр класса OpenAIModel.

        Args:
            system_instruction (str): Инструкция для системы OpenAI.
        """
        ...

    def ask(self, prompt: str) -> str:
        """
        Отправляет запрос в модель OpenAI и возвращает ответ.

        Args:
            prompt (str): Запрос для отправки в модель OpenAI.

        Returns:
            str: Ответ от модели OpenAI.
        """
        ...
```

**Описание**: Класс для взаимодействия с моделью OpenAI.

**Атрибуты**:
- `system_instruction` (str): Инструкция для системы OpenAI.

**Методы**:
- `ask(prompt: str) -> str`: Отправляет запрос в модель OpenAI и возвращает ответ.

**Принцип работы**:
- Класс инициализируется с системной инструкцией для модели OpenAI.
- Метод `ask` принимает запрос и отправляет его в модель OpenAI.
- Возвращает ответ от модели OpenAI.

**Примеры**:

```python
# Инициализация класса OpenAIModel с системной инструкцией
system_instruction = "You are a helpful assistant."
openai = OpenAIModel(system_instruction=system_instruction)

# Отправка запроса в модель OpenAI и получение ответа
prompt = "What is the capital of France?"
response = openai.ask(prompt)
print(response)  # Вывод: The capital of France is Paris.
```

### `GoogleGenerativeAI`

```python
class GoogleGenerativeAI:
    """
    Класс для взаимодействия с моделью Google Generative AI.

    Attributes:
        system_instruction (str): Инструкция для системы Google Generative AI.

    Methods:
        ask(prompt: str) -> str: Отправляет запрос в модель Google Generative AI и возвращает ответ.
    """

    def __init__(self, system_instruction: str):
        """
        Инициализирует экземпляр класса GoogleGenerativeAI.

        Args:
            system_instruction (str): Инструкция для системы Google Generative AI.
        """
        ...

    def ask(self, prompt: str) -> str:
        """
        Отправляет запрос в модель Google Generative AI и возвращает ответ.

        Args:
            prompt (str): Запрос для отправки в модель Google Generative AI.

        Returns:
            str: Ответ от модели Google Generative AI.
        """
        ...
```

**Описание**: Класс для взаимодействия с моделью Google Generative AI.

**Атрибуты**:
- `system_instruction` (str): Инструкция для системы Google Generative AI.

**Методы**:
- `ask(prompt: str) -> str`: Отправляет запрос в модель Google Generative AI и возвращает ответ.

**Принцип работы**:
- Класс инициализируется с системной инструкцией для модели Google Generative AI.
- Метод `ask` принимает запрос и отправляет его в модель Google Generative AI.
- Возвращает ответ от модели Google Generative AI.

**Примеры**:

```python
# Инициализация класса GoogleGenerativeAI с системной инструкцией
system_instruction = "You are a helpful assistant."
gemini = GoogleGenerativeAI(system_instruction=system_instruction)

# Отправка запроса в модель Google Generative AI и получение ответа
prompt = "What is the capital of France?"
response = gemini.ask(prompt)
print(response)  # Вывод: The capital of France is Paris.
```

## Переменные

- `product_titles_files` (list): Список файлов с названиями продуктов, полученный рекурсивно из директории `gs.path.google_drive / 'aliexpress' / 'campaigns'` с расширением `product_titles.txt`.
- `system_instruction_path` (str): Путь к файлу с системной инструкцией для моделей AI, расположенному в `gs.path.src / 'ai' / 'prompts' / 'aliexpress_campaign' / 'system_instruction.txt'`.
- `system_instruction` (str): Содержимое файла с системной инструкцией, считанное с использованием функции `read_text_file`.
- `openai` (OpenAIModel): Экземпляр класса `OpenAIModel`, инициализированный с системной инструкцией.
- `gemini` (GoogleGenerativeAI): Экземпляр класса `GoogleGenerativeAI`, инициализированный с системной инструкцией.
- `file` (str): Переменная цикла, представляющая текущий файл с названиями продуктов.
- `product_titles` (str): Содержимое файла с названиями продуктов, считанное с использованием функции `read_text_file`.
- `response_openai` (str): Ответ от модели OpenAI на запрос с названиями продуктов.
- `response_gemini` (str): Ответ от модели Gemini на запрос с названиями продуктов.