### **Как использовать блок кода `RetryProvider`**

=========================================================================================

Описание
-------------------------
Блок кода реализует класс `RetryProvider`, который предназначен для повторных попыток использования различных провайдеров для получения ответа на запрос. Если один провайдер не отвечает или возвращает ошибку, `RetryProvider` автоматически переключается на следующий провайдер из списка и повторяет попытку.

Шаги выполнения
-------------------------
1. **Инициализация `RetryProvider`**:
   - Класс `RetryProvider` принимает список провайдеров (`providers`), флаг перемешивания списка (`shuffle`), флаг повтора только для одного провайдера (`single_provider_retry`) и максимальное количество попыток (`max_retries`).
   - При инициализации вызывается конструктор родительского класса `IterListProvider` с указанием списка провайдеров и флага перемешивания.
   - Устанавливаются значения атрибутов `single_provider_retry` и `max_retries`.

2. **Метод `create_completion`**:
   - Этот метод пытается получить ответ от провайдеров, выполняя повторные попытки в случае ошибок.
   - Если `single_provider_retry` установлен в `True`, метод пытается использовать только первого провайдера из списка `providers` `max_retries` раз.
   - Если `single_provider_retry` установлен в `False`, метод перебирает всех провайдеров из списка, пока не получит ответ.
   - Внутри цикла `try` вызывается метод `get_create_function()` текущего провайдера для получения ответа.
   - Ответ передается по частям через `yield`, и если часть ответа получена, устанавливается флаг `started`.
   - Если во время получения ответа происходит исключение, оно записывается в словарь `exceptions`.

3. **Метод `create_async_generator`**:
   - Аналогичен методу `create_completion`, но предназначен для асинхронного выполнения.
   - Также поддерживает флаг `single_provider_retry` для повторных попыток с одним провайдером.
   - Использует `get_async_create_function()` для получения асинхронного генератора ответов.
   - Асинхронно перебирает части ответа и передает их через `yield`.

4. **Функция `raise_exceptions`**:
   - Если во время работы `RetryProvider` возникли исключения, эта функция генерирует исключение `RetryProviderError` или `RetryNoProviderError`.
   - `RetryProviderError` генерируется, если хотя бы один провайдер вернул ошибку.
   - `RetryNoProviderError` генерируется, если ни один провайдер не был найден.

Пример использования
-------------------------

```python
from typing import List
from g4f.providers import RetryProvider, GeminiProChat, ChatgptAi

# Пример использования RetryProvider
providers: List = [
    GeminiProChat,
    ChatgptAi
]

retry_provider = RetryProvider(
    providers=providers,
    shuffle=True,
    single_provider_retry=False,
    max_retries=3
)

try:
    # Используем retry_provider для получения ответа
    response = retry_provider.create_completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, World!"}],
        stream=False
    )
    for chunk in response:
        print(chunk)
except Exception as e:
    print(f"An error occurred: {e}")
```