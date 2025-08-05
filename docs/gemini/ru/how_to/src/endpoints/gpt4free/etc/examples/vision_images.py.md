## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует, как использовать GPT-4Free API для анализа изображений. Он показывает примеры обработки как удаленных, так и локальных изображений.

Шаги выполнения
-------------------------
1. **Инициализация клиента:** Создается объект `Client` для взаимодействия с API GPT-4Free.
2. **Загрузка удаленного изображения:** 
   - Используется библиотека `requests` для загрузки изображения по URL.
   - Данные изображения преобразуются в байтовый поток (binary stream).
3. **Загрузка локального изображения:**
   - Используется встроенная функция `open` для открытия локального файла изображения в режиме чтения в байтовом потоке.
4. **Отправка запроса в API:**
   - Используется метод `client.chat.completions.create` для отправки запроса.
   - Устанавливается модель `g4f.models.default_vision` для обработки изображений.
   - Указывается текст запроса `{"role": "user", "content": "What are on this image?"}`.
   - Передаются данные изображения (`remote_image` или `local_image`).
5. **Обработка ответа:**
   -  Извлекается текст ответа из `response_remote.choices[0].message.content` или `response_local.choices[0].message.content`.
   - Выводится ответ на консоль.
6. **Закрытие локального файла:** 
   - Закрывается файл изображения `local_image` после использования.


Пример использования
-------------------------

```python
import g4f
import requests

from g4f.client import Client

client = Client()

# Processing remote image
remote_image = requests.get("https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/images/cat.jpeg", stream=True).content
response_remote = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=remote_image
)
print("Response for remote image:")
print(response_remote.choices[0].message.content)

print("\n" + "-"*50 + "\n")  # Separator

# Processing local image
local_image = open("docs/images/cat.jpeg", "rb")
response_local = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=local_image
)
print("Response for local image:")
print(response_local.choices[0].message.content)
local_image.close()  # Close file after use
```