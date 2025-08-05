# src/ai/openai/README.md

## Обзор

Модуль `src.ai.openai` предоставляет функциональность для взаимодействия с API OpenAI. 
Он позволяет использовать различные возможности OpenAI, включая генерацию текста, 
перевод,  и многое другое.

## Подробней

Данный модуль является частью проекта `hypotez`, который предоставляет набор инструментов для 
обработки данных и автоматизации задач. Модуль `src.ai.openai` взаимодействует с API OpenAI для 
реализации различных функций, связанных с искусственным интеллектом, таких как: 

- **Генерация текста:** Модель может генерировать текст, 
  напоминающий текст человека, в соответствии с заданными инструкциями.
- **Перевод:** Модель может переводить текст с одного языка на другой.
- **Ответы на вопросы:** Модель может отвечать на вопросы, 
  представленные ей в виде текста.
- **Суммирование текста:** Модель может обобщать текст, 
  сохраняя при этом главные идеи и информацию.
- **Завершение текста:** Модель может завершить текст, 
  предложенный пользователем, в соответствии с его контекстом. 

##  Классы

###  `OpenAIClient`

**Описание**: Класс `OpenAIClient` предоставляет интерфейс для взаимодействия 
с API OpenAI. Он позволяет отправлять запросы, получать ответы и управлять ключом API.

**Наследует**: 

**Атрибуты**:
- `api_key` (str):  Ключ API, полученный на сайте OpenAI. 
- `api_base` (str): Базовый URL для API OpenAI.

**Принцип работы**:

Класс `OpenAIClient` предоставляет функции для отправки запросов к API OpenAI. 
Он использует библиотеку `requests` для отправки HTTP-запросов.

**Методы**:

- `get_response(model: str, prompt: str, temperature: float = 0.5) -> Dict[str, Any]`: 
  Отправляет запрос к API OpenAI с указанным текстом запроса (`prompt`), 
  моделью (`model`) и температурой (`temperature`). 
  Возвращает ответ в виде словаря.

  **Параметры**:

  - `model` (str): Название модели OpenAI.
  - `prompt` (str): Текст запроса к API OpenAI.
  - `temperature` (float): Уровень креативности модели.

  **Возвращает**:
  - `Dict[str, Any]`: Словарь с ответом от OpenAI.

  **Примеры**:

  ```python
  from src.ai.openai import OpenAIClient

  client = OpenAIClient(api_key='YOUR_API_KEY')

  # Сгенерировать текст
  response = client.get_response(model='text-davinci-003', prompt='Напишите стихотворение про кота.')

  # Вывести результат
  print(response['choices'][0]['text'])
  ```
- `get_translation(model: str, source_language: str, target_language: str, text: str) -> str`: 
  Переводит текст с одного языка на другой.

  **Параметры**:

  - `model` (str): Название модели OpenAI.
  - `source_language` (str):  Код языка исходного текста.
  - `target_language` (str): Код языка, на который нужно перевести текст.
  - `text` (str): Текст для перевода.

  **Возвращает**:

  - `str`: Переведенный текст.

  **Примеры**:

  ```python
  from src.ai.openai import OpenAIClient

  client = OpenAIClient(api_key='YOUR_API_KEY')

  # Перевести текст с русского на английский
  translated_text = client.get_translation(
      model='gpt-3.5-turbo', source_language='ru', target_language='en', text='Привет мир!'
  )

  # Вывести результат
  print(translated_text)
  ```

## Функции

### `get_openai_response(model: str, prompt: str, temperature: float = 0.5) -> Dict[str, Any]`

**Назначение**: Функция отправляет запрос к API OpenAI и возвращает ответ в 
виде словаря. 

**Параметры**:

- `model` (str): Название модели OpenAI.
- `prompt` (str): Текст запроса к API OpenAI.
- `temperature` (float): Уровень креативности модели.

**Возвращает**:
- `Dict[str, Any]`: Словарь с ответом от OpenAI.

**Примеры**:

```python
from src.ai.openai import get_openai_response

# Сгенерировать текст
response = get_openai_response(model='text-davinci-003', prompt='Напишите стихотворение про кота.')

# Вывести результат
print(response['choices'][0]['text'])