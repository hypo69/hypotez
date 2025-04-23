### Как использовать блок кода `ThebApi`
=========================================================================================

Описание
-------------------------
Класс `ThebApi` является частью модуля `g4f.Provider` и предназначен для взаимодействия с API сервиса TheB.AI. Он наследуется от класса `OpenaiTemplate` и предоставляет методы для создания асинхронных генераторов на основе моделей, поддерживаемых TheB.AI. Класс определяет URL, базовый URL API, необходимость аутентификации, а также список поддерживаемых моделей.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются классы `CreateResult` и `Messages` из модуля `...typing`.
   - Импортируются функции `filter_none` из модуля `..helper` и `OpenaiTemplate` из модуля `..template`.

2. **Определение словаря моделей**:
   - Создается словарь `models`, который содержит соответствия между именами моделей, используемыми в коде, и их отображаемыми названиями на сервисе TheB.AI.
     ```python
     models = {
         "theb-ai": "TheB.AI",
         "gpt-3.5-turbo": "GPT-3.5",
         "gpt-4-turbo": "GPT-4 Turbo",
         "gpt-4": "GPT-4",
         "claude-3.5-sonnet": "Claude",
         "llama-2-7b-chat": "Llama 2 7B",
         "llama-2-13b-chat": "Llama 2 13B",
         "llama-2-70b-chat": "Llama 2 70B",
         "code-llama-7b": "Code Llama 7B",
         "code-llama-13b": "Code Llama 13B",
         "code-llama-34b": "Code Llama 34B",
         "qwen-2-72b": "Qwen"
     }
     ```

3. **Определение класса `ThebApi`**:
   - Класс `ThebApi` наследуется от `OpenaiTemplate` и определяет атрибуты, специфичные для TheB.AI API:
     ```python
     class ThebApi(OpenaiTemplate):
         label = "TheB.AI API"
         url = "https://theb.ai"
         login_url = "https://beta.theb.ai/home"
         api_base = "https://api.theb.ai/v1"
         working = True
         needs_auth = True

         default_model = "theb-ai"
         fallback_models = list(models)
     ```
     - `label`: Отображаемое название API.
     - `url`: URL сервиса TheB.AI.
     - `login_url`: URL для входа в сервис.
     - `api_base`: Базовый URL API TheB.AI.
     - `working`: Указывает, что API в рабочем состоянии.
     - `needs_auth`: Указывает, что для работы с API требуется аутентификация.
     - `default_model`: Модель, используемая по умолчанию.
     - `fallback_models`: Список моделей, которые могут быть использованы в качестве запасных.

4. **Определение метода `create_async_generator`**:
   - Метод `create_async_generator` создает асинхронный генератор для получения ответов от API TheB.AI.
     ```python
     @classmethod
     def create_async_generator(
         cls,
         model: str,
         messages: Messages,
         temperature: float = None,
         top_p: float = None,
         **kwargs
     ) -> CreateResult:
         system_message = "\\n".join([message["content"] for message in messages if message["role"] == "system"])
         messages = [message for message in messages if message["role"] != "system"]
         data = {
             "model_params": filter_none(
                 system_prompt=system_message,
                 temperature=temperature,
                 top_p=top_p,
             )
         }
         return super().create_async_generator(model, messages, extra_data=data, **kwargs)
     ```
     - `model`: Имя модели, которую необходимо использовать.
     - `messages`: Список сообщений для отправки в API.
     - `temperature`: Параметр температуры для управления случайностью генерации.
     - `top_p`: Параметр `top_p` для управления разнообразием генерации.
     - `system_message`: Извлекается системное сообщение из списка сообщений.
     - `messages`: Оставляются только сообщения, не являющиеся системными.
     - `data`: Формируется словарь данных для отправки в API, включающий параметры модели.
     - Вызывается метод `create_async_generator` родительского класса `OpenaiTemplate` с передачей необходимых параметров.

Пример использования
-------------------------

```python
 from g4f.Provider.needs_auth import ThebApi
 from g4f.typing import Message

 # Создание экземпляра класса ThebApi
 theb_api = ThebApi()

 # Определение списка сообщений
 messages: list[Message] = [
     {"role": "system", "content": "You are a helpful assistant."},
     {"role": "user", "content": "What is the capital of France?"}
 ]

 # Вызов метода create_async_generator для получения асинхронного генератора
 generator = theb_api.create_async_generator(
     model="theb-ai",
     messages=messages,
     temperature=0.7,
     top_p=0.9
 )

 # Асинхронный перебор генератора для получения ответов
 async for response in generator:
     print(response)