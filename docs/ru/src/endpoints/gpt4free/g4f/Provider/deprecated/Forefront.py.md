# Модуль для взаимодействия с Forefront API

## Обзор

Модуль предоставляет класс `Forefront` для взаимодействия с API Forefront. Forefront позволяет использовать модель `gpt-4` для генерации текста.
Модуль поддерживает потоковую передачу данных, а также работу с моделью `gpt-35-turbo`.

## Подробней

Модуль `Forefront` является провайдером для `g4f`, который позволяет использовать API Forefront для генерации текста. Класс наследуется от `AbstractProvider` и переопределяет метод `create_completion` для выполнения запросов к API Forefront.

## Классы

### `Forefront`

**Описание**: Класс для взаимодействия с API Forefront.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `url` (str): URL для доступа к Forefront.
- `supports_stream` (bool): Поддержка потоковой передачи данных.
- `supports_gpt_35_turbo` (bool): Поддержка модели `gpt-35-turbo`.

**Методы**:
- `create_completion`: Создает завершение текста на основе предоставленных сообщений.

## Функции

### `create_completion`

```python
def create_completion(
    model: str,
    messages: list[dict[str, str]],
    stream: bool, **kwargs: Any) -> CreateResult:
    """ Функция создает запрос к API Forefront для генерации текста на основе предоставленных сообщений.

    Args:
        model (str): Имя модели для использования.
        messages (list[dict[str, str]]): Список сообщений для передачи в API.
        stream (bool): Флаг, указывающий, следует ли использовать потоковую передачу данных.
        **kwargs (Any): Дополнительные параметры.

    Returns:
        CreateResult: Результат создания завершения текста.

    Raises:
        requests.exceptions.HTTPError: Если возникает ошибка при выполнении HTTP-запроса.

    Example:
        >>> Forefront.create_completion(model="gpt-4", messages=[{"role": "user", "content": "Hello"}], stream=True)
        <generator object Forefront.create_completion at 0x...>
    """
```

**Назначение**: Создает запрос к API Forefront для генерации текста на основе предоставленных сообщений.

**Параметры**:
- `model` (str): Имя модели для использования.
- `messages` (list[dict[str, str]]): Список сообщений для передачи в API.
- `stream` (bool): Флаг, указывающий, следует ли использовать потоковую передачу данных.
- `**kwargs` (Any): Дополнительные параметры.

**Возвращает**:
- `CreateResult`: Результат создания завершения текста.

**Вызывает исключения**:
- `requests.exceptions.HTTPError`: Если возникает ошибка при выполнении HTTP-запроса.

**Как работает функция**:

1. **Формирование JSON-данных**: Функция формирует JSON-данные для отправки в API Forefront.
   - Извлекается последнее сообщение из списка `messages` и используется как основной текст (`text`).
   - Устанавливаются параметры `action`, `id`, `parentId`, `workspaceId`, `messagePersona` и `model`.
   - Если в списке `messages` больше одного сообщения, предыдущие сообщения используются в поле `messages`.
   - Устанавливается режим `internetMode` в значение "auto".

2. **Выполнение POST-запроса**: Функция выполняет POST-запрос к API Forefront с использованием библиотеки `requests`.
   - URL для запроса: `"https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat"`.
   - Параметр `stream` устанавливается в `True` для потоковой передачи данных.

3. **Обработка потока ответов**: Функция итерируется по строкам в потоке ответов от API.
   - Для каждой строки проверяется наличие подстроки `b"delta"`.
   - Если подстрока найдена, строка декодируется, извлекается JSON-объект, и извлекается значение из поля `"delta"`.
   - Значение `"delta"` возвращается как результат итерации.

```
Формирование JSON-данных
↓
Выполнение POST-запроса (stream=True)
↓
Обработка потока ответов
│
└─→ Проверка наличия "delta" в строке
  │
  └─→ Извлечение значения "delta" из JSON
    │
    └─→ yield "delta"
```

**Примеры**:

```python
# Пример вызова функции с потоковой передачей данных
result = Forefront.create_completion(model="gpt-4", messages=[{"role": "user", "content": "Напиши небольшое стихотворение про осень."}], stream=True)
for token in result:
    print(token, end="")
```

```python
# Пример вызова функции без потоковой передачи данных
result = Forefront.create_completion(model="gpt-4", messages=[{"role": "user", "content": "Как дела?"}], stream=False)
print(result)