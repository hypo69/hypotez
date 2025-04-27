# Модуль Payload для OpenAI-трейнера
## Обзор
Модуль `payload.py` предоставляет функции и классы для работы с OpenAI-трейнером в проекте `hypotez`. 

## Детали
Этот модуль отвечает за подготовку входных данных (payload) для обучения OpenAI-моделей. 

## Классы
### `class Payload`
**Описание**: Класс `Payload` используется для создания payload'а для OpenAI-модели. 

**Атрибуты**:
- `model`: str - Имя модели (например, "text-davinci-003").
- `prompt`: str - Текстовый запрос для модели.
- `temperature`: float - Параметр, определяющий креативность модели (0-1).
- `max_tokens`: int - Максимальное количество токенов в ответе.
- `top_p`: float - Параметр, определяющий выбор вариантов ответа (0-1).
- `frequency_penalty`: float - Штраф за частоту использования слов.
- `presence_penalty`: float - Штраф за присутствие слов.
- `stop`: List[str] - Список токенов, на которых необходимо прекратить генерацию.

**Методы**:
- `to_dict()`: Метод возвращает payload в виде словаря.


## Функции
### `function prepare_payload(prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 1024, top_p: float = 1, frequency_penalty: float = 0, presence_penalty: float = 0, stop: Optional[List[str]] = None) -> dict`
**Цель**: Подготовка payload'а для OpenAI-модели.

**Параметры**:
- `prompt` (str): Текстовый запрос для модели.
- `model` (str): Имя модели (например, "text-davinci-003").
- `temperature` (float): Параметр, определяющий креативность модели (0-1). По умолчанию 0.7.
- `max_tokens` (int): Максимальное количество токенов в ответе. По умолчанию 1024.
- `top_p` (float): Параметр, определяющий выбор вариантов ответа (0-1). По умолчанию 1.
- `frequency_penalty` (float): Штраф за частоту использования слов. По умолчанию 0.
- `presence_penalty` (float): Штраф за присутствие слов. По умолчанию 0.
- `stop` (Optional[List[str]]): Список токенов, на которых необходимо прекратить генерацию. По умолчанию None.

**Возвращает**:
- `dict`: Payload в виде словаря.

**Пример**:
```python
payload = prepare_payload(
    prompt="Напишите текст о кошке",
    model="text-davinci-003",
    temperature=0.5,
    max_tokens=50,
)
print(payload)
```
**Пример вывода**:
```json
{
  "model": "text-davinci-003",
  "prompt": "Напишите текст о кошке",
  "temperature": 0.5,
  "max_tokens": 50,
  "top_p": 1,
  "frequency_penalty": 0,
  "presence_penalty": 0
}
```

### `function prepare_payload_from_file(file_path: str, model: str, temperature: float = 0.7, max_tokens: int = 1024, top_p: float = 1, frequency_penalty: float = 0, presence_penalty: float = 0, stop: Optional[List[str]] = None) -> dict`
**Цель**:  Подготовка payload'а для OpenAI-модели из файла.

**Параметры**:
- `file_path` (str): Путь к файлу с текстом запроса.
- `model` (str): Имя модели (например, "text-davinci-003").
- `temperature` (float): Параметр, определяющий креативность модели (0-1). По умолчанию 0.7.
- `max_tokens` (int): Максимальное количество токенов в ответе. По умолчанию 1024.
- `top_p` (float): Параметр, определяющий выбор вариантов ответа (0-1). По умолчанию 1.
- `frequency_penalty` (float): Штраф за частоту использования слов. По умолчанию 0.
- `presence_penalty` (float): Штраф за присутствие слов. По умолчанию 0.
- `stop` (Optional[List[str]]): Список токенов, на которых необходимо прекратить генерацию. По умолчанию None.

**Возвращает**:
- `dict`: Payload в виде словаря.

**Пример**:
```python
payload = prepare_payload_from_file(
    file_path="prompt.txt",
    model="text-davinci-003",
    temperature=0.5,
    max_tokens=50,
)
print(payload)
```
**Пример вывода**:
```json
{
  "model": "text-davinci-003",
  "prompt": "Текст из файла prompt.txt",
  "temperature": 0.5,
  "max_tokens": 50,
  "top_p": 1,
  "frequency_penalty": 0,
  "presence_penalty": 0
}
```
### `function prepare_payload_from_list(prompts: List[str], model: str, temperature: float = 0.7, max_tokens: int = 1024, top_p: float = 1, frequency_penalty: float = 0, presence_penalty: float = 0, stop: Optional[List[str]] = None) -> List[dict]`
**Цель**: Подготовка списка payload'ов для OpenAI-модели из списка запросов.

**Параметры**:
- `prompts` (List[str]): Список текстовых запросов для модели.
- `model` (str): Имя модели (например, "text-davinci-003").
- `temperature` (float): Параметр, определяющий креативность модели (0-1). По умолчанию 0.7.
- `max_tokens` (int): Максимальное количество токенов в ответе. По умолчанию 1024.
- `top_p` (float): Параметр, определяющий выбор вариантов ответа (0-1). По умолчанию 1.
- `frequency_penalty` (float): Штраф за частоту использования слов. По умолчанию 0.
- `presence_penalty` (float): Штраф за присутствие слов. По умолчанию 0.
- `stop` (Optional[List[str]]): Список токенов, на которых необходимо прекратить генерацию. По умолчанию None.

**Возвращает**:
- `List[dict]`: Список payload'ов в виде словарей.

**Пример**:
```python
payloads = prepare_payload_from_list(
    prompts=["Напишите текст о кошке", "Напишите текст о собаке"],
    model="text-davinci-003",
    temperature=0.5,
    max_tokens=50,
)
print(payloads)
```
**Пример вывода**:
```json
[
  {
    "model": "text-davinci-003",
    "prompt": "Напишите текст о кошке",
    "temperature": 0.5,
    "max_tokens": 50,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
  },
  {
    "model": "text-davinci-003",
    "prompt": "Напишите текст о собаке",
    "temperature": 0.5,
    "max_tokens": 50,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
  }
]
```