## Как использовать RetryProvider
=========================================================================================

Описание
-------------------------
RetryProvider - это класс, который предоставляет механизм повторных попыток для доступа к разным API-провайдерам. Он принимает список провайдеров и предоставляет удобный способ переключаться между ними в случае, если один провайдер недоступен или возвращает ошибку.

Шаги выполнения
-------------------------
1. **Инициализация RetryProvider:**
    - Создайте экземпляр класса RetryProvider, передав список провайдеров, которые нужно использовать.
    - Укажите, нужно ли перемешивать список провайдеров (shuffle), а также настройки для повторных попыток (single_provider_retry, max_retries).
2. **Создание завершения (completion):**
    - Вызовите метод `create_completion()` для генерации текста.
    - Передайте в качестве параметров модель (model), сообщения (messages) и флаг `stream` (если нужно получить поток данных).
    - Метод `create_completion()` попробует выполнить запрос к каждому провайдеру в списке, переключаясь на следующий, если текущий провайдер недоступен.
3. **Обработка результатов:**
    - Метод `create_completion()` возвращает генератор, который выдает токены или результат завершения.
    - Пройдемся по результатам генератора и обработаем данные.
4. **Обработка исключений:**
    - Если все провайдеры недоступны, RetryProvider выбросит исключение RetryProviderError или RetryNoProviderError, содержащее информацию об ошибках, которые произошли в каждом провайдере.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.providers import RetryProvider
from hypotez.src.endpoints.gpt4free.g4f.providers.types import BaseProvider
from hypotez.src.endpoints.gpt4free.g4f.providers.openai import OpenAI
from hypotez.src.endpoints.gpt4free.g4f.providers.gpt4free import GPT4Free

# Создайте список провайдеров
providers: List[Type[BaseProvider]] = [OpenAI, GPT4Free]

# Создайте экземпляр RetryProvider
retry_provider = RetryProvider(providers, shuffle=True, single_provider_retry=True, max_retries=3)

# Сообщение для завершения
messages = [
    {"role": "user", "content": "Привет! Расскажи мне о себе."},
]

# Сгенерируйте завершение
for chunk in retry_provider.create_completion(model="text-davinci-003", messages=messages):
    print(chunk)

```