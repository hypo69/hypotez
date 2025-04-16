# Модуль для управления и обработки изображений в Emil Design

## Обзор

Модуль `src.endpoints.emil.emil_design` предназначен для управления и обработки изображений, а также для продвижения в Facebook и PrestaShop. Он относится к магазину `emil-design.com`.

## Подробней

Модуль предоставляет функциональность для описания изображений с использованием Gemini AI, загрузки описаний товаров в PrestaShop и продвижения товаров через Facebook.

## Классы

### `Config`

**Описание**: Класс конфигурации для `EmilDesign`.

**Атрибуты**:

*   `ENDPOINT` (str): Конечная точка API (значение: `'emil'`).
*   `MODE` (str): Определяет конечную точку API. Возможные значения:
    *   `'dev'` - `dev.emil_design.com` (PrestaShop 1.7)
    *   `'dev8'` - `dev8.emil_design.com` (PrestaShop 8)
    *   `'prod'` - `emil_design.com` (PrestaShop 1.7) - Внимание! Рабочий магазин!
*   `POST_FORMAT` (str): Формат данных для отправки (значение: `'XML'`).
*   `API_DOMAIN` (str): Домен API.
*   `API_KEY` (str): Ключ API.

**Принцип работы**:

Класс `Config` определяет параметры конфигурации для работы с API `emil-design.com`. Он использует переменные окружения, если `USE_ENV` установлен в `True`, иначе использует значения из базы данных паролей `keepass`. В зависимости от значения `MODE` устанавливаются различные домены и ключи API. Если `MODE` имеет невалидное значение, устанавливается режим `'dev'`.

### `EmilDesign`

**Описание**: Класс для разработки дизайна и продвижения изображений через различные платформы.

**Атрибуты**:

*   `gemini` (Optional[GoogleGenerativeAi]): Экземпляр класса `GoogleGenerativeAi` для работы с Gemini AI.
*   `openai` (Optional[OpenAIModel]): Экземпляр класса `OpenAIModel` для работы с OpenAI.
*   `base_path` (Path): Базовый путь к файлам модуля (значение: `gs.path.endpoints / Config.ENDPOINT`).
*   `config` (SimpleNamespace): Конфигурация, загруженная из JSON-файла (значение: `j_loads_ns(base_path / f'{Config.ENDPOINT}.json')`).
*   `data_path` (Path): Путь к данным (значение: `getattr(gs.path, config.storage, 'external_storage') / Config.ENDPOINT`).
*   `gemini_api` (str): Ключ API для Gemini (значение: `os.getenv('GEMINI_API') if USE_ENV else gs.credentials.gemini.emil`).
*   `presta_api` (str): Ключ API для PrestaShop (значение: `os.getenv('PRESTA_API') if USE_ENV else gs.credentials.presta.client.emil_design.api_key`).
*   `presta_domain` (str): Домен PrestaShop (значение: `os.getenv('PRESTA_URL') if USE_ENV else gs.credentials.presta.client.emil_design.api_domain`).

## Методы класса `EmilDesign`

### `describe_images`

```python
def describe_images(
    self,
    lang: str,
    models: dict = {
        'gemini': {'model_name': 'gemini-1.5-flash'},
        'openai': {'model_name': 'gpt-4o-mini', 'assistant_id': 'asst_uDr5aVY3qRByRwt5qFiMDk43'},
    },
) -> None:
```

**Назначение**: Описывает изображения на основе предоставленной инструкции и примеров.

**Параметры**:

*   `lang` (str): Язык для описания.
*   `models` (dict, optional): Конфигурация моделей. По умолчанию используются модели Gemini и OpenAI.

**Возвращает**:

*   `None`

**Вызывает исключения**:

*   `FileNotFoundError`: Если файлы инструкций не найдены.
*   `Exception`: Если возникает ошибка при обработке изображения.

**Как работает функция**:

1.  Функция читает системную инструкцию и подсказки из файлов Markdown, расположенных в каталоге `instructions`.
2.  Определяет список изображений для обработки, исключая те, которые уже описаны.
3.  Инициализирует модели Gemini и/или OpenAI, если это указано в параметрах.
4.  Для каждого изображения:
    *   Извлекает необработанные данные изображения.
    *   Запрашивает описание изображения у Gemini.
    *   Сохраняет описание изображения в JSON-файл.
    *   Обновляет список обработанных изображений.
5.  Выполняет задержку между запросами.

**Примеры**:

```python
from src.endpoints.emil.emil_design import EmilDesign

emil = EmilDesign()
emil.describe_images('he')
```

### `promote_to_facebook`

```python
async def promote_to_facebook(self) -> None:
```

**Назначение**: Продвигает изображения и их описания в Facebook.

**Параметры**:

*   `None`

**Возвращает**:

*   `None`

**Вызывает исключения**:

*   `Exception`: Если возникает ошибка при продвижении в Facebook.

**Как работает функция**:

1.  Функция создает экземпляр драйвера Chrome.
2.  Открывает страницу Facebook.
3.  Загружает описания изображений из JSON-файла.
4.  Для каждого описания изображения:
    *   Создает сообщение с заголовком и описанием.
    *   Публикует сообщение в Facebook.

**Примеры**:

```python
from src.endpoints.emil.emil_design import EmilDesign
import asyncio

emil = EmilDesign()
asyncio.run(emil.promote_to_facebook())
```

### `upload_described_products_to_prestashop`

```python
def upload_described_products_to_prestashop(
    self, products_list: Optional[List[SimpleNamespace]] = None, id_lang: Optional[int | str] = 2, *args, **kwards
) -> bool:
```

**Назначение**: Загружает информацию о товарах в PrestaShop.

**Параметры**:

*   `products_list` (Optional[List[SimpleNamespace]], optional): Список информации о товарах. По умолчанию `None`.
*   `id_lang` (Optional[int | str], optional): ID языка для базы данных PrestaShop. По умолчанию `2`.
*   Обычно языки назначаются в таком порядке: `1` - `en`, `2` - `he`, `3` - `ru`. Важно проверить порядок языков в целевой базе данных.

**Возвращает**:

*   `bool`: `True`, если загрузка прошла успешно, `False` в противном случае.

**Вызывает исключения**:

*   `FileNotFoundError`: Если файл локалей не найден.
*   `Exception`: Если возникает ошибка при загрузке в PrestaShop.

**Как работает функция**:

1.  Функция получает список файлов JSON из каталога данных.
2.  Загружает информацию о товарах из файлов JSON.
3.  Создает экземпляр класса `PrestaProduct`.
4.  Для каждого товара:
    *   Создает экземпляр класса `ProductFields` и устанавливает значения полей.
    *   Добавляет новый товар в PrestaShop.
5.  Возвращает `True`, если все товары успешно загружены.

**Примеры**:

```python
from src.endpoints.emil.emil_design import EmilDesign

emil = EmilDesign()
emil.upload_described_products_to_prestashop(id_lang=2)