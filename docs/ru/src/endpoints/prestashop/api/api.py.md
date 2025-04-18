# Модуль для взаимодействия с PrestaShop API

## Обзор

Этот модуль предоставляет класс `PrestaShop` для взаимодействия с PrestaShop webservice API, используя JSON и XML для форматирования сообщений. Он поддерживает CRUD операции, поиск, и загрузку изображений, с обработкой ошибок для ответов.

## Подробнее

Модуль предназначен для упрощения интеграции с PrestaShop API. Он предоставляет удобный интерфейс для выполнения различных операций, таких как создание, чтение, обновление и удаление данных, а также поиск и загрузка изображений. Модуль поддерживает как JSON, так и XML форматы данных, что позволяет гибко взаимодействовать с API PrestaShop.

## Классы

### `Config`

**Описание**: Класс конфигурации для PrestaShop API.

**Принцип работы**:
Класс `Config` предназначен для хранения и управления конфигурационными параметрами, необходимыми для взаимодействия с PrestaShop API. Он определяет такие параметры, как язык, версия PrestaShop, режим работы (разработка или продакшн), формат данных, домен API и ключ API. Конфигурация может быть загружена из переменных окружения или задана статически в классе. В зависимости от режима работы (`MODE`), класс выбирает соответствующие учетные данные для доступа к API PrestaShop.

**Атрибуты**:
- `language` (str): Язык.
- `ps_version` (str): Версия PrestaShop (по умолчанию '').
- `MODE` (str): Определяет конечную точку API ('dev', 'dev8', 'prod').
- `POST_FORMAT` (str): Формат данных для POST запросов (по умолчанию 'XML').
- `API_DOMAIN` (str): Домен API.
- `API_KEY` (str): Ключ API.

### `PrestaShop`

**Описание**: Класс для взаимодействия с PrestaShop webservice API, использующий JSON и XML для сообщений.

**Принцип работы**:
Класс `PrestaShop` предоставляет методы для взаимодействия с PrestaShop API. Он позволяет выполнять CRUD операции, искать данные, загружать изображения и обрабатывать ошибки. Класс поддерживает как JSON, так и XML форматы данных. При инициализации класса проверяется соединение с API и определяется версия PrestaShop.

**Аттрибуты**:
- `client` (Session): Сессия для выполнения HTTP запросов.
- `debug` (bool): Флаг отладки (по умолчанию `False`).
- `language` (Optional[int]): ID языка (по умолчанию `None`).
- `data_format` (str): Формат данных ('JSON' или 'XML') (по умолчанию 'JSON').
- `ps_version` (str): Версия PrestaShop.
- `api_domain` (str): Домен API.
- `api_key` (str): Ключ API.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaShop`.
- `ping`: Проверяет работоспособность веб-сервиса.
- `_check_response`: Проверяет статус ответа и обрабатывает ошибки.
- `_parse_response_error`: Разбирает ответ об ошибке от PrestaShop API.
- `_prepare_url`: Подготавливает URL для запроса.
- `_exec`: Выполняет HTTP запрос к PrestaShop API.
- `_parse_response`: Преобразует XML или JSON ответ от API в структуру dict.
- `create`: Создает новый ресурс в PrestaShop API.
- `read`: Читает ресурс из PrestaShop API.
- `write`: Обновляет существующий ресурс в PrestaShop API.
- `unlink`: Удаляет ресурс из PrestaShop API.
- `search`: Ищет ресурсы в PrestaShop API.
- `create_binary`: Загружает бинарный файл в ресурс PrestaShop API.
- `get_schema`: Получает схему данного ресурса из PrestaShop API.
- `get_data`: Получает данные из ресурса PrestaShop API и сохраняет их.
- `get_apis`: Получает список всех доступных API.
- `upload_image_async`: Асинхронно загружает изображение в PrestaShop API.
- `upload_image_from_url`: Загружает изображение в PrestaShop API.
- `get_product_images`: Получает изображения для продукта.

## Функции

### `main`

```python
def main() -> None:
    """Проверка сущностей Prestashop"""
```

**Назначение**: Функция `main` предназначена для проверки функциональности взаимодействия с PrestaShop API.

**Как работает функция**:

1.  **Определение данных**: Функция начинает с определения словаря `data`, который содержит информацию о налоге (`tax`). Этот словарь включает ставку налога (`rate`), статус активности (`active`) и название налога (`name`) на разных языках.
2.  **Создание экземпляра `PrestaShop`**: Создается экземпляр класса `PrestaShop` с использованием параметров конфигурации, определенных в классе `Config`. Эти параметры включают домен API, ключ API, язык по умолчанию и формат данных.
3.  **Вызов методов API**: Затем функция вызывает методы `api.create` и `api.write` для создания и записи данных о налоге в PrestaShop.
4.  **Логирование**: В случае возникновения ошибок в процессе выполнения HTTP запросов к PrestaShop API, ошибки будут залогированы с использованием модуля `logger` из `src.logger.logger`.

```
    Определение данных о налоге
    │
    Создание экземпляра PrestaShop
    │
    Вызов api.create('taxes', data)
    │
    Вызов api.write('taxes', data)
```

**Примеры**:

```python
data = {
    'tax': {
        'rate': 3.000,
        'active': '1',
        'name': {
            'language': {
                'attrs': {'id': '1'},
                'value': '3% tax',
            }
        },
    }
}
api = PrestaShop(
    api_domain=Config.API_DOMAIN,
    api_key=Config.API_KEY,
    default_lang=1,
    debug=True,
    data_format=Config.POST_FORMAT,
)
api.create('taxes', data)
api.write('taxes', data)