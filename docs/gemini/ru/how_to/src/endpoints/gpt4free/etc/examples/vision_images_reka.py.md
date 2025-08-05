## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода реализует функциональность взаимодействия с моделью `reka-core` через API `gpt4free` для анализа изображения. 

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: 
    - `g4f.client`:  Предоставляет API клиента для взаимодействия с различными моделями.
    - `g4f.Provider`:  Определяет провайдера модели (в данном случае `Reka`).
2. **Инициализация клиента**:  
    - Создается клиент `Client` с указанием провайдера `Reka`.
3. **Создание запроса**: 
    -  Используется метод `chat.completions.create` для создания запроса к модели `reka-core`.
    -  В запросе передаются:
        -  `model = "reka-core"`: Указывает модель, к которой обращается запрос.
        -  `messages = [...]`:  Список сообщений, которые включают:
            -  `role = "user"`: Определяет роль пользователя.
            -  `content = "What can you see in the image ?"`: Текст запроса к модели.
        -  `stream = True`:  Включает потоковый режим ответа от модели.
        -  `image = open("docs/images/cat.jpeg", "rb")`:  Загружает изображение из файла `docs/images/cat.jpeg` в бинарном режиме (`"rb"`).
4. **Обработка ответа**:
    -  Цикл `for message in completion:` итеративно обрабатывает ответ от модели.
    -  `print(message.choices[0].delta.content or "")`:  Выводит текст ответа модели.

Пример использования
-------------------------

```python
# Image Chat with Reca
# !! YOU NEED COOKIES / BE LOGGED IN TO chat.reka.ai
# download an image and save it as test.png in the same folder

from g4f.client import Client
from g4f.Provider import Reka

client = Client(
    provider=Reka # Optional if you set model name to reka-core
)

completion = client.chat.completions.create(
    model="reka-core",
    messages=[
        {
            "role": "user",
            "content": "What can you see in the image ?"
        }
    ],
    stream=True,
    image=open("docs/images/cat.jpeg", "rb") # open("path", "rb"), do not use .read(), etc. it must be a file object
)

for message in completion:
    print(message.choices[0].delta.content or "")

    # >>> In the image there is ...
```

**Дополнительные комментарии**:
- Данный код предполагает, что пользователь уже авторизован на сайте `chat.reka.ai` и имеет необходимые cookie-файлы.
- Изображение `test.png` должно находиться в той же папке, что и код.
- Код использует потоковый режим (`stream=True`) для получения ответа от модели, что позволяет выводить текст ответа по мере его формирования.