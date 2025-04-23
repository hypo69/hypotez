### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот блок кода определяет структуры данных (Data Transfer Objects - DTO), используемые для конфигурации чат-ботов, генерации изображений, а также для представления ответов от различных провайдеров и моделей, включая сообщения об ошибках и информацию о загруженных файлах. Он использует библиотеку Pydantic для определения схем данных с возможностью валидации и автоматической генерации документации.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `BaseModel`, `Field` из библиотеки `pydantic` для создания моделей данных.
   - Импортируются `Union` и `Optional` из `typing` для определения типов данных.
   - Выполняется попытка импорта `Annotated` из `typing`. Если импорт не удаётся (для старых версий Python), создаётся пустой класс `Annotated`.
   - Импортируется `Messages` из `g4f.typing`.

2. **Определение класса `ChatCompletionsConfig`**:
   - Этот класс используется для конфигурации чат-ботов.
   - Поля класса:
     - `messages`: Список сообщений для чат-бота. Используется `Messages` тип, заданный в `g4f.typing`. Предоставлен пример структуры сообщения.
     - `model`: Идентификатор используемой модели.
     - `provider`: Провайдер модели (опционально).
     - `stream`: Флаг для стриминга ответов (по умолчанию `False`).
     - `image`, `image_name`, `images`, `media`: Опциональные поля для мультимодальных запросов.
     - `modalities`: Список модальностей, используемых в запросе (текст, аудио и т.д.).
     - `temperature`, `presence_penalty`, `frequency_penalty`, `top_p`: Параметры для контроля генерации текста.
     - `max_tokens`: Максимальное количество токенов в ответе.
     - `stop`: Условия остановки генерации текста.
     - `api_key`, `api_base`: Параметры для аутентификации API.
     - `web_search`: Флаг для включения веб-поиска.
     - `proxy`: Прокси-сервер для использования.
     - `conversation_id`, `conversation`, `return_conversation`, `history_disabled`: Параметры для управления историей разговоров.
     - `timeout`: Максимальное время ожидания ответа.
     - `tool_calls`, `tools`, `parallel_tool_calls`, `tool_choice`: Параметры для использования инструментов (tools) в запросах.
     - `reasoning_effort`: Параметр для контроля усилий по рассуждению.
     - `logit_bias`: Параметр для смещения вероятностей токенов.
     - `audio`: Параметр для передачи аудио данных.
     - `response_format`: Параметр для указания формата ответа.
     - `extra_data`: Дополнительные данные для передачи в запросе.

3. **Определение класса `ImageGenerationConfig`**:
   - Используется для конфигурации генерации изображений.
   - Поля класса:
     - `prompt`: Текстовое описание изображения для генерации.
     - `model`, `provider`: Модель и провайдер для генерации изображений (опционально).
     - `response_format`: Формат ответа (опционально).
     - `api_key`, `proxy`: Параметры для аутентификации API и прокси-сервера (опционально).
     - `width`, `height`: Размеры генерируемого изображения (опционально).
     - `num_inference_steps`: Количество шагов для генерации изображения (опционально).
     - `seed`: Зерно для генерации случайных чисел (опционально).
     - `guidance_scale`: Масштаб направления (опционально).
     - `aspect_ratio`: Соотношение сторон изображения (опционально).
     - `n`: Количество генерируемых изображений (опционально).
     - `negative_prompt`: Негативное описание, чтобы избежать нежелательных элементов на изображении (опционально).
     - `resolution`: Разрешение изображения (опционально).

4. **Определение классов для ответов провайдеров**:
   - `ProviderResponseModel`: Базовый класс для ответов провайдеров.
     - `id`: Идентификатор ответа.
     - `object`: Тип объекта (всегда "provider").
     - `created`: Временная метка создания.
     - `url`: URL ресурса (опционально).
     - `label`: Метка (опционально).
   - `ProviderResponseDetailModel`: Расширенный класс для ответов провайдеров с детальной информацией.
     - `models`: Список поддерживаемых моделей.
     - `image_models`: Список моделей для генерации изображений.
     - `vision_models`: Список моделей для компьютерного зрения.
     - `params`: Список параметров.

