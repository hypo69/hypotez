# Модуль Yqcloud 

## Обзор

Модуль `Yqcloud` предоставляет реализацию провайдера `g4f` для взаимодействия с сервисом Yqcloud. 

## Подробнее

Данный модуль позволяет использовать API сервиса Yqcloud для генерации текста с помощью модели GPT-3.5-turbo. 

## Классы

### `class Yqcloud`

**Описание**: Класс `Yqcloud` реализует провайдера `g4f` для сервиса Yqcloud. 

**Атрибуты**:

- `url` (str): Базовый URL для взаимодействия с сервисом Yqcloud.
- `model` (list): Список поддерживаемых моделей. 

**Методы**:

- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`:  Функция создает запрос для генерации текста.

## Функции

### `_create_completion`

**Назначение**: Функция формирует запрос к API Yqcloud для генерации текста.

**Параметры**:

- `model` (str): Имя модели, используемой для генерации.
- `messages` (list): Список сообщений в чате.
- `stream` (bool): Флаг, указывающий на необходимость потоковой передачи ответов.
- `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:

- Генератор, который выдает токены ответа.

**Как работает функция**:

- Функция формирует JSON-запрос к API Yqcloud, используя информацию из переданных параметров.
- Выполняется POST-запрос к API-адресу, указанному в `url`.
- Ответ от сервера декодируется в формат UTF-8 и передается в виде токенов через генератор.

**Примеры**:

```python
# Пример вызова функции для генерации текста:
model = 'gpt-3.5-turbo'
messages = [
    {'role': 'user', 'content': 'Привет! Расскажи мне что-нибудь интересное.'}
]
stream = True
completion = _create_completion(model, messages, stream)
for token in completion:
    print(token, end='')
```

## Параметры класса

- `url` (str): URL-адрес для взаимодействия с API Yqcloud.
- `model` (list): Список поддерживаемых моделей.

**Примеры**:

```python
# Пример создания экземпляра класса Yqcloud:
yqcloud_provider = Yqcloud()

# Доступ к параметрам:
print(yqcloud_provider.url)
print(yqcloud_provider.model)