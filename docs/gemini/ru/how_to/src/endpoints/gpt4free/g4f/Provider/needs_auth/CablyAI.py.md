## Как использовать класс `CablyAI`
=========================================================================================

Описание
-------------------------
Класс `CablyAI` предоставляет возможность использовать API CablyAI для взаимодействия с моделями искусственного интеллекта. 
Он наследует базовый класс `OpenaiTemplate` и реализует специфические для CablyAI методы и настройки.

Шаги выполнения
-------------------------
1. **Инициализация класса**:  Создайте объект класса `CablyAI`, который будет представлять ваше соединение с API CablyAI.
2. **Установка API ключа**:  Установите `api_key`, используя `api_key=your_api_key` при инициализации класса или через метод `set_api_key`.
3. **Создание асинхронного генератора**:  Используйте метод `create_async_generator` для получения асинхронного генератора, который будет генерировать ответы от модели.
4. **Взаимодействие с моделью**:  Используйте полученный генератор для отправки запросов к модели и получения ответов. 

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.CablyAI import CablyAI
from hypotez.src.endpoints.gpt4free.g4f.Messages import Messages

# Инициализация класса CablyAI
cably_ai = CablyAI(api_key="ваш_api_key")

# Создание асинхронного генератора
messages = Messages(
    user_messages=[
        {
            "role": "user",
            "content": "Привет, как дела?"
        }
    ]
)

async_generator = cably_ai.create_async_generator(
    model="gpt-3.5-turbo",  # Выберите модель
    messages=messages
)

# Получение ответа от модели
async for response in async_generator:
    print(response)
```

**Описание кода:**

-  `from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.CablyAI import CablyAI`: Импортирует класс `CablyAI` для работы с API CablyAI.
-  `from hypotez.src.endpoints.gpt4free.g4f.Messages import Messages`: Импортирует класс `Messages` для создания объекта с сообщениями.
-  `cably_ai = CablyAI(api_key="ваш_api_key")`:  Создает объект класса `CablyAI` с использованием вашего API ключа.
-  `messages = Messages(...)`: Создает объект `Messages` с заданным пользователем сообщением.
-  `async_generator = cably_ai.create_async_generator(...)`:  Создает асинхронный генератор для отправки запросов к модели.
-  `async for response in async_generator:`:  Использует цикл `async for` для получения ответов от модели.
-  `print(response)`: Выводит полученный ответ на экран.

**Дополнительные замечания**:

-  Класс `CablyAI` предоставляет ряд дополнительных функций, таких как поддержка потоковой передачи (streaming) и настройки заголовков запросов. 
-  Ознакомьтесь с документацией CablyAI для получения более подробной информации о доступных моделях и параметрах.