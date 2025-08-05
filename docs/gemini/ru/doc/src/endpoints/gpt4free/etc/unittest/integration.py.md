# hypotez/src/endpoints/gpt4free/etc/unittest/integration.py

## Обзор

Модуль `integration.py`  содержит интеграционные тесты для проверки функциональности  класса `Client`  и  `AsyncClient`  из библиотеки `g4f`.  Тесты проверяют, что методы  `chat.completions.create`  могут успешно взаимодействовать с  провайдерами  `Copilot`  и  `DDG`  (Bing и OpenAI)  и  получить  ответ  в  формате  JSON. 

## Подробнее 

Модуль `integration.py` является  частью  проекта  `hypotez`.  Он  используется  для  проверки  работоспособности  библиотеки  `g4f`  и  обеспечивает  интеграцию  с  различными  AI-моделями  (Copilot  и  DDG).  

## Классы

### `TestProviderIntegration`

**Описание**:  Класс `TestProviderIntegration`  содержит  тесты  для  проверки  интеграции  с  разными  провайдерами  (Copilot  и  DDG).  Он  наследует  от  класса  `unittest.TestCase`.

**Атрибуты**:

 - **None**

**Методы**:

 - **`test_bing`**:  Функция  проверяет  работоспособность  интеграции  с  провайдером  `Copilot`.  В  тесте  создается  инстанс  класса  `Client`  с  провайдером  `Copilot`.  Далее  выполняется  метод  `chat.completions.create`,  который  отправляет  запрос  в  Bing.  Проверяется,  что  ответ  является  инстансом  класса  `ChatCompletion`  и  содержит  ключ  `success`  в  JSON-ответе.

 - **`test_openai`**:  Функция  проверяет  работоспособность  интеграции  с  провайдером  `DDG`.  В  тесте  создается  инстанс  класса  `Client`  с  провайдером  `DDG`.  Далее  выполняется  метод  `chat.completions.create`,  который  отправляет  запрос  в  OpenAI.  Проверяется,  что  ответ  является  инстансом  класса  `ChatCompletion`  и  содержит  ключ  `success`  в  JSON-ответе. 

### `TestChatCompletionAsync`

**Описание**:  Класс `TestChatCompletionAsync`  содержит  асинхронные  тесты  для  проверки  интеграции  с  разными  провайдерами  (Copilot  и  DDG).  Он  наследует  от  класса  `unittest.IsolatedAsyncioTestCase`.

**Атрибуты**:

 - **None**

**Методы**:

 - **`test_bing`**:  Функция  проверяет  работоспособность  асинхронной  интеграции  с  провайдером  `Copilot`.  В  тесте  создается  инстанс  класса  `AsyncClient`  с  провайдером  `Copilot`.  Далее  выполняется  метод  `chat.completions.create`,  который  отправляет  асинхронный  запрос  в  Bing.  Проверяется,  что  ответ  является  инстансом  класса  `ChatCompletion`  и  содержит  ключ  `success`  в  JSON-ответе.

 - **`test_openai`**:  Функция  проверяет  работоспособность  асинхронной  интеграции  с  провайдером  `DDG`.  В  тесте  создается  инстанс  класса  `AsyncClient`  с  провайдером  `DDG`.  Далее  выполняется  метод  `chat.completions.create`,  который  отправляет  асинхронный  запрос  в  OpenAI.  Проверяется,  что  ответ  является  инстансом  класса  `ChatCompletion`  и  содержит  ключ  `success`  в  JSON-ответе.

## Функции

### `test_bing`

**Описание**:  Функция  `test_bing`  проверяет  работоспособность  интеграции  с  провайдером  `Copilot`.  В  тесте  создается  инстанс  класса  `Client`  с  провайдером  `Copilot`.  Далее  выполняется  метод  `chat.completions.create`,  который  отправляет  запрос  в  Bing.  Проверяется,  что  ответ  является  инстансом  класса  `ChatCompletion`  и  содержит  ключ  `success`  в  JSON-ответе. 

