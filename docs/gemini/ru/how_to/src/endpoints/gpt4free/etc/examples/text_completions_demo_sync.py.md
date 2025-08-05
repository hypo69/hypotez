## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода демонстрирует синхронное использование API gpt-4free для генерации текста с помощью модели `gpt-4o`. 

Шаги выполнения
-------------------------
1. Импортируется класс `Client` из модуля `g4f.client`.
2. Создается экземпляр класса `Client`.
3. Вызывается метод `create` у объекта `client.chat.completions`.
    - Устанавливается параметр `model`  равным `"gpt-4o"`  для использования модели GPT-4.
    - Передается список `messages`  с двумя элементами:
        - Первый элемент (`role`: `"system"`, `content`: `"You are a helpful assistant."`) задает роль системы как "полезный помощник".
        - Второй элемент (`role`: `"user"`, `content`: `"how does a court case get to the Supreme Court?"`) задает вопрос пользователя.
4. Полученный ответ (`response`) от сервера содержит список `choices`.
5. Извлекается первый выбор (`response.choices[0]`) и его содержимое (`message.content`).
6. Выводится на экран текст ответа модели.

Пример использования
-------------------------

```python
from g4f.client import Client

client = Client()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
)

print(response.choices[0].message.content)
```

В этом примере задается вопрос "What is the capital of France?".  Модель GPT-4 ответит на этот вопрос, и результат будет выведен на экран.