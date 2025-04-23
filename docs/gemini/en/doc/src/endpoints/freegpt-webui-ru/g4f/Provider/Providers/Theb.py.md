# Документация для модуля `Theb.py`

## Обзор

Модуль предоставляет класс для взаимодействия с провайдером Theb.ai, используя модель `gpt-3.5-turbo`. Он поддерживает потоковую передачу данных и не требует аутентификации.

## Более подробно

Модуль использует подпроцесс для выполнения Python скрипта `theb.py`, передавая ему конфигурацию в формате JSON. Это позволяет взаимодействовать с API Theb.ai и получать ответы в потоковом режиме.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает запрос к API Theb.ai и возвращает ответ в потоковом режиме.

    Args:
        model (str): Имя модели для использования.
        messages (list): Список сообщений для отправки в API.
        stream (bool): Флаг, указывающий, использовать ли потоковый режим.
        **kwargs: Дополнительные аргументы.

    Returns:
        Generator[str, None, None]: Генератор строк, представляющих ответ от API Theb.ai.

    Пример:
        >>> _create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}], stream=True)
        <generator object _create_completion at 0x...>
    """
    ...
```

**Описание**: Функция `_create_completion` создает запрос к API Theb.ai, используя указанную модель и сообщения. Она запускает подпроцесс с Python скриптом `theb.py`, передавая ему JSON-конфигурацию.

**Параметры**:
- `model` (str): Имя модели, которую следует использовать.
- `messages` (list): Список сообщений для отправки в API. Каждое сообщение представляет собой словарь с ключами `role` и `content`.
- `stream` (bool): Флаг, указывающий, следует ли использовать потоковый режим. Если `True`, функция будет возвращать ответ по частям, в виде генератора.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в API.

**Возвращает**:
- `Generator[str, None, None]`: Генератор строк, представляющих ответ от API Theb.ai. Каждая строка является частью ответа.

**Как работает функция**:
1. Функция определяет путь к текущему файлу.
2. Формирует JSON-конфигурацию из параметров `messages` и `model`.
3. Создает команду для запуска подпроцесса с Python скриптом `theb.py` и JSON-конфигурацией в качестве аргумента.
4. Запускает подпроцесс и читает вывод построчно.
5. Декодирует каждую строку из байтов в UTF-8 и возвращает её через генератор.

**Пример**:
```python
messages = [{'role': 'user', 'content': 'Hello'}]
model = 'gpt-3.5-turbo'
stream = True
result = _create_completion(model=model, messages=messages, stream=stream)
for part in result:
    print(part)
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '({})'.format(', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]]))
```

**Описание**: Строка `params` формирует строку с информацией о поддержке параметров функцией `_create_completion`.

**Как работает**:
1. Извлекает имя файла текущего модуля без расширения `.py`.
2. Формирует список параметров функции `_create_completion` с их типами.
3. Объединяет параметры в строку и форматирует её для отображения информации о поддержке.

**Пример**:
```python
print(params)