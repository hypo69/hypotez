# Документация модуля Facebook Promoter

## Обзор

Модуль **Facebook Promoter** автоматизирует процесс продвижения товаров и событий AliExpress в группах Facebook. Модуль отвечает за публикацию рекламных объявлений в Facebook, гарантируя, что категории и события продвигаются без дубликатов. Он использует WebDriver для автоматизации браузера, что позволяет эффективно управлять рекламными акциями.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для автоматизации маркетинговых кампаний в Facebook. Он позволяет продвигать товары и события из AliExpress в заданных группах, избегая повторных публикаций и поддерживая гибкую настройку параметров продвижения, таких как язык и валюта. Модуль использует веб-драйвер для эмуляции действий пользователя в браузере, что позволяет обходить ограничения API Facebook и эффективно публиковать контент.

## Содержание

1.  [Класс `FacebookPromoter`](#класс-facebookpromoter)
    *   [Метод `__init__`](#метод-__init__)
    *   [Метод `promote`](#метод-promote)
    *   [Метод `log_promotion_error`](#метод-log_promotion_error)
    *   [Метод `update_group_promotion_data`](#метод-update_group_promotion_data)
    *   [Метод `process_groups`](#метод-process_groups)
    *   [Метод `get_category_item`](#метод-get_category_item)
    *   [Метод `check_interval`](#метод-check_interval)
    *   [Метод `validate_group`](#метод-validate_group)
2.  [Использование](#использование)
3.  [Лицензия](#лицензия)

## Классы

### `FacebookPromoter`

**Описание**:
Этот класс управляет процессом продвижения товаров и событий AliExpress в группах Facebook.

**Принцип работы**:
Класс инициализируется с WebDriver, именем промоутера и путями к файлам с данными о группах. Он содержит методы для продвижения элементов (категорий или событий) в указанных группах Facebook, логирования ошибок и обновления данных о продвижении в группах. Класс также включает методы для проверки интервалов между продвижениями и валидации данных групп.

#### Методы

*   ##### `__init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False)`

    ```python
    def __init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False):
        """
        Инициализирует промоутер Facebook с необходимыми конфигурациями.

        Args:
            d (Driver): Экземпляр WebDriver для автоматизации.
            promoter (str): Имя промоутера (например, "aliexpress").
            group_file_paths (Optional[list[str | Path] | str | Path], optional): Пути к файлам данных группы. По умолчанию None.
            no_video (bool): Флаг для отключения видео в постах. По умолчанию False.
        """
    ```

    **Назначение**:
    Инициализирует экземпляр класса `FacebookPromoter`.

    **Параметры**:

    *   `d` (Driver): Экземпляр `Driver`, используемый для управления браузером.
    *   `promoter` (str): Имя промоутера, например, 'aliexpress'.
    *   `group_file_paths` (Optional[list[str | Path]  |  str  |  Path], optional): Путь к файлу или списку файлов, содержащих данные о группах Facebook. По умолчанию `None`.
    *   `no_video` (bool): Флаг, указывающий, следует ли отключать загрузку видео в постах. По умолчанию `False`.

    **Как работает функция**:

    1.  Сохраняет переданные параметры в атрибуты экземпляра класса для дальнейшего использования.
    2.  Инициализирует внутренние структуры данных для хранения информации о промоутере и группах.

    **Примеры**:

    ```python
    from src.webdriver.driver import Driver
    from pathlib import Path

    # Пример с использованием списка путей к файлам
    driver = Driver()
    promoter = FacebookPromoter(d=driver, promoter='aliexpress', group_file_paths=['group1.json', 'group2.json'], no_video=True)

    # Пример с использованием одного пути к файлу
    promoter = FacebookPromoter(d=driver, promoter='aliexpress', group_file_paths='group1.json')

    # Пример с использованием pathlib.Path
    path_to_file = Path('group1.json')
    promoter = FacebookPromoter(d=driver, promoter='aliexpress', group_file_paths=path_to_file)
    ```

*   ##### `promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool`

    ```python
    def promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool:
        """
        Продвигает категорию или событие в указанной группе Facebook.

        Args:
            group (SimpleNamespace): Данные группы.
            item (SimpleNamespace): Категория или событие для продвижения.
            is_event (bool): Указывает, является ли элемент событием.
            language (str): Язык для продвижения.
            currency (str): Валюта для продвижения.

        Returns:
            bool: Успешно ли прошло продвижение.
        """
    ```

    **Назначение**:
    Осуществляет продвижение товара или события в указанной группе Facebook.

    **Параметры**:

    *   `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook, в которой будет осуществляться продвижение.
    *   `item` (SimpleNamespace): Объект, содержащий информацию о товаре или событии, которое нужно продвигать.
    *   `is_event` (bool): Флаг, указывающий, является ли продвигаемый элемент событием. По умолчанию `False`.
    *   `language` (str): Язык, на котором будет осуществляться продвижение. По умолчанию `None`.
    *   `currency` (str): Валюта, используемая в продвижении. По умолчанию `None`.

    **Возвращает**:

    *   `bool`: `True`, если продвижение прошло успешно, и `False` в противном случае.

    **Как работает функция**:

    1.  Формирует описание для публикации на основе предоставленных данных о группе и элементе (товаре или событии).
    2.  Использует WebDriver для входа в Facebook и публикации сообщения в указанной группе.
    3.  Обрабатывает возможные ошибки, логирует их и возвращает соответствующий результат.

    **Примеры**:

    ```python
    from types import SimpleNamespace
    from src.webdriver.driver import Driver

    # Пример объекта группы
    group_data = SimpleNamespace(
        group_url='https://www.facebook.com/groups/testgroup',
        cookies=[{'name': 'cookie1', 'value': 'value1'}]
    )

    # Пример объекта товара
    item_data = SimpleNamespace(
        title='Test Product',
        price=99.99,
        image_url='https://example.com/image.jpg',
        product_url='https://example.com/product'
    )

    driver = Driver()
    promoter = FacebookPromoter(d=driver, promoter='aliexpress')

    # Вызов функции promote
    success = promoter.promote(group=group_data, item=item_data, language='en', currency='USD')
    if success:
        print('Promotion successful')
    else:
        print('Promotion failed')
    ```

*   ##### `log_promotion_error(self, is_event: bool, item_name: str)`

    ```python
    def log_promotion_error(self, is_event: bool, item_name: str):
        """
        Логирует ошибку, когда продвижение не удается.

        Args:
            is_event (bool): Указывает, является ли элемент событием.
            item_name (str): Имя элемента.
        """
    ```

    **Назначение**:
    Логирует информацию об ошибке, возникшей при попытке продвижения элемента (товара или события).

    **Параметры**:

    *   `is_event` (bool): Флаг, указывающий, является ли продвигаемый элемент событием.
    *   `item_name` (str): Имя элемента, при продвижении которого произошла ошибка.

    **Как работает функция**:

    1.  Формирует сообщение об ошибке, содержащее информацию о типе элемента (событие или товар) и его имени.
    2.  Записывает сообщение об ошибке в лог с использованием модуля `logger`.

    **Примеры**:

    ```python
    from src.webdriver.driver import Driver
    from src.logger import logger

    driver = Driver()
    promoter = FacebookPromoter(d=driver, promoter='aliexpress')

    # Пример логирования ошибки продвижения товара
    promoter.log_promotion_error(is_event=False, item_name='Test Product')

    # Пример логирования ошибки продвижения события
    promoter.log_promotion_error(is_event=True, item_name='Test Event')
    ```

*   ##### `update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False)`

    ```python
    def update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False):
        """
        Обновляет данные группы после продвижения, добавляя продвигаемый элемент в список продвинутых категорий или событий.

        Args:
            group (SimpleNamespace): Данные группы.
            item_name (str): Имя продвигаемого элемента.
            is_event (bool): Указывает, является ли элемент событием.
        """
    ```

    **Назначение**:
    Обновляет данные о группе после успешного продвижения элемента (товара или события), добавляя информацию о продвинутом элементе в список уже продвинутых элементов.

    **Параметры**:

    *   `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook, в которой было осуществлено продвижение.
    *   `item_name` (str): Имя продвинутого элемента (товара или события).
    *   `is_event` (bool): Флаг, указывающий, был ли продвинут элемент событием. По умолчанию `False`.

    **Как работает функция**:

    1.  Проверяет, является ли продвигаемый элемент событием или категорией.
    2.  Добавляет имя продвинутого элемента в соответствующий список (продвинутых событий или продвинутых категорий) в данных группы.
    3.  Обновляет данные группы в файле конфигурации.

    **Примеры**:

    ```python
    from types import SimpleNamespace
    from src.webdriver.driver import Driver

    # Пример данных группы
    group_data = SimpleNamespace(
        group_url='https://www.facebook.com/groups/testgroup',
        promoted_categories=[],
        promoted_events=[]
    )

    driver = Driver()
    promoter = FacebookPromoter(d=driver, promoter='aliexpress')

    # Пример обновления данных группы после продвижения товара
    promoter.update_group_promotion_data(group=group_data, item_name='Test Product', is_event=False)

    # Пример обновления данных группы после продвижения события
    promoter.update_group_promotion_data(group=group_data, item_name='Test Event', is_event=True)
    ```

*   ##### `process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None)`

    ```python
    def process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None):
        """
        Обрабатывает группы для текущей кампании или продвижения события.

        Args:
            campaign_name (str): Имя кампании.
            events (list[SimpleNamespace]): Список событий для продвижения.
            is_event (bool): Указывает, продвигать ли события или категории.
            group_file_paths (list[str]): Пути к файлам данных группы.
            group_categories_to_adv (list[str]): Категории для продвижения.
            language (str): Язык для продвижения.
            currency (str): Валюта для продвижения.
        """
    ```

    **Назначение**:
    Обрабатывает список групп Facebook для продвижения товаров или событий в рамках заданной кампании.

    **Параметры**:

    *   `campaign_name` (str): Имя кампании, в рамках которой происходит продвижение.
    *   `events` (list[SimpleNamespace]): Список объектов, представляющих события, которые необходимо продвигать.
    *   `is_event` (bool): Флаг, указывающий, следует ли продвигать события (`True`) или категории (`False`).
    *   `group_file_paths` (list[str]): Список путей к файлам, содержащим данные о группах Facebook.
    *   `group_categories_to_adv` (list[str]): Список категорий товаров, которые необходимо продвигать.
    *   `language` (str): Язык, на котором будет осуществляться продвижение.
    *   `currency` (str): Валюта, которая будет использоваться в продвижении.

    **Как работает функция**:

    1.  Загружает данные о группах Facebook из указанных файлов.
    2.  Для каждой группы проверяет, можно ли ее продвигать в данный момент (на основе интервалов между продвижениями).
    3.  Получает элемент (товар или событие) для продвижения.
    4.  Осуществляет продвижение элемента в группе.
    5.  Обновляет данные о продвижении в группе.

    **Примеры**:

    ```python
    from types import SimpleNamespace
    from src.webdriver.driver import Driver

    driver = Driver()
    promoter = FacebookPromoter(d=driver, promoter='aliexpress')

    # Пример данных события
    event_data = SimpleNamespace(
        title='Test Event',
        start_date='2024-01-01',
        end_date='2024-01-02',
        description='Join our test event!'
    )

    # Вызов функции process_groups для продвижения событий
    promoter.process_groups(
        campaign_name='Test Campaign',
        events=[event_data],
        is_event=True,
        group_file_paths=['groups.json'],
        language='en',
        currency='USD'
    )

    # Вызов функции process_groups для продвижения категорий
    promoter.process_groups(
        campaign_name='Test Campaign',
        group_file_paths=['groups.json'],
        group_categories_to_adv=['sales'],
        language='en',
        currency='USD'
    )
    ```

*   ##### `get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace`

    ```python
    def get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace:
        """
        Получает элемент категории для продвижения на основе кампании и промоутера.

        Args:
            campaign_name (str): Имя кампании.
            group (SimpleNamespace): Данные группы.
            language (str): Язык для продвижения.
            currency (str): Валюта для продвижения.

        Returns:
            SimpleNamespace: Элемент категории для продвижения.
        """
    ```

    **Назначение**:
    Извлекает информацию о товаре (элементе категории) для продвижения в заданной группе Facebook в рамках определенной кампании.

    **Параметры**:

    *   `campaign_name` (str): Имя кампании, в рамках которой происходит продвижение.
    *   `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook, в которой будет осуществляться продвижение.
    *   `language` (str): Язык, на котором будет осуществляться продвижение.
    *   `currency` (str): Валюта, которая будет использоваться в продвижении.

    **Возвращает**:

    *   `SimpleNamespace`: Объект, содержащий информацию о товаре (элементе категории), который будет продвигаться.

    **Как работает функция**:

    1.  Определяет, какого промоутера следует использовать (например, AliExpress).
    2.  Получает список товаров из заданной категории с использованием API промоутера.
    3.  Выбирает случайный товар из полученного списка.
    4.  Возвращает информацию о выбранном товаре в виде объекта `SimpleNamespace`.

    **Примеры**:

    ```python
    from types import SimpleNamespace
    from src.webdriver.driver import Driver

    driver = Driver()
    promoter = FacebookPromoter(d=driver, promoter='aliexpress')

    # Пример данных группы
    group_data = SimpleNamespace(
        group_url='https://www.facebook.com/groups/testgroup',
        promoted_categories=[],
        promoted_events=[]
    )

    # Вызов функции get_category_item
    item = promoter.get_category_item(
        campaign_name='Test Campaign',
        group=group_data,
        language='en',
        currency='USD'
    )

    if item:
        print(f'Item for promotion: {item.title}')
    else:
        print('No item found for promotion')
    ```

*   ##### `check_interval(self, group: SimpleNamespace) -> bool`

    ```python
    def check_interval(self, group: SimpleNamespace) -> bool:
        """
        Проверяет, прошло ли достаточно времени для повторного продвижения этой группы.

        Args:
            group (SimpleNamespace): Данные группы.

        Returns:
            bool: Может ли группа быть продвинута.
        """
    ```

    **Назначение**:
    Проверяет, прошло ли достаточно времени с момента последнего продвижения в заданной группе Facebook.

    **Параметры**:

    *   `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook, включая время последнего продвижения.

    **Возвращает**:

    *   `bool`: `True`, если прошло достаточно времени для повторного продвижения в группе, и `False` в противном случае.

    **Как работает функция**:

    1.  Получает интервал между продвижениями из данных группы.
    2.  Вычисляет время, прошедшее с момента последнего продвижения.
    3.  Сравнивает прошедшее время с установленным интервалом.
    4.  Возвращает `True`, если прошло достаточно времени, и `False` в противном случае.

    **Примеры**:

    ```python
    from types import SimpleNamespace
    from datetime import datetime, timedelta
    from src.webdriver.driver import Driver

    driver = Driver()
    promoter = FacebookPromoter(d=driver, promoter='aliexpress')

    # Пример данных группы (прошло меньше времени, чем интервал)
    group_data_recent = SimpleNamespace(
        group_url='https://www.facebook.com/groups/testgroup',
        last_promotion_time=datetime.now() - timedelta(hours=1),
        interval_between_promotions=2
    )

    # Пример данных группы (прошло больше времени, чем интервал)
    group_data_old = SimpleNamespace(
        group_url='https://www.facebook.com/groups/testgroup',
        last_promotion_time=datetime.now() - timedelta(hours=3),
        interval_between_promotions=2
    )

    # Проверка интервала для группы, которую можно продвигать
    can_promote_old = promoter.check_interval(group=group_data_old)
    print(f'Can promote group (old): {can_promote_old}')

    # Проверка интервала для группы, которую нельзя продвигать
    can_promote_recent = promoter.check_interval(group=group_data_recent)
    print(f'Can promote group (recent): {can_promote_recent}')
    ```

*   ##### `validate_group(self, group: SimpleNamespace) -> bool`

    ```python
    def validate_group(self, group: SimpleNamespace) -> bool:
        """
        Проверяет данные группы, чтобы убедиться, что у нее есть необходимые атрибуты.

        Args:
            group (SimpleNamespace): Данные группы.

        Returns:
            bool: Действительны ли данные группы.
        """
    ```

    **Назначение**:
    Проверяет, содержит ли объект группы Facebook все необходимые атрибуты для дальнейшей обработки и продвижения.

    **Параметры**:

    *   `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook.

    **Возвращает**:

    *   `bool`: `True`, если объект группы содержит все необходимые атрибуты, и `False` в противном случае.

    **Как работает функция**:

    1.  Проверяет наличие обязательных атрибутов, таких как `group_url` (URL группы), `cookies` (куки для авторизации), `interval_between_promotions` (интервал между продвижениями) и `promoted_categories` (список продвинутых категорий).
    2.  Возвращает `True`, если все обязательные атрибуты присутствуют, и `False` в противном случае.

    **Примеры**:

    ```python
    from types import SimpleNamespace
    from src.webdriver.driver import Driver

    driver = Driver()
    promoter = FacebookPromoter(d=driver, promoter='aliexpress')

    # Пример данных группы (все атрибуты присутствуют)
    group_data_valid = SimpleNamespace(
        group_url='https://www.facebook.com/groups/testgroup',
        cookies=[{'name': 'cookie1', 'value': 'value1'}],
        interval_between_promotions=2,
        promoted_categories=[]
    )

    # Пример данных группы (отсутствует атрибут cookies)
    group_data_invalid = SimpleNamespace(
        group_url='https://www.facebook.com/groups/testgroup',
        interval_between_promotions=2,
        promoted_categories=[]
    )

    # Проверка валидности данных группы (валидные данные)
    is_valid_valid = promoter.validate_group(group=group_data_valid)
    print(f'Is group data valid (valid): {is_valid_valid}')

    # Проверка валидности данных группы (невалидные данные)
    is_valid_invalid = promoter.validate_group(group=group_data_invalid)
    print(f'Is group data valid (invalid): {is_valid_invalid}')
    ```

## Использование

### Пример использования класса `FacebookPromoter`

```python
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.webdriver.driver import Driver
from src.utils.jjson import j_loads_ns

# Setup WebDriver instance (replace with actual WebDriver)
d = Driver()

# Create an instance of FacebookPromoter
promoter = FacebookPromoter(
    d=d,
    promoter="aliexpress",
    group_file_paths=["path/to/group/file1.json", "path/to/group/file2.json"]
)

# Start promoting products or events
promoter.process_groups(
    campaign_name="Campaign1",
    events=[],
    group_categories_to_adv=["sales"],
    language="en",
    currency="USD"
)
```

## Лицензия

Этот модуль является частью большого пакета **Facebook Promoter** и распространяется под лицензией MIT.