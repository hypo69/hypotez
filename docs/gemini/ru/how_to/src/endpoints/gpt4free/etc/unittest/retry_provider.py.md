## Как использовать `IterListProvider` 
=========================================================================================

Описание
-------------------------
Класс `IterListProvider`  -  провайдер, который предоставляет доступ к списку других провайдеров. 
Он итерирует по списку, пока не получит успешный результат. 
Провайдер может пропускать провайдеров, которые выдают исключения.

Шаги выполнения
-------------------------
1. Создайте экземпляр `IterListProvider`, передав ему список других провайдеров.
2. Передайте этот провайдер в качестве аргумента в `AsyncClient`.
3. Вызовите метод `client.chat.completions.create`, который вернет ответ от модели.
4. (Опционально) Используйте `stream=True` для получения ответа в виде потока.

Пример использования
-------------------------

```python
from g4f.client import AsyncClient
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldProviderMock, RaiseExceptionProviderMock

# Создайте список провайдеров, который включает как успешный, так и неуспешный провайдер
providers = [RaiseExceptionProviderMock, YieldProviderMock]

# Создайте экземпляр IterListProvider, передав ему список провайдеров
provider = IterListProvider(providers, False)

# Создайте экземпляр AsyncClient с использованием IterListProvider
client = AsyncClient(provider=provider)

# Вызовите метод client.chat.completions.create для получения ответа от модели
response = await client.chat.completions.create(DEFAULT_MESSAGES, "")

# Проверьте результат
self.assertIsInstance(response, ChatCompletion)
self.assertEqual("Hello", response.choices[0].message.content)
```

В данном примере `IterListProvider` попробует получить ответ от `RaiseExceptionProviderMock`, который выдает исключение. 
Затем он перейдет к следующему провайдеру, `YieldProviderMock`, который вернет успешный ответ.