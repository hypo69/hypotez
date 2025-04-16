# Модуль для проверки валидности ответов от модели

## Обзор

Модуль предназначен для отправки запросов к AI-модели (Google Gemini) на русском и иврите, получения ответов, проверки их валидности и сохранения результатов в формате JSON. Используется для обработки данных о товарах и проверки соответствия ответов модели ожидаемому формату.

## Подробней

Модуль выполняет следующие шаги:

1.  Загружает необходимые инструкции для модели на русском и иврите.
2.  Формирует запросы к модели, объединяя инструкции и список товаров.
3.  Отправляет запросы к модели, используя класс `GoogleGenerativeAi`.
4.  Проверяет полученные ответы на валидность и соответствие формату JSON.
5.  Сохраняет валидные ответы в файлы JSON.

## Функции

### `model_ask`

```python
def model_ask(lang:str, attempts = 3) -> dict:
    """"""
    global model, q_ru, q_he

    response = model.ask(q_ru if lang == 'ru' else q_he)
    if not response:
        logger.error(f"Нет ответа от модели")
        ...
        return {}

    response_dict:dict = j_loads(response)
    if not response_dict:
        logger.error("Ошибка парсинга ")
        if attempts >1:
            model_ask(lang, attempts -1 )
        return {}

    return response_dict
```

**Назначение**: Отправляет запрос к AI-модели на указанном языке, проверяет ответ и возвращает его в виде словаря. В случае неудачи предпринимает несколько попыток.

**Параметры**:

*   `lang` (str): Язык запроса (`'ru'` или `'he'`).
*   `attempts` (int, optional): Количество попыток отправки запроса. По умолчанию `3`.

**Возвращает**:

*   `dict`: Словарь с ответом от модели в формате JSON. В случае ошибки возвращает пустой словарь `{}`.

**Как работает функция**:

1.  Определяет глобальные переменные `model`, `q_ru` и `q_he`, которые используются для доступа к экземпляру модели и текстам запросов на разных языках.
2.  Отправляет запрос к модели, используя метод `ask` класса `GoogleGenerativeAi`. Запрос формируется в зависимости от языка, указанного в параметре `lang`.
3.  Проверяет, получен ли ответ от модели. Если ответ отсутствует, логируется ошибка и возвращается пустой словарь.
4.  Пытается преобразовать полученный ответ из формата JSON в словарь Python с использованием функции `j_loads`.
5.  Проверяет, удалось ли преобразование. Если преобразование не удалось, логируется ошибка и, если количество попыток не исчерпано, функция рекурсивно вызывает саму себя с уменьшенным количеством попыток.
6.  Если ответ успешно получен и преобразован, функция возвращает полученный словарь.

**Примеры**:

```python
# Пример вызова функции для запроса на русском языке
response_ru = model_ask(lang='ru')

# Пример вызова функции для запроса на иврите с одной попыткой
response_he = model_ask(lang='he', attempts=1)
```

## Переменные модуля

### `test_directory`

```python
test_directory:Path = gs.path.external_storage / 'kazarinov' / 'mexironim' / '24_12_07_19_06_40_508'
```

**Описание**: Путь к директории с тестовыми данными. Определяется на основе структуры каталогов, специфичной для проекта.

### `products_in_test_dir`

```python
products_in_test_dir:Path = test_directory /  'products'
```

**Описание**: Путь к файлу, содержащему список товаров в директории с тестовыми данными.

### `products_list`

```python
products_list:list[dict] = j_loads(products_in_test_dir)
```

**Описание**: Список товаров, загруженных из файла JSON, расположенного по пути `products_in_test_dir`.

### `system_instruction`

```python
system_instruction = Path(gs.path.endpoints / 'kazarinov' / 'instructions' / 'system_instruction_mexiron.md').read_text(encoding='UTF-8')
```

**Описание**: Системная инструкция для модели, загруженная из файла `system_instruction_mexiron.md`.

### `command_instruction_ru`

```python
command_instruction_ru = Path(gs.path.endpoints / 'kazarinov' / 'instructions' / 'command_instruction_mexiron_ru.md').read_text(encoding='UTF-8')
```

**Описание**: Инструкция для модели на русском языке, загруженная из файла `command_instruction_mexiron_ru.md`.

### `command_instruction_he`

```python
command_instruction_he = Path(gs.path.endpoints / 'kazarinov' / 'instructions' / 'command_instruction_mexiron_he.md').read_text(encoding='UTF-8')
```

**Описание**: Инструкция для модели на иврите, загруженная из файла `command_instruction_mexiron_he.md`.

### `api_key`

```python
api_key = gs.credentials.gemini.kazarinov
```

**Описание**: Ключ API для доступа к модели Gemini.

### `model`

```python
model = GoogleGenerativeAi(
                api_key=api_key,
                system_instruction=system_instruction,
                generation_config={'response_mime_type': 'application/json'}
            )
```

**Описание**: Экземпляр класса `GoogleGenerativeAi`, используемый для взаимодействия с моделью Gemini.

### `q_ru`

```python
q_ru = command_instruction_ru + str(products_list)
```

**Описание**: Текст запроса на русском языке, сформированный путем объединения инструкции и списка товаров.

### `q_he`

```python
q_he = command_instruction_he + str(products_list)
```

**Описание**: Текст запроса на иврите, сформированный путем объединения инструкции и списка товаров.

### `response_ru_dict`

```python
response_ru_dict = model_ask('ru')
```

**Описание**: Ответ от модели на русском языке в виде словаря, полученный с помощью функции `model_ask`.

### `response_he_dict`

```python
response_he_dict = model_ask('he')
```

**Описание**: Ответ от модели на иврите в виде словаря, полученный с помощью функции `model_ask`.

## Действия после определения функции `model_ask`

После определения функции `model_ask` выполняются следующие действия:

1.  Вызывается функция `model_ask` с параметром `'ru'` для получения ответа от модели на русском языке. Результат сохраняется в переменной `response_ru_dict`.
2.  Полученный словарь `response_ru_dict` сохраняется в файл JSON с именем `ru_{gs.now}.json` в директории `gs.path.external_storage / 'kazarinov' / 'mexironim' / '24_12_07_19_06_40_508'`.
3.  Вызывается функция `model_ask` с параметром `'he'` для получения ответа от модели на иврите. Результат сохраняется в переменной `response_he_dict`.
4.  Полученный словарь `response_he_dict` сохраняется в файл JSON с именем `he_{gs.now}.json` в той же директории.

```python
response_ru_dict = model_ask('ru')
j_dumps(response_ru_dict,gs.path.external_storage / 'kazarinov' / 'mexironim' / '24_12_07_19_06_40_508' / f'ru_{gs.now}.json')
response_he_dict = model_ask('he')
j_dumps(response_he_dict, gs.path.external_storage / 'kazarinov' / 'mexironim' / '24_12_07_19_06_40_508' / f'he_{gs.now}.json')