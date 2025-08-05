# Модуль Phind

## Обзор

Этот модуль предоставляет реализацию провайдера `Phind` для `freegpt-webui-ru`, позволяя использовать модель `Phind` в качестве источника ответов. Модуль использует вспомогательную программу `phind.py` для взаимодействия с API `Phind`. 

## Подробнее

Модуль реализует класс `Phind`, который наследует от `Provider`, и предоставляет метод `_create_completion` для генерации ответов. В  `_create_completion` используется `subprocess` для запуска скрипта `phind.py`, передавая ему конфигурационные данные в виде JSON-строки. 

## Классы

### `Phind`

**Описание**: Класс `Phind` реализует провайдера для модели `Phind`.

**Наследует**: `Provider`

**Атрибуты**:
- `url`: URL-адрес `Phind` API. 
- `model`: Список доступных моделей. В данном случае `model = ['gpt-4']`
- `supports_stream`: Флаг, указывающий на поддержку потоковой передачи ответов.

**Методы**:
- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`: Метод для создания ответа модели `Phind`. 

## Функции

### `_create_completion`

**Назначение**: Функция `_create_completion` создает ответ модели `Phind` на основе переданных сообщений. 

**Параметры**:
- `model` (str): Имя модели.
- `messages` (list): Список сообщений для модели.
- `stream` (bool): Флаг, указывающий на потоковую передачу.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- Generator[str, None, None]: Генератор, который выдает части ответа по мере их получения.

**Как работает функция**:

- Функция `_create_completion` получает путь к текущему файлу с помощью `os.path.realpath(__file__)`.
- Затем она создает конфигурационную строку в формате JSON, которая содержит имя модели и список сообщений. 
- Используя `subprocess`, функция запускает скрипт `phind.py` с конфигурационной строкой в качестве аргумента.
- Используя `p.stdout.readline`, функция считывает вывод из процесса `phind.py` построчно.
- Если в строке присутствует текст `<title>Just a moment...</title>`, функция выводит сообщение о Cloudflare ошибке и завершает работу.
- В противном случае, функция выводит строку в консоль после удаления строки "ping - 2023-", если она присутствует. 
- Функция использует кодировку `cp1251` для декодирования строки.
- `os._exit(0)` - завершает скрипт.

**Примеры**:

```python
# Пример вызова функции _create_completion
messages = [
    {"role": "user", "content": "Привет, как дела?"},
]
response = _create_completion(model="gpt-4", messages=messages, stream=False)
for line in response:
    print(line)
```
```python
# Пример вызова функции _create_completion
messages = [
    {"role": "user", "content": "Расскажи мне анекдот."},
]
response = _create_completion(model="gpt-4", messages=messages, stream=True)
for line in response:
    print(line)
```

## Внутренние функции

## Параметры

- `url`: URL-адрес `Phind` API.
- `model`: Список доступных моделей.
- `supports_stream`: Флаг, указывающий на поддержку потоковой передачи ответов.

**Примеры**:

```python
#  Создание экземпляра модели `Phind`
from g4f.Provider.Providers.Phind import Phind

provider = Phind()