**Параметры**:

 - **None**

**Возвращает**:

 - **None**

**Вызывает исключения**:

 - **None**

**Пример**:

```python
>>> client = Client(provider=Copilot)
>>> response = client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
>>> self.assertIsInstance(response, ChatCompletion)
>>> self.assertIn("success", json.loads(response.choices[0].message.content))
```

### `test_openai`

**Описание**:  Функция  `test_openai`  проверяет  работоспособность  интеграции  с  провайдером  `DDG`.  В  тесте  создается  инстанс  класса  `Client`  с  провайдером  `DDG`.  Далее  выполняется  метод  `chat.completions.create`,  который  отправляет  запрос  в  OpenAI.  Проверяется,  что  ответ  является  инстансом  класса  `ChatCompletion`  и  содержит  ключ  `success`  в  JSON-ответе. 

**Параметры**:

 - **None**

**Возвращает**:

 - **None**

**Вызывает исключения**:

 - **None**

**Пример**:

```python
>>> client = Client(provider=DDG)
>>> response = client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
>>> self.assertIsInstance(response, ChatCompletion)
>>> self.assertIn("success", json.loads(response.choices[0].message.content))
```

### `test_bing`

**Описание**:  Функция  `test_bing`  проверяет  работоспособность  асинхронной  интеграции  с  провайдером  `Copilot`.  В  тесте  создается  инстанс  класса  `AsyncClient`  с  провайдером  `Copilot`.  Далее  выполняется  метод  `chat.completions.create`,  который  отправляет  асинхронный  запрос  в  Bing.  Проверяется,  что  ответ  является  инстансом  класса  `ChatCompletion`  и  содержит  ключ  `success`  в  JSON-ответе. 

**Параметры**:

 - **None**

**Возвращает**:

 - **None**

**Вызывает исключения**:

 - **None**

**Пример**:

```python
>>> client = AsyncClient(provider=Copilot)
>>> response = await client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
>>> self.assertIsInstance(response, ChatCompletion)
>>> self.assertIn("success", json.loads(response.choices[0].message.content))
```

### `test_openai`

**Описание**:  Функция  `test_openai`  проверяет  работоспособность  асинхронной  интеграции  с  провайдером  `DDG`.  В  тесте  создается  инстанс  класса  `AsyncClient`  с  провайдером  `DDG`.  Далее  выполняется  метод  `chat.completions.create`,  который  отправляет  асинхронный  запрос  в  OpenAI.  Проверяется,  что  ответ  является  инстансом  класса  `ChatCompletion`  и  содержит  ключ  `success`  в  JSON-ответе. 

**Параметры**:

 - **None**

**Возвращает**:

 - **None**

**Вызывает исключения**:

 - **None**

**Пример**:

```python
>>> client = AsyncClient(provider=DDG)
>>> response = await client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
>>> self.assertIsInstance(response, ChatCompletion)
>>> self.assertIn("success", json.loads(response.choices[0].message.content))
```

## Параметры класса
 - **`DEFAULT_MESSAGES`**:  Список  сообщений  для  тестов.  Первый  элемент  -  системное  сообщение  с  инструкцией  отвечать  в  JSON-формате  с  примером  структуры  JSON-ответа.  Второй  элемент  -  запрос  пользователя  с  просьбой  вернуть  значение  `true`  в  ключе  `success`.

## Примеры 

```python
# Создание объекта класса TestProviderIntegration
>>> test = TestProviderIntegration()
# Вызов метода test_bing
>>> test.test_bing()
# Вызов метода test_openai
>>> test.test_openai()

# Создание объекта класса TestChatCompletionAsync
>>> test_async = TestChatCompletionAsync()
# Вызов метода test_bing
>>> test_async.test_bing()
# Вызов метода test_openai
>>> test_async.test_openai()