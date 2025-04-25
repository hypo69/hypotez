# Модуль токенизации текста

## Обзор

Этот модуль содержит функции для токенизации текстовых данных. 

##  

## Классы 

### `class Tokenizer`

**Описание**: Класс предоставляет функции для токенизации текста с помощью моделей GPT-3.5-turbo и GPT-4.

**Атрибуты**:

- `model` (str): Название модели GPT, для которой нужно получить токен. По умолчанию `gpt-3.5-turbo`.

**Методы**:

- `tokenize(text: str) -> Union[int, str]`:  Токенизация текста с помощью модели GPT.

**Как работает класс**:

- Класс использует библиотеку `tiktoken` для токенизации текста.
- Метод `tokenize` сначала получает кодировку для заданной модели GPT.
- Затем он кодирует текст с помощью этой кодировки и возвращает количество токенов и кодированный текст.

**Примеры**:
```python
from src.endpoints.gpt4free.g4f.api._tokenizer import Tokenizer

# Создание объекта Tokenizer
tokenizer = Tokenizer(model='gpt-3.5-turbo')

# Токенизация текста
text = 'Привет, мир!'
num_tokens, encoded = tokenizer.tokenize(text)

# Вывод результата
print(f'Количество токенов: {num_tokens}')
print(f'Кодированный текст: {encoded}')
```

## Функции 

### `tokenize(text: str, model: str = 'gpt-3.5-turbo') -> Union[int, str]`

**Назначение**: Токенизация текста с помощью модели GPT.

**Параметры**:

- `text` (str): Текст для токенизации.
- `model` (str): Название модели GPT, для которой нужно получить токен. По умолчанию `gpt-3.5-turbo`.

**Возвращает**:

- `Union[int, str]`:  Количество токенов и кодированный текст.

**Как работает функция**:

- Функция использует библиотеку `tiktoken` для токенизации текста.
- Сначала она получает кодировку для заданной модели GPT.
- Затем она кодирует текст с помощью этой кодировки и возвращает количество токенов и кодированный текст.

**Примеры**:
```python
from src.endpoints.gpt4free.g4f.api._tokenizer import tokenize

# Токенизация текста
text = 'Привет, мир!'
num_tokens, encoded = tokenize(text, model='gpt-4')

# Вывод результата
print(f'Количество токенов: {num_tokens}')
print(f'Кодированный текст: {encoded}')
```

##  
```python
                # import tiktoken
# from typing import Union
# 
# def tokenize(text: str, model: str = 'gpt-3.5-turbo') -> Union[int, str]:
#     encoding   = tiktoken.encoding_for_model(model)
#     encoded    = encoding.encode(text)
#     num_tokens = len(encoded)
#     
#     return num_tokens, encoded