# Модуль Equing

## Обзор

Модуль `Equing` реализует провайдер для доступа к модели ИИ `Equing`. 

## Подробоней

`Equing` - это провайдер, предоставляющий доступ к API `Equing`. 
Он реализует интерфейс `AbstractProvider` и предоставляет функции для 
создания завершений (комментариев) модели.
`Equing` поддерживает потоковую передачу данных. 

## Классы

### `class Equing`

**Описание**:  Класс `Equing` реализует провайдер для модели `Equing`, 
предоставляя функции для создания завершений и управления 
параметрами модели.
**Наследует**:  `AbstractProvider`

**Атрибуты**:

- `url (str)`: URL-адрес API `Equing`.
- `working (bool)`: Флаг, указывающий на доступность провайдера.
- `supports_stream (bool)`:  Флаг, указывающий на поддержку потоковой 
передачи.
- `supports_gpt_35_turbo (bool)`: Флаг, указывающий на поддержку модели `gpt-3.5-turbo`.
- `supports_gpt_4 (bool)`: Флаг, указывающий на поддержку модели `gpt-4`.

**Методы**:

- `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`

## Функции

### `create_completion`

**Назначение**:  Функция отправляет запрос к API `Equing` для получения 
завершения (комментария) модели.

**Параметры**:

- `model (str)`: Имя модели (`gpt-3.5-turbo`).
- `messages (list[dict[str, str]])`: Список сообщений в истории 
конверсации.
- `stream (bool)`: Флаг, указывающий на потоковую передачу 
завершений.
- `**kwargs: Any`:  Дополнительные параметры модели, такие как 
`temperature`, `presence_penalty`, `frequency_penalty` и т. д.

**Возвращает**:

- `CreateResult`:  Результат создания завершения, включая 
сообщение и информацию о состоянии.

**Как работает функция**:
- Создает заголовки запроса для API `Equing`.
- Формирует JSON-данные для запроса.
- Отправляет POST-запрос к API `Equing` с использованием 
`requests.post`.
- Обрабатывает ответ:
    - Если `stream=False`:
        - Извлекает результат из ответа `response.json()`.
        - Выводит результат в формате `CreateResult`.
    - Если `stream=True`:
        - Обрабатывает потоковые данные.
        - Извлекает фрагменты текста (`token`) из ответа.
        - Выводит фрагменты текста.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Equing import Equing

# Создаем экземпляр провайдера Equing
provider = Equing()

# Формируем список сообщений
messages = [
    {'role': 'user', 'content': 'Привет!'},
    {'role': 'assistant', 'content': 'Привет! Как дела?'},
]

# Получаем завершение с использованием потоковой передачи
for token in provider.create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')

# Получаем завершение без потоковой передачи
result = provider.create_completion(model='gpt-3.5-turbo', messages=messages, stream=False)
print(result)
```