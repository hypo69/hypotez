# Модуль для генерации видео с использованием g4f.Provider.HuggingFaceMedia 

## Обзор

Данный модуль демонстрирует пример использования библиотеки `g4f` для генерации видео с помощью модели `HuggingFaceMedia` от `g4f.Provider`. 

## Подробности

В коде представлен следующий алгоритм:

1. **Инициализация клиента:** Создается экземпляр класса `Client` с использованием `g4f.Provider.HuggingFaceMedia` в качестве провайдера. 
2. **Получение списка моделей:** Вызывается метод `client.models.get_video()` для получения списка доступных моделей для генерации видео.
3. **Генерация видео:** Вызывается метод `client.media.generate()` с указанием модели, текстового запроса (`prompt`) и формата ответа (`response_format`). 
4. **Вывод URL:** В качестве ответа возвращается URL сгенерированного видео, который выводится на консоль.

## Пример использования 

```python
import g4f.Provider
from g4f.client import Client

client = Client(
    provider=g4f.Provider.HuggingFaceMedia,
    api_key="hf_***" # Ваш API ключ
)

video_models = client.models.get_video()

print(video_models)

result = client.media.generate(
    model=video_models[0],
    prompt="G4F AI технология - лучшая в мире.",
    response_format="url"
)

print(result.data[0].url)