5. **Определение классов для ответов моделей**:
   - `ModelResponseModel`: Класс для представления ответов моделей.
     - `id`: Идентификатор модели.
     - `object`: Тип объекта (всегда "model").
     - `created`: Временная метка создания.
     - `owned_by`: Владелец модели (опционально).

6. **Определение классов для загрузки файлов**:
   - `UploadResponseModel`: Класс для представления ответов при загрузке файлов.
     - `bucket_id`: Идентификатор бакета.
     - `url`: URL загруженного файла.

7. **Определение классов для ошибок**:
   - `ErrorResponseModel`: Класс для представления ошибок.
     - `error`: Объект `ErrorResponseMessageModel`, содержащий сообщение об ошибке.
     - `model`: Модель, вызвавшая ошибку (опционально).
     - `provider`: Провайдер, вызвавший ошибку (опционально).
   - `ErrorResponseMessageModel`: Класс для представления сообщения об ошибке.
     - `message`: Текст сообщения об ошибке.

8. **Определение класса `FileResponseModel`**:
   - `FileResponseModel`: Класс для представления информации о файле.
     - `filename`: Имя файла.

Пример использования
-------------------------

```python
from g4f.api.stubs import ChatCompletionsConfig

# Пример создания конфигурации для чат-бота
config = ChatCompletionsConfig(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    model="gpt-3.5-turbo",
    temperature=0.7
)

print(config.model_dump_json(indent=2))
# {
#   "messages": [
#     {
#       "role": "system",
#       "content": "You are a helpful assistant."
#     },
#     {
#       "role": "user",
#       "content": "What is the capital of France?"
#     }
#   ],
#   "model": "gpt-3.5-turbo",
#   "provider": null,
#   "stream": false,
#   "image": null,
#   "image_name": null,
#   "images": null,
#   "media": null,
#   "temperature": 0.7,
#   "presence_penalty": null,
#   "frequency_penalty": null,
#   "top_p": null,
#   "max_tokens": null,
#   "stop": null,
#   "api_key": null,
#   "api_base": null,
#   "web_search": null,
#   "proxy": null,
#   "conversation_id": null,
#   "conversation": null,
#   "return_conversation": null,
#   "history_disabled": null,
#   "timeout": null,
#   "tool_calls": [],
#   "tools": null,
#   "parallel_tool_calls": null,
#   "tool_choice": null,
#   "reasoning_effort": null,
#   "logit_bias": null,
#   "audio": null,
#   "response_format": null,
#   "extra_data": null
# }
```
```python
from g4f.api.stubs import ImageGenerationConfig

# Пример создания конфигурации для генерации изображений
image_config = ImageGenerationConfig(
    prompt="A cat sitting on a mat",
    model="dall-e-3",
    n=1
)

print(image_config.model_dump_json(indent=2))
# {
#   "prompt": "A cat sitting on a mat",
#   "model": "dall-e-3",
#   "provider": null,
#   "response_format": null,
#   "api_key": null,
#   "proxy": null,
#   "width": null,
#   "height": null,
#   "num_inference_steps": null,
#   "seed": null,
#   "guidance_scale": null,
#   "aspect_ratio": null,
#   "n": 1,
#   "negative_prompt": null,
#   "resolution": null
# }
```
```python
from g4f.api.stubs import ErrorResponseModel, ErrorResponseMessageModel

# Пример создания объекта ошибки
error_message = ErrorResponseMessageModel(message="Something went wrong")
error_response = ErrorResponseModel(error=error_message, model="gpt-3.5-turbo")

print(error_response.model_dump_json(indent=2))
# {
#   "error": {
#     "message": "Something went wrong"
#   },
#   "model": "gpt-3.5-turbo",
#   "provider": null
# }
```
```python
from g4f.api.stubs import FileResponseModel

# Пример создания модели ответа файла
file_response = FileResponseModel(filename="example.txt")
print(file_response.model_dump_json(indent=2))
# {
#   "filename": "example.txt"
# }
```