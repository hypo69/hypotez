Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует, как использовать библиотеку `g4f` для взаимодействия с OpenAI Chat API через прокси и с механизмом повторных попыток. Код создает клиента, настраивает прокси для обхода географических ограничений OpenAI и отправляет запрос на генерацию ответа на сообщение пользователя.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются классы `Client` из `g4f.client` и `OpenaiChat`, `RetryProvider` из `g4f.Provider`.
2. **Настройка прокси**:
   - Создается словарь `proxies` с настройками HTTP и HTTPS прокси. **Важно**: замените `username:password@host:port` на реальные учетные данные и адрес вашего прокси-сервера, расположенного в стране, поддерживаемой OpenAI (например, США).
3. **Создание клиента**:
   - Инициализируется объект `Client` с указанием прокси и провайдера. В качестве провайдера используется `RetryProvider`, который обеспечивает повторные попытки отправки запроса через `OpenaiChat` в случае сбоя. Параметр `single_provider_retry=True` указывает на то, что повторные попытки должны выполняться только с использованием `OpenaiChat`, а `max_retries=5` устанавливает максимальное количество повторных попыток равным 5.
4. **Формирование сообщения**:
   - Создается список `messages`, содержащий одно сообщение с ролью `user` и текстом `Hello`.
5. **Отправка запроса**:
   - Вызывается метод `client.chat.completions.create` для отправки запроса в OpenAI Chat API. Указывается модель `gpt-3.5-turbo`, список сообщений `messages` и параметр `stream=True` для получения ответа в режиме потоковой передачи.
6. **Обработка ответа**:
   - В цикле `for message in response` перебираются полученные сообщения. Из каждого сообщения извлекается содержимое (`message.choices[0].delta.content`) и выводится на экран. Если содержимое отсутствует, выводится пустая строка.

Пример использования
-------------------------

```python
from g4f.client import Client
from g4f.Provider import OpenaiChat, RetryProvider

# compatible countries: https://pastebin.com/UK0gT9cn
client = Client(
    proxies = {
        'http': 'http://username:password@host:port', # MUST BE WORKING OPENAI COUNTRY PROXY ex: USA
        'https': 'http://username:password@host:port' # MUST BE WORKING OPENAI COUNTRY PROXY ex: USA
    },
    provider = RetryProvider([OpenaiChat],
                             single_provider_retry=True, max_retries=5)
)

messages = [
    {'role': 'user', 'content': 'Hello'}
]

response = client.chat.completions.create(model='gpt-3.5-turbo',
                                     messages=messages, 
                                     stream=True)

for message in response:
    print(message.choices[0].delta.content or "")
```