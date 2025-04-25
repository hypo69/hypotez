# Модуль `typing`

## Обзор

Модуль `typing` предоставляет типы для типизации различных сущностей в контексте GPT4Free.  

## Подробнее

Этот модуль содержит набор типов, используемых для определения типов данных и параметров различных функций и классов в проекте GPT4Free. Типизация позволяет повысить  безопасность кода, а также  улучшить его читаемость. 

## Типы

### `SHA256`

**Описание**: Тип данных, представляющий хэш SHA-256.

**Пример**:

```python
sha256_hash: SHA256 = 'e5b8c4050994820426398090c2d46f40301c870c6b149c0071d4279f46f1f65f'
```


### `CreateResult`

**Описание**:  Тип, который представляет собой итератор, возвращающий либо строку, либо объект типа `ResponseType`. 

**Пример**:

```python
result: CreateResult = create_response()
for item in result:
    if isinstance(item, str):
        print(item)
    elif isinstance(item, ResponseType):
        print(item.text)
```

### `AsyncResult`

**Описание**: Тип, представляющий асинхронный итератор, возвращающий либо строку, либо объект типа `ResponseType`. 

**Пример**:

```python
async def async_create_response():
    ...
    yield "some text"
    yield ResponseType(text="some text", status_code=200)

result: AsyncResult = async_create_response()
async for item in result:
    if isinstance(item, str):
        print(item)
    elif isinstance(item, ResponseType):
        print(item.text)
```

### `Messages`

**Описание**:  Тип, который представляет собой список словарей, где каждый словарь содержит информацию о сообщениях.  

**Пример**:

```python
messages: Messages = [
    {'role': 'user', 'content': 'Hello, world!'},
    {'role': 'assistant', 'content': 'Hello! How can I help you?'}
]
```

### `Cookies`

**Описание**:  Тип, который представляет собой словарь с информацией о куки. 

**Пример**:

```python
cookies: Cookies = {
    'session': 'some_session_id',
    'user_id': 'some_user_id',
}
```

### `ImageType`

**Описание**:  Тип, который представляет собой изображение. 

**Пример**:

```python
image: ImageType = 'path/to/image.jpg'
```

### `MediaListType`

**Описание**: Тип, представляющий собой список пар, где каждая пара состоит из изображения и его описания (опционально). 

**Пример**:

```python
media_list: MediaListType = [
    ('path/to/image.jpg', 'Description of image 1'),
    ('path/to/image2.png', 'Description of image 2')
]
```