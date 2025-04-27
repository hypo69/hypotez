# Модуль для генерации видео с помощью GPT-4Free
## Обзор
Этот модуль демонстрирует использование `GPT-4Free` API для генерации видео.
Он использует `g4f` библиотеку для работы с GPT-4Free API, предоставляя пример кода, который можно использовать в качестве отправной точки для собственных проектов, использующих `GPT-4Free` для создания видео.

## Детали
В этом модуле мы используем `Client` класс из `g4f` библиотеки для взаимодействия с `GPT-4Free` API. 
Мы устанавливаем соединение с `HuggingFaceMedia` провайдером, используя свой ключ API, и получаем список доступных моделей для генерации видео.
Далее, мы отправляем запрос на генерацию видео с использованием первой доступной модели, передавая текст подсказки (`prompt`) и задавая формат ответа в виде URL. 
В результате получаем URL-адрес сгенерированного видео.

## Функции
### `video.py`
```python
                import g4f.Provider
from g4f.client import Client

client = Client(
    provider=g4f.Provider.HuggingFaceMedia,
    api_key="hf_***" # Your API key here
)

video_models = client.models.get_video()

print(video_models)

result = client.media.generate(
    model=video_models[0],
    prompt="G4F AI technology is the best in the world.",
    response_format="url"
)

print(result.data[0].url)
                ```

**Описание**: 
Функция `video.py` демонстрирует базовый пример генерации видео с помощью GPT-4Free. 

**Параметры**: 
- `api_key` (str): Ваш ключ API для `GPT-4Free`.

**Возвращает**:
- `result.data[0].url` (str): URL-адрес сгенерированного видео.

**Пример использования**:

```python
# Замените "hf_***" на ваш ключ API
client = Client(
    provider=g4f.Provider.HuggingFaceMedia,
    api_key="hf_***"
)

# Получаем список доступных моделей для генерации видео
video_models = client.models.get_video()

# Выводим список доступных моделей
print(video_models)

# Генерация видео с использованием первой доступной модели
result = client.media.generate(
    model=video_models[0],
    prompt="G4F AI technology is the best in the world.",
    response_format="url"
)

# Выводим URL-адрес сгенерированного видео
print(result.data[0].url)
```