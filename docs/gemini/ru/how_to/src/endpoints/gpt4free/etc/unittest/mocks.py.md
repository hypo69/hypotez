### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет набор классов-заглушек (моков) для имитации различных поставщиков (провайдеров) в системе `g4f` (Generative for free). Эти моки используются для юнит-тестирования, позволяя изолировать компоненты и проверять их поведение в контролируемых условиях. Моки охватывают различные сценарии, такие как успешное выполнение, асинхронное выполнение, генерация последовательности результатов, возвращение изображений, возникновение ошибок аутентификации и другие исключения.

Шаги выполнения
-------------------------
1. **Определение базовых классов**:
   - Классы `ProviderMock`, `AsyncProviderMock`, `AsyncGeneratorProviderMock`, `ModelProviderMock`, `YieldProviderMock`, `YieldImageResponseProviderMock`, `MissingAuthProviderMock`, `RaiseExceptionProviderMock`, `AsyncRaiseExceptionProviderMock`, `YieldNoneProviderMock` наследуются от `AbstractProvider`, `AsyncProvider` или `AsyncGeneratorProvider`.
   - Каждый класс переопределяет метод `create_completion` или `create_async_generator` (в зависимости от типа провайдера) для имитации поведения реального провайдера.

2. **Имитация успешного выполнения**:
   - Классы `ProviderMock`, `AsyncProviderMock` и `AsyncGeneratorProviderMock` имитируют успешное выполнение, возвращая строку "Mock" в качестве результата.

3. **Имитация возврата модели**:
   - Класс `ModelProviderMock` возвращает название модели (`model`) в качестве результата.

4. **Имитация генерации последовательности результатов**:
   - Класс `YieldProviderMock` генерирует последовательность результатов на основе содержимого сообщений (`messages`), возвращая содержимое каждого сообщения.

5. **Имитация возврата изображения**:
   - Класс `YieldImageResponseProviderMock` возвращает объект `ImageResponse` с имитацией изображения.

6. **Имитация ошибки аутентификации**:
   - Класс `MissingAuthProviderMock` выбрасывает исключение `MissingAuthError`, имитируя отсутствие аутентификации.

7. **Имитация возникновения исключений**:
   - Классы `RaiseExceptionProviderMock` и `AsyncRaiseExceptionProviderMock` выбрасывают исключение `RuntimeError`, имитируя возникновение ошибки во время выполнения.

8. **Имитация возврата `None`**:
   - Класс `YieldNoneProviderMock` генерирует `None` в качестве результата.

Пример использования
-------------------------

```python
from g4f.models import Model

async def test_provider_mock():
    # Пример использования AsyncProviderMock
    model = Model.gpt_35_turbo
    messages = [{"role": "user", "content": "Hello"}]
    result = await AsyncProviderMock.create_async(model=model, messages=messages)
    print(result)

# Пример использования MissingAuthProviderMock (вызовет исключение)
try:
    for chunk in MissingAuthProviderMock.create_completion(model=Model.gpt_35_turbo, messages=[{"role": "user", "content": "test"}], stream=True):
        print(chunk, end='')
except MissingAuthError as e:
    print(f"Исключение: {e}")