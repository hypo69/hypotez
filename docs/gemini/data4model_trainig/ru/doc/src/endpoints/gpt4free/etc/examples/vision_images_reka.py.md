# Модуль для работы с изображениями Reka

## Обзор

Модуль демонстрирует пример взаимодействия с моделью Reka для анализа изображений. Он использует библиотеку `g4f` для отправки запроса на анализ изображения и вывода результата в консоль.

## Подробней

Этот модуль является частью проекта `hypotez` и демонстрирует, как использовать модель Reka для анализа изображений. Для работы с модулем необходимо установить библиотеку `g4f` и иметь учетную запись на сайте chat.reka.ai с сохраненными cookies. Модуль загружает изображение, отправляет его в модель Reka и выводит ответ модели в консоль.

## Классы

В данном модуле классы не используются.

## Функции

### `create`

```python
completion = client.chat.completions.create(
    model = "reka-core",
    messages = [
        {
            "role": "user",
            "content": "What can you see in the image ?"
        }
    ],
    stream = True,
    image = open("docs/images/cat.jpeg", "rb") # open("path", "rb"), do not use .read(), etc. it must be a file object
)
```

**Назначение**: Отправляет запрос на анализ изображения в модель Reka и возвращает объект completion для потоковой обработки ответа.

**Параметры**:

-   `model` (str): Имя модели, используемой для анализа изображения ("reka-core").
-   `messages` (list): Список сообщений, содержащих запрос пользователя. В данном случае, запрос "What can you see in the image ?".
-   `stream` (bool): Флаг, указывающий, что ответ должен быть возвращен в потоковом режиме (`True`).
-   `image` (file object): Объект файла изображения, открытый в бинарном режиме чтения ("rb").

**Возвращает**:

-   `completion`: Объект completion, который позволяет итерироваться по ответу модели в потоковом режиме.

**Как работает функция**:

1.  Создается запрос к API модели Reka через метод `client.chat.completions.create`.
2.  В запросе указывается модель `reka-core`, сообщение с запросом пользователя и изображение для анализа.
3.  Параметр `stream=True` указывает, что ответ от модели будет возвращаться частями в режиме реального времени.
4.  Функция `open("docs/images/cat.jpeg", "rb")` открывает файл изображения, который будет отправлен в модель для анализа. Важно отметить, что необходимо передавать объект файла, а не содержимое файла, прочитанное с помощью `.read()`.

### Итерация по completion

```python
for message in completion:
    print(message.choices[0].delta.content or "")
```

**Назначение**: Итерируется по объекту `completion` и выводит содержимое ответа модели в консоль.

**Параметры**:

-   `message`: Каждый элемент в объекте `completion`, представляющий собой часть ответа модели.

**Как работает функция**:

1.  Цикл `for message in completion:` перебирает каждую часть ответа, полученную от модели Reka.
2.  `message.choices[0].delta.content` извлекает текст ответа из объекта сообщения.
3.  `or ""` используется для обработки случаев, когда `message.choices[0].delta.content` имеет значение `None`. В таких случаях выводится пустая строка.

## Переменные

-   `client`: Объект класса `Client` из библиотеки `g4f`, используемый для взаимодействия с API.
-   `completion`: Объект, возвращаемый методом `client.chat.completions.create`, содержащий информацию о завершении запроса.
-   `message`: Переменная цикла, содержащая отдельные части ответа от модели.

## Примеры

Пример использования модуля:

```python
from g4f.client import Client
from g4f.Provider import Reka

client = Client(
    provider = Reka # Optional if you set model name to reka-core
)

completion = client.chat.completions.create(
    model = "reka-core",
    messages = [
        {
            "role": "user",
            "content": "What can you see in the image ?"
        }
    ],
    stream = True,
    image = open("docs/images/cat.jpeg", "rb") # open("path", "rb"), do not use .read(), etc. it must be a file object
)

for message in completion:
    print(message.choices[0].delta.content or "")

# >>> In the image there is ...
```

В этом примере предполагается, что в каталоге `docs/images/` есть файл `cat.jpeg`.