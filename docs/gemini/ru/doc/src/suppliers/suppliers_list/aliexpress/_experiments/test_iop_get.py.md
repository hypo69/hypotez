# Модуль `test_iop_get`

## Обзор

Модуль `test_iop_get` представляет собой тестовый скрипт для взаимодействия с API AliExpress через библиотеку `iop`. 
Он демонстрирует базовые операции, такие как создание запроса, добавление параметров, отправка запроса и обработка ответа. 
Этот модуль является примером использования библиотеки `iop` для получения информации о товарах и других данных из API AliExpress.

## Подробней

В коде:

- **Инициализация клиента `iop`**: 
    - Используется библиотека `iop` для работы с API AliExpress. 
    - Создается объект `IopClient` с указанием URL API, AppKey и AppSecret.
- **Создание запроса**:
    - Создается объект `IopRequest` с заданным методом (GET в данном случае). 
- **Добавление параметров к запросу**: 
    - К запросу добавляются необходимые параметры (например, `promotion_link_type`, `source_values`, `tracking_id`).
- **Отправка запроса**: 
    - Отправляется запрос к API AliExpress с помощью метода `execute` объекта `IopClient`.
- **Обработка ответа**:
    - Получается ответ от API, который содержит информацию о результатах запроса.
    - Вывод информации о ответе:
        - Тело ответа (`response.body`).
        - Тип ответа (`response.type`).
        - Код ответа (`response.code`).
        - Сообщение об ошибке (`response.message`).
        - Уникальный идентификатор запроса (`response.request_id`).

## Классы

### `IopClient`

**Описание**:  Класс для взаимодействия с API AliExpress через библиотеку `iop`.

**Наследует**:  
    - `iop.IopClient` 

**Атрибуты**:
    - `url`: URL-адрес API AliExpress.
    - `appkey`:  AppKey для доступа к API.
    - `appSecret`: AppSecret для доступа к API.
    - `log_level`:  Уровень логирования (`iop.P_LOG_LEVEL_DEBUG` в данном случае, устанавливает детальное логирование).

**Методы**:
    - `execute(request: IopRequest, access_token: str = 'default')`: Отправка запроса к API AliExpress.
        - **Параметры**:
            - `request` (`IopRequest`):  Объект запроса к API.
            - `access_token` (`str`):  Токен доступа (по умолчанию 'default').
        - **Возвращает**:  `IopResponse`: Ответ от API AliExpress.

### `IopRequest`

**Описание**:  Класс для создания запросов к API AliExpress.

**Наследует**:  
    - `iop.IopRequest` 

**Атрибуты**:
    - `method`:  HTTP-метод запроса (по умолчанию `POST`). 
    - `source_values`:  Источник данных для запроса (например, URL товара).
    - `api_params`:  Словарь с параметрами запроса.

**Методы**:
    - `add_api_param(param_name: str, param_value: Any)`:  Добавление параметра к запросу.
        - **Параметры**:
            - `param_name`:  Название параметра.
            - `param_value`: Значение параметра.
    - `set_simplify()`:  Упрощение параметров запроса. 

## Функции

### `test_iop_get()`

**Назначение**:  Тестовая функция для демонстрации работы с API AliExpress через библиотеку `iop`.

**Параметры**:
    - Нет.

**Возвращает**: 
    - Нет.

**Как работает функция**:

- **Инициализация клиента**: 
    - Создается объект `IopClient` с указанием URL API, AppKey и AppSecret.
- **Создание запроса**: 
    - Создается объект `IopRequest` с заданным методом `GET`. 
- **Добавление параметров**:
    - Добавляются параметры `promotion_link_type`, `source_values`, `tracking_id` к запросу.
- **Отправка запроса**: 
    - Отправляется запрос к API с помощью метода `execute` объекта `IopClient`.
- **Обработка ответа**:
    - Выводится информация о ответе: тело ответа, тип, код, сообщение об ошибке, уникальный идентификатор запроса.

**Примеры**: 

- **Пример 1**: 
    ```python
    # Инициализация клиента
    client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93eb26aabc391d187732af93')

    # Создание запроса
    request = iop.IopRequest('aliexpress.affiliate.link.generate')

    # Добавление параметров
    request.add_api_param('promotion_link_type', '0')
    request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
    request.add_api_param('tracking_id', 'default')

    # Отправка запроса
    response = client.execute(request)

    # Вывод информации о ответе
    print(response.body)
    print(response.type)
    print(response.code)
    print(response.message)
    print(response.request_id)
    ```

## Параметры класса

- `url`: URL-адрес API AliExpress.
- `appkey`:  AppKey для доступа к API.
- `appSecret`: AppSecret для доступа к API.
- `log_level`:  Уровень логирования (`iop.P_LOG_LEVEL_DEBUG` в данном случае, устанавливает детальное логирование).

## Примеры

- **Пример 1**: 
    ```python
    # Инициализация клиента
    client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93eb26aabc391d187732af93')

    # Создание запроса
    request = iop.IopRequest('aliexpress.affiliate.link.generate')

    # Добавление параметров
    request.add_api_param('promotion_link_type', '0')
    request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
    request.add_api_param('tracking_id', 'default')

    # Отправка запроса
    response = client.execute(request)

    # Вывод информации о ответе
    print(response.body)
    print(response.type)
    print(response.code)
    print(response.message)
    print(response.request_id)
    ```