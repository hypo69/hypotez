## Как использовать класс `EasyChat`

=========================================================================================

Описание
-------------------------
Класс `EasyChat` предоставляет функциональность для взаимодействия с API EasyChat для генерации текста. 

Шаги выполнения
-------------------------
1. **Инициализация класса:** Создайте экземпляр класса `EasyChat` для использования.

2. **Использование метода `create_completion`**:
    - Передаем в метод `create_completion` необходимые параметры, такие как модель (`model`), сообщения (`messages`), а также дополнительные параметры, такие как `temperature`, `presence_penalty`, `frequency_penalty`, `top_p`. 
    - Метод отправляет запрос на сервер EasyChat и возвращает ответ, который может быть как текстом, так и потоком данных (stream).

3. **Обработка ответа**:
    - Если `stream` установлен в `False`, метод `create_completion` возвращает текст, который может быть обработан для дальнейшего использования.
    - Если `stream` установлен в `True`, метод `create_completion` возвращает генератор, который позволяет получать данные по частям, в виде потока.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.EasyChat import EasyChat

# Создание экземпляра класса
easychat = EasyChat()

# Создание сообщения
messages = [
    {"role": "user", "content": "Привет!"},
]

# Вызов метода create_completion
# Получаем ответ в виде текста
response = easychat.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)

# Вывод ответа
print(response)

# Вызов метода create_completion
# Получаем ответ в виде потока данных
response = easychat.create_completion(model="gpt-3.5-turbo", messages=messages, stream=True)

# Обработка потока данных
for chunk in response:
    print(chunk)
```