# Модуль Theb.py

## Обзор

Модуль `Theb.py` предоставляет реализацию провайдера `Theb` для доступа к модели GPT-3.5-turbo через API `theb.ai`. 

## Подробнее

Провайдер Theb реализован как отдельный процесс с использованием библиотеки `subprocess`.  Модуль взаимодействует с внешним скриптом `helpers/theb.py`, который фактически отправляет запросы к API `theb.ai`.

## Классы

### `_create_completion`

**Описание**: Функция, которая отправляет запрос к модели `gpt-3.5-turbo` через API `theb.ai`.

**Параметры**:
- `model` (str): Название модели, например, `gpt-3.5-turbo`.
- `messages` (list): Список сообщений для отправки модели.
- `stream` (bool): Флаг, указывающий на необходимость потоковой передачи ответа модели.

**Возвращает**:
- `Generator[str, None, None]`: Генератор строк, представляющий ответ модели, в том числе промежуточные результаты (если `stream` равен `True`).

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при выполнении скрипта `helpers/theb.py`.

**Как работает функция**:
- Функция формирует JSON-объект с сообщениями и названием модели.
- Выполняет скрипт `helpers/theb.py` с помощью `subprocess.Popen`.
- Читает строки из потока вывода скрипта и возвращает их с помощью генератора.

**Примеры**:

```python
# Пример вызова функции с потоковой передачей ответа
messages = [
    {'role': 'user', 'content': 'Привет!'}
]
response = _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True)
for line in response:
    print(line.strip())

# Пример вызова функции без потоковой передачи ответа
messages = [
    {'role': 'user', 'content': 'Как дела?'}
]
response = _create_completion(model='gpt-3.5-turbo', messages=messages, stream=False)
print(response)