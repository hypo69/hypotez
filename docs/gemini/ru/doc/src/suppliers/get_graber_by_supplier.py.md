# Модуль для получения граббера по URL поставщика

## Обзор

Модуль предоставляет функциональность для получения соответствующего объекта граббера для заданного URL поставщика. У каждого поставщика есть свой собственный граббер, который извлекает значения полей из целевой HTML-страницы.

## Подробнее

Этот модуль содержит функции для определения граббера на основе URL или префикса поставщика. Он импортирует грабберы для различных поставщиков, таких как AliExpress, Amazon, eBay и другие, и возвращает соответствующий граббер в зависимости от URL или префикса.

## Классы

В данном модуле классы не определены.

## Функции

### `get_graber_by_supplier_url`

```python
def get_graber_by_supplier_url(driver: 'Driver', url: str, lang_index: int) -> Graber | None:
    """
    Функция возвращает соответствующий граббер для заданного URL поставщика.

    Каждый поставщик имеет свой собственный граббер, который извлекает значения полей из целевой HTML-страницы.

    Args:
        driver (Driver): Инстанс веб-драйвера.
        url (str): URL страницы поставщика.
        lang_index (int): Указывает индекс языка в магазине Prestashop

    Returns:
        Graber | None: Инстанс граббера, если соответствие найдено, иначе None.

    """
    driver.get_url(url)
    if url.startswith(('https://aliexpress.com', 'https://wwww.aliexpress.com')):\
        # Функция возвращает граббер AliexpressGraber, если URL начинается с указанных префиксов AliExpress.
        return AliexpressGraber(driver, lang_index)

    if url.startswith(('https://amazon.com', 'https://wwww.amazon.com')):\
        # Функция возвращает граббер AmazonGraber, если URL начинается с указанных префиксов Amazon.
        return AmazonGraber(driver, lang_index)

    if url.startswith(('https://bangood.com', 'https://wwww.bangood.com')):\
        # Функция возвращает граббер BangoodGraber, если URL начинается с указанных префиксов Bangood.
        return BangoodGraber(driver, lang_index)

    if url.startswith(('https://cdata.co.il', 'https://wwww.cdata.co.il')):\
        # Функция возвращает граббер CdataGraber, если URL начинается с указанных префиксов Cdata.
        return CdataGraber(driver, lang_index)

    if url.startswith(('https://ebay.', 'https://wwww.ebay.')):\
        # Функция возвращает граббер EbayGraber, если URL начинается с указанных префиксов eBay.
        return EbayGraber(driver, lang_index)

    if url.startswith(('https://etzmaleh.co.il','https://www.etzmaleh.co.il')):\
        # Функция возвращает граббер EtzmalehGraber, если URL начинается с указанных префиксов Etzmaleh.
        return EtzmalehGraber(driver, lang_index)

    if url.startswith(('https://gearbest.com', 'https://wwww.gearbest.com')):\
        # Функция возвращает граббер GearbestGraber, если URL начинается с указанных префиксов Gearbest.
        return GearbestGraber(driver, lang_index)

    if url.startswith(('https://grandadvance.co.il', 'https://www.grandadvance.co.il')):\
        # Функция возвращает граббер GrandadvanceGraber, если URL начинается с указанных префиксов Grandadvance.
        return GrandadvanceGraber(driver, lang_index)

    if url.startswith(('https://hb-digital.co.il', 'https://www.hb-digital.co.il')):\
        # Функция возвращает граббер HBGraber, если URL начинается с указанных префиксов HB.
        return HBGraber(driver, lang_index)

    if url.startswith(('https://ivory.co.il', 'https://www.ivory.co.il')):\
        # Функция возвращает граббер IvoryGraber, если URL начинается с указанных префиксов Ivory.
        return IvoryGraber(driver, lang_index)

    if url.startswith(('https://ksp.co.il', 'https://www.ksp.co.il')):\
        # Функция возвращает граббер KspGraber, если URL начинается с указанных префиксов KSP.
        return KspGraber(driver, lang_index)

    if url.startswith(('https://kualastyle.com', 'https://www.kualastyle.com')):\
        # Функция возвращает граббер KualaStyleGraber, если URL начинается с указанных префиксов KualaStyle.
        return KualaStyleGraber(driver, lang_index)

    if url.startswith(('https://morlevi.co.il', 'https://www.morlevi.co.il')):\
        # Функция возвращает граббер MorleviGraber, если URL начинается с указанных префиксов Morlevi.
        return MorleviGraber(driver, lang_index)

    if url.startswith(('https://www.visualdg.com', 'https://visualdg.com')):\
        # Функция возвращает граббер VisualDGGraber, если URL начинается с указанных префиксов VisualDG.
        return VisualDGGraber(driver, lang_index)

    if url.startswith(('https://wallashop.co.il', 'https://www.wallashop.co.il')):\
        # Функция возвращает граббер WallaShopGraber, если URL начинается с указанных префиксов WallaShop.
        return WallaShopGraber(driver, lang_index)

    if url.startswith(('https://www.wallmart.com', 'https://wallmart.com')):\
        # Функция возвращает граббер WallmartGraber, если URL начинается с указанных префиксов Wallmart.
        return WallmartGraber(driver, lang_index)

    logger.debug(f'No graber found for URL: {url}')
    ...\
    return
```

**Как работает функция**:

