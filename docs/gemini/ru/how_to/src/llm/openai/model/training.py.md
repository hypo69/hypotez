## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет функцию `describe_image_by_requests`, которая отправляет изображение на OpenAI API и получает описание.  

Шаги выполнения
-------------------------
1. **Получение base64-кодированного изображения**: Используя функцию `base64encode(image_path)` из модуля `src.utils.convertors.base64`, кодирует изображение в base64-формат.
2. **Подготовка заголовков и данных для запроса**:
    - Создает словарь `headers`, содержащий заголовки для запроса, включая `Content-Type` и `Authorization`.
    - Создает словарь `payload`, содержащий данные для запроса, такие как `model`, `messages` и `max_tokens`. 
    - В `messages`  запрос содержит текстовый запрос (prompt), если он задан, и base64-кодированное изображение,  отправленное в виде `image_url`.
3. **Отправка запроса на OpenAI API**:  Использует функцию `requests.post` для отправки запроса на API `https://api.openai.com/v1/chat/completions` с заголовками `headers` и данными `payload`.
4. **Обработка ответа**: 
    - Проверяет, был ли запрос успешен (status code 200).
    - В случае успеха преобразует полученный JSON-ответ в словарь `response_json`.

Пример использования
-------------------------

```python
from src.llm.openai.model.training import OpenAIModel

# Инициализация модели OpenAI
model = OpenAIModel(api_key='YOUR_API_KEY')

# Путь к изображению
image_path = gs.path.google_drive / 'images' / 'example_image.jpg'

# Необязательный запрос (prompt)
prompt = "Что на этом изображении?"

# Вызов функции describe_image_by_requests
description = model.describe_image_by_requests(image_path, prompt)

# Вывод описания
print(f"Описание изображения: {description}")
```