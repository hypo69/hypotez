# Модуль для взаимодействия с API You.com

## Обзор

Модуль `you.py` предоставляет функциональность для взаимодействия с API You.com, который реализует чат-бот с поддержкой искусственного интеллекта.  Он позволяет отправить запрос к API с историей сообщений чата, а также получить токен доступа к API You.com.

## Подробности

В модуле `you.py` реализована логика отправки запросов к API You.com. Основные шаги включают:

1. **Подготовка данных:** 
   - Преобразование истории сообщений чата в формат, удобный для API You.com.
   - Подготовка запроса с использованием URL-кодирования.

2. **Отправка запроса:** 
   - Использование библиотеки `requests` для отправки запроса к API You.com.
   - Установка заголовков запроса с соответствующими данными.

3. **Обработка ответа:**
   - Получение токена доступа из ответа API.

## Функции

### `transform`

**Назначение**: Преобразует список сообщений чата в формат, подходящий для API You.com.

**Параметры**:
- `messages` (list): Список сообщений чата.

**Возвращает**:
- `list`: Список сообщений в формате, подходящем для API You.com.

**Как работает функция**:
- Функция перебирает список сообщений чата.
- Для каждого сообщения определяется его роль (`user`, `assistant`, `system`).
- Формируется словарь с ключами `question` и `answer` для каждого сообщения.
- Возвращается список сформированных словарей.

**Примеры**:
```python
messages = [
    {'role': 'user', 'content': 'Привет!'},
    {'role': 'assistant', 'content': 'Привет!'},
    {'role': 'user', 'content': 'Как дела?'},
    {'role': 'assistant', 'content': 'Хорошо, а у тебя?'},
]

transformed_messages = transform(messages)

print(transformed_messages)
```

### `output`

**Назначение**: Обрабатывает ответ от API You.com и выводит токен доступа.

**Параметры**:
- `chunk` (bytes): Фрагмент ответа от API.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция проверяет, содержит ли фрагмент ответа текст `'youChatToken'`.
- Если да, то из фрагмента извлекается JSON-объект с токеном доступа.
- Токен доступа выводится в консоль.

**Примеры**:
```python
chunk = b'data: {"youChatToken": "your_token"}'

output(chunk)
```

## Основной код

Основной код модуля `you.py` включает в себя:

- Загрузка конфигурации из аргумента командной строки.
- Получение последнего сообщения пользователя.
- Подготовка запроса с историей сообщений чата.
- Отправка запроса к API You.com.
- Получение токена доступа к API You.com.

```python
# Загрузка конфигурации
config = json.loads(sys.argv[1])
messages = config['messages']
prompt = ''

# Преобразование истории сообщений
transformed_messages = transform(messages)

# Получение последнего сообщения пользователя
if messages[-1]['role'] == 'user':
    prompt = messages[-1]['content']
    messages = messages[:-1]

# Подготовка запроса
params = urllib.parse.urlencode({
    'q': prompt,
    'domain': 'youchat',
    'chat': transformed_messages
})

# Отправка запроса к API You.com
while True:
    try:
        response = requests.get(f'https://you.com/api/streamingSearch?{params}',
                                headers=headers, content_callback=output, impersonate='safari15_5')
        exit(0)
    except Exception as ex:
        print('an error occured, retrying... |', ex, flush=True)
        continue