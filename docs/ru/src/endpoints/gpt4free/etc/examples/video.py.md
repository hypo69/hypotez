# Модуль для генерации видео с использованием g4f.Provider

## Обзор

Этот модуль предназначен для создания видеороликов с использованием библиотеки `g4f` (GPT4Free) и провайдера `HuggingFaceMedia`. Он содержит пример кода для инициализации клиента, получения доступных видео-моделей и генерации видео на основе текстового запроса.

## Подробней

Модуль демонстрирует, как использовать `g4f` для работы с видео-моделями, предоставляемыми `HuggingFaceMedia`. Он включает в себя:

1.  Импорт необходимых библиотек `g4f.Provider` и `g4f.client.Client`.
2.  Создание экземпляра клиента `Client` с указанием провайдера `HuggingFaceMedia` и API-ключа.
3.  Получение списка доступных видео-моделей с помощью метода `client.models.get_video()`.
4.  Генерацию видеоролика на основе текстового запроса с использованием метода `client.media.generate()`.
5.  Вывод URL сгенерированного видео.

## Функции

### `client.media.generate`

```python
result = client.media.generate(
    model=video_models[0],
    prompt="G4F AI technology is the best in the world.",
    response_format="url"
)
```

**Назначение**: Генерация видеоролика на основе текстового запроса.

**Параметры**:

*   `model` (str): Идентификатор видео-модели, используемой для генерации видео.
*   `prompt` (str): Текстовый запрос, на основе которого генерируется видео.
*   `response_format` (str): Формат ответа. В данном случае `"url"`, указывающий на то, что в ответе ожидается URL сгенерированного видео.

**Возвращает**:

*   `result`: Объект, содержащий информацию о сгенерированном видео, включая URL.

**Как работает функция**:

1.  Функция принимает идентификатор видео-модели и текстовый запрос.
2.  Отправляет запрос к `HuggingFaceMedia` для генерации видео на основе указанных параметров.
3.  Получает ответ от `HuggingFaceMedia`, содержащий информацию о сгенерированном видео.
4.  Извлекает URL сгенерированного видео из ответа.

```
   Запрос на генерацию видео
   |
   ↓
   Отправка запроса к HuggingFaceMedia
   |
   ↓
   Получение ответа с информацией о видео
   |
   ↓
   Извлечение URL видео из ответа
```

**Примеры**:

```python
import g4f.Provider
from g4f.client import Client

client = Client(
    provider=g4f.Provider.HuggingFaceMedia,
    api_key="hf_***" # Your API key here
)

video_models = client.models.get_video()

# Генерация видео с использованием первой доступной модели и запроса "G4F AI technology is the best in the world."
result = client.media.generate(
    model=video_models[0],
    prompt="G4F AI technology is the best in the world.",
    response_format="url"
)

print(result.data[0].url)
```

### `client.models.get_video`

```python
video_models = client.models.get_video()
```

**Назначение**: Получение списка доступных видео-моделей.

**Параметры**:

*   Нет.

**Возвращает**:

*   `video_models` (List[str]): Список идентификаторов доступных видео-моделей.

**Как работает функция**:

1.  Функция отправляет запрос к `HuggingFaceMedia` для получения списка доступных видео-моделей.
2.  Получает ответ от `HuggingFaceMedia`, содержащий список идентификаторов видео-моделей.

```
   Запрос списка видео-моделей
   |
   ↓
   Отправка запроса к HuggingFaceMedia
   |
   ↓
   Получение ответа со списком видео-моделей
```

**Примеры**:

```python
import g4f.Provider
from g4f.client import Client

client = Client(
    provider=g4f.Provider.HuggingFaceMedia,
    api_key="hf_***" # Your API key here
)

# Получение списка доступных видео-моделей
video_models = client.models.get_video()

print(video_models)