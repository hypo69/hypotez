# Модуль для работы с моделями GPT4Free
## Обзор

Модуль `models.py` предназначен для загрузки, форматирования, чтения и сохранения информации о моделях, используемых в проекте `gpt4free`. Он обеспечивает централизованное управление списком моделей, их путями, требованиями к оперативной памяти, а также шаблонами промптов и системными промптами. Модуль включает функции для получения директории моделей, загрузки списка моделей с удалённого сервера, чтения из файла, сохранения в файл и форматирования данных о моделях.

## Подробнее
Данный модуль предназначен для работы со списком доступных моделей. Он позволяет автоматически загружать этот список с удаленного сервера, сохранять его локально для последующего использования, а также предоставляет функции для доступа к информации о каждой модели. Это упрощает добавление новых моделей и управление ими в проекте `gpt4free`.

## Функции

### `load_models`

**Назначение**: Загружает список моделей с удаленного сервера.

```python
def load_models() -> dict:
    """Загружает список моделей с https://gpt4all.io/models/models3.json

    Returns:
        dict:  Словарь, содержащий информацию о моделях.
    """
```

**Как работает функция**:

1.  Отправляет GET-запрос по URL `https://gpt4all.io/models/models3.json`.
2.  Вызывает функцию `raise_for_status` для проверки статуса ответа (вызывает исключение при ошибке).
3.  Вызывает функцию `format_models` для форматирования полученных данных в словарь.
4.  Возвращает отформатированный словарь моделей.

```
Запрос на сервер --> Получение ответа (JSON) --> Форматирование --> Возврат словаря моделей
```

**Примеры**:

```python
models = load_models()
print(models)
# {'name': {'path': '...', 'ram': '...', 'prompt': '...', 'system': '...'}, ...}
```

### `get_model_name`

**Назначение**: Извлекает имя модели из имени файла.

```python
def get_model_name(filename: str) -> str:
    """Извлекает имя модели из имени файла, удаляя лишние суффиксы.

    Args:
        filename (str): Имя файла модели.

    Returns:
        str: Очищенное имя модели.
    """
```

**Как работает функция**:

1.  Разделяет имя файла на основе первой точки (`.`) и берёт первую часть.
2.  Последовательно удаляет из имени файла подстроки `"-v1_5"`, `"-v1"`, `"-q4_0"`, `"_v01"`, `"-v0"`, `"-f16"`, `"-gguf2"`, `"-newbpe"`.
3.  Возвращает очищенное имя модели.

```
Имя файла --> Разделение по точке --> Удаление подстрок --> Возврат имени модели
```

**Примеры**:

```python
filename = "model-v1_5.bin"
name = get_model_name(filename)
print(name)
# model
```

### `format_models`

**Назначение**: Форматирует список моделей в словарь.

```python
def format_models(models: list) -> dict:
    """Форматирует список моделей в словарь, где ключом является имя модели.

    Args:
        models (list): Список моделей в формате JSON.

    Returns:
        dict: Словарь, где ключом является имя модели, а значением - информация о модели.
    """
```

**Как работает функция**:

1.  Преобразует список моделей в словарь, используя генератор словаря.
2.  В качестве ключа использует имя модели, полученное с помощью функции `get_model_name`.
3.  Значением является словарь с информацией о модели, включающий путь к файлу (`path`), требования к оперативной памяти (`ram`), шаблон промпта (`prompt`) и системный промпт (`system`).
4.  Возвращает созданный словарь.

```
Список моделей --> Извлечение имени модели --> Формирование словаря --> Возврат словаря
```

**Примеры**:

```python
models = [{"filename": "model-v1.bin", "ramrequired": "8 GB", "promptTemplate": "template", "systemPrompt": "system"}]
formatted_models = format_models(models)
print(formatted_models)
# {'model': {'path': 'model-v1.bin', 'ram': '8 GB', 'prompt': 'template', 'system': 'system'}}
```

### `read_models`

**Назначение**: Читает информацию о моделях из файла.

```python
def read_models(file_path: str) -> dict:
    """Читает информацию о моделях из файла.

    Args:
        file_path (str): Путь к файлу.

    Returns:
        dict:  Словарь, содержащий информацию о моделях.
    """
```

**Как работает функция**:

1.  Открывает файл по указанному пути в режиме чтения байтов (`"rb"`).
2.  Загружает JSON-данные из файла с помощью `json.load`.
3.  Возвращает полученный словарь.

```
Открытие файла --> Чтение JSON --> Возврат словаря
```

**Примеры**:

```python
file_path = "models.json"
models = read_models(file_path)
print(models)
# {'model1': {'path': '...', 'ram': '...'}, 'model2': {'path': '...', 'ram': '...'}}
```

### `save_models`

**Назначение**: Сохраняет информацию о моделях в файл.

```python
def save_models(file_path: str, data: dict):
    """Сохраняет информацию о моделях в файл.

    Args:
        file_path (str): Путь к файлу.
        data (dict): Данные для сохранения.
    """
```

**Как работает функция**:

1.  Открывает файл по указанному пути в режиме записи (`'w'`).
2.  Записывает JSON-данные в файл с отступами для удобочитаемости (`indent=4`).

```
Открытие файла --> Запись JSON --> Закрытие файла
```

**Примеры**:

```python
file_path = "models.json"
data = {"model1": {"path": "path1"}, "model2": {"path": "path2"}}
save_models(file_path, data)
```

### `get_model_dir`

**Назначение**: Возвращает путь к директории с моделями.

```python
def get_model_dir() -> str:
    """Возвращает путь к директории с моделями.

    Returns:
        str: Путь к директории с моделями.
    """
```

**Как работает функция**:

1.  Определяет путь к текущей директории, где находится файл (`__file__`).
2.  Определяет путь к корневой директории проекта, поднимаясь на два уровня вверх.
3.  Формирует путь к директории `models`, объединяя путь к проекту и имя директории `"models"`.
4.  Проверяет, существует ли директория `models`, и если нет, создаёт её.
5.  Возвращает путь к директории `models`.

```
Определение директории --> Создание, если отсутствует --> Возврат пути
```

**Примеры**:

```python
model_dir = get_model_dir()
print(model_dir)
# /path/to/project/models
```

### `get_models`

**Назначение**: Получает информацию о моделях. Сначала пытается прочитать из файла, если файл отсутствует, загружает с сервера и сохраняет в файл.

```python
def get_models() -> dict[str, dict]:
    """Получает информацию о моделях.

    Returns:
        dict[str, dict]: Словарь, содержащий информацию о моделях.
    """
```

**Как работает функция**:

1.  Получает путь к директории с моделями с помощью функции `get_model_dir`.
2.  Формирует путь к файлу `models.json` в директории моделей.
3.  Проверяет, существует ли файл по указанному пути.
4.  Если файл существует, читает данные из файла с помощью функции `read_models`.
5.  Если файл не существует, загружает данные с помощью функции `load_models`, сохраняет их в файл с помощью функции `save_models`.
6.  Возвращает полученный словарь с информацией о моделях.

```
Получение пути к файлу --> Проверка наличия файла --> Чтение из файла / Загрузка с сервера --> Сохранение в файл --> Возврат словаря
```

**Примеры**:

```python
models = get_models()
print(models)
# {'model1': {'path': '...', 'ram': '...'}, 'model2': {'path': '...', 'ram': '...'}}