- Функция `get_graber_by_supplier_url` принимает URL страницы поставщика и пытается определить соответствующий граббер на основе начальных символов URL.
- Для каждого известного поставщика (AliExpress, Amazon, eBay и т.д.) функция проверяет, начинается ли URL с соответствующего префикса.
- Если соответствие найдено, функция возвращает экземпляр соответствующего класса граббера, передавая ему драйвер и индекс языка.
- Если ни один из префиксов не совпадает с URL, функция регистрирует отладочное сообщение в лог и возвращает `None`.

**Примеры**:

```python
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
from src.webdriver import Driver

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Пример 1: Получение граббера для AliExpress
url = 'https://aliexpress.com/item/1234567890.html'
graber = get_graber_by_supplier_url(driver, url, '2')
if graber:
    print(f'Нашли граббер: {graber.__class__.__name__}')
else:
    print('Граббер не найден')

# Пример 2: Получение граббера для Amazon
url = 'https://amazon.com/item/ABCDEFG'
graber = get_graber_by_supplier_url(driver, url, '2')
if graber:
    print(f'Нашли граббер: {graber.__class__.__name__}')
else:
    print('Граббер не найден')

# Пример 3: URL не соответствует ни одному из известных поставщиков
url = 'https://unknown-supplier.com/product/XYZ'
graber = get_graber_by_supplier_url(driver, url, '2')
if graber:
    print(f'Нашли граббер: {graber.__class__.__name__}')
else:
    print('Граббер не найден')
```

### `get_graber_by_supplier_prefix`

```python
def get_graber_by_supplier_prefix(driver: 'Driver', supplier_prefix: str, lang_index:str = '2' ) -> Optional[Graber] | bool:
    """
    
    Args:
        driver (Driver): Инстанс веб-драйвера.
        supplier_prefix (str): Префикс поставщика.
        lang_index (str, optional): Индекс языка. По умолчанию '2'.

    Returns:
        Optional[Graber] | bool: Инстанс граббера, если соответствие найдено, иначе False.
    """
    ...

    if supplier_prefix == 'aliexpress':
        # Функция возвращает граббер AliexpressGraber, если префикс поставщика 'aliexpress'.
        grabber = AliexpressGraber(driver,lang_index)
    if supplier_prefix == 'amazon':
        # Функция возвращает граббер AmazonGraber, если префикс поставщика 'amazon'.
        grabber = AmazonGraber(driver,lang_index)
    if supplier_prefix == 'ebay':
        # Функция возвращает граббер EbayGraber, если префикс поставщика 'ebay'.
        grabber = EbayGraber(driver,lang_index)
    if supplier_prefix == 'gearbest':
        # Функция возвращает граббер GearbestGraber, если префикс поставщика 'gearbest'.
        grabber = GearbestGraber(driver,lang_index)
    if supplier_prefix == 'grandadvance':
        # Функция возвращает граббер GrandadvanceGraber, если префикс поставщика 'grandadvance'.
        grabber = GrandadvanceGraber(driver,lang_index)
    if supplier_prefix == 'hb':
        # Функция возвращает граббер HBGraber, если префикс поставщика 'hb'.
        grabber = HBGraber(driver,lang_index)
    if supplier_prefix == 'ivory':
        # Функция возвращает граббер IvoryGraber, если префикс поставщика 'ivory'.
        grabber = IvoryGraber(driver,lang_index)
    if supplier_prefix == 'ksp':
        # Функция возвращает граббер KspGraber, если префикс поставщика 'ksp'.
        grabber = KspGraber(driver,lang_index)
    if supplier_prefix == 'kualastyle':
        # Функция возвращает граббер KualaStyleGraber, если префикс поставщика 'kualastyle'.
        grabber = KualaStyleGraber(driver,lang_index)
    if supplier_prefix == 'morlevi':
        # Функция возвращает граббер MorleviGraber, если префикс поставщика 'morlevi'.
        grabber = MorleviGraber(driver,lang_index)
    if supplier_prefix == 'visualdg':
        # Функция возвращает граббер VisualDGGraber, если префикс поставщика 'visualdg'.
        grabber = VisualDGGraber(driver,lang_index)
    if supplier_prefix == 'wallashop':
        # Функция возвращает граббер WallaShopGraber, если префикс поставщика 'wallashop'.
        grabber = WallaShopGraber(driver,lang_index)
    if supplier_prefix == 'wallmart':
        # Функция возвращает граббер WallmartGraber, если префикс поставщика 'wallmart'.
        grabber = WallmartGraber(driver,lang_index)

    return grabber or False
```

**Как работает функция**:

- Функция `get_graber_by_supplier_prefix` принимает префикс поставщика и пытается определить соответствующий граббер.
- Для каждого известного поставщика (AliExpress, Amazon, eBay и т.д.) функция проверяет, совпадает ли переданный префикс с известным значением.
- Если соответствие найдено, функция возвращает экземпляр соответствующего класса граббера, передавая ему драйвер и индекс языка.
- Если ни один из префиксов не совпадает, функция возвращает `False`.

**Примеры**:

```python
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_prefix
from src.webdriver import Driver

# Создание инстанса драйвера
driver = Driver(Chrome)

# Пример 1: Получение граббера для AliExpress по префиксу
supplier_prefix = 'aliexpress'
graber = get_graber_by_supplier_prefix(driver, supplier_prefix, '2')
if graber:
    print(f'Нашли граббер: {graber.__class__.__name__}')
else:
    print('Граббер не найден')

# Пример 2: Получение граббера для невалидного префикса
supplier_prefix = 'unknown'
graber = get_graber_by_supplier_prefix(driver, supplier_prefix, '2')
if graber:
    print(f'Нашли граббер: {graber.__class__.__name__}')
else:
    print('Граббер не найден')