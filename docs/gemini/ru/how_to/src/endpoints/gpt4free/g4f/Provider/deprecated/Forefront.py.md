## Как использовать Forefront в проекте hypotez
=========================================================================================

Описание
-------------------------
Класс `Forefront` реализует провайдера `gpt-4` для использования с помощью библиотеки `requests` на бесплатной платформе `Forefront.com`. Данный класс позволяет генерировать текст, используя модель `gpt-4` в режиме потоковой передачи, а также поддерживает модель `gpt-3.5-turbo`.

Шаги выполнения
-------------------------
1. **Инициализация**: Класс `Forefront` создается как экземпляр класса `AbstractProvider`.
2. **Создание запроса**: Метод `create_completion` принимает в качестве аргументов название модели, список сообщений, режим потоковой передачи и дополнительные параметры.
3. **Формирование JSON-запроса**: В методе `create_completion` формируется JSON-запрос, содержащий информацию о модели, сообщениях, режиме потоковой передачи и других параметрах.
4. **Отправка запроса**: Используется `requests.post` для отправки запроса на сервер `Forefront` по адресу "https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat".
5. **Обработка ответа**: Метод `iter_lines` используется для получения строк из ответа сервера. Каждая строка, содержащая "delta", декодируется и парсится с помощью `json.loads`. 
6. **Возврат результата**: Генератор `yield` возвращает значения "delta" из декодированного JSON-ответа, которые представляют собой части генерируемого текста.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Forefront import Forefront

provider = Forefront()

messages = [
    {"role": "user", "content": "Привет!"},
    {"role": "assistant", "content": "Привет! Как дела?"},
]

# Создание запроса для модели gpt-4 в режиме потоковой передачи
for token in provider.create_completion(model="gpt-4", messages=messages, stream=True):
    print(token)

# Создание запроса для модели gpt-3.5-turbo
for token in provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False):
    print(token)
```