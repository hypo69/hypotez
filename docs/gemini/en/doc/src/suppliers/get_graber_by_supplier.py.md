# Модуль для получения грабера на основе URL поставщика

## Обзор

Модуль предоставляет функциональность для получения соответствующего объекта грабера для заданного URL поставщика. У каждого поставщика есть свой собственный грабер, который извлекает значения полей из целевой HTML-страницы.

## Более подробно

Этот модуль предназначен для определения подходящего грабера на основе URL поставщика. Он содержит функцию `get_graber_by_supplier_url`, которая принимает URL и возвращает соответствующий объект грабера. Модуль импортирует граберы для различных поставщиков, таких как Aliexpress, Amazon, Ebay и другие. Если для данного URL не найден соответствующий грабер, возвращается `None`, при этом фиксируется отладочное сообщение с использованием `logger.debug`.

## Функции

### `get_graber_by_supplier_url`

```python
def get_graber_by_supplier_url(driver: 'Driver', url: str, lang_index: int) -> Graber | None:
    """
    Функция, которая возвращает соответствующий грабер для заданного URL поставщика.

    У каждого поставщика есть свой грабер, который извлекает значения полей из целевой HTML-страницы.

    Args:
        driver (Driver): Экземпляр веб-драйвера, используемый для взаимодействия с веб-страницей.
        url (str): URL страницы поставщика.
        lang_index (int): Указывает индекс языка в магазине Prestashop

    Returns:
        Graber | None: Экземпляр Graber, если найдено соответствие, иначе None.
    """
    driver.get_url(url)
    if url.startswith(('https://aliexpress.com', 'https://wwww.aliexpress.com')):
        return AliexpressGraber(driver,lang_index)

    if url.startswith(('https://amazon.com', 'https://wwww.amazon.com')):
        return AmazonGraber(driver,lang_index)

    if url.startswith(('https://bangood.com', 'https://wwww.bangood.com')):
        return BangoodGraber(driver,lang_index)

    if url.startswith(('https://cdata.co.il', 'https://wwww.cdata.co.il')):
        return CdataGraber(driver,lang_index)

    if url.startswith(('https://ebay.', 'https://wwww.ebay.')):
        return EbayGraber(driver,lang_index)

    if url.startswith(('https://etzmaleh.co.il','https://www.etzmaleh.co.il')):
        return EtzmalehGraber(driver,lang_index)

    if url.startswith(('https://gearbest.com', 'https://wwww.gearbest.com')):
        return GearbestGraber(driver,lang_index)

    if url.startswith(('https://grandadvance.co.il', 'https://www.grandadvance.co.il')):
        return GrandadvanceGraber(driver,lang_index)

    if url.startswith(('https://hb-digital.co.il', 'https://www.hb-digital.co.il')):
        return HBGraber(driver,lang_index)

    if url.startswith(('https://ivory.co.il', 'https://www.ivory.co.il')):
        return IvoryGraber(driver,lang_index)

    if url.startswith(('https://ksp.co.il', 'https://www.ksp.co.il')):
        return KspGraber(driver,lang_index)

    if url.startswith(('https://kualastyle.com', 'https://www.kualastyle.com')):
        return KualaStyleGraber(driver,lang_index)

    if url.startswith(('https://morlevi.co.il', 'https://www.morlevi.co.il')):
        return MorleviGraber(driver,lang_index)

    if url.startswith(('https://www.visualdg.com', 'https://visualdg.com')):
        return VisualDGGraber(driver,lang_index)

    if url.startswith(('https://wallashop.co.il', 'https://www.wallashop.co.il')):
        return WallaShopGraber(driver,lang_index)

    if url.startswith(('https://www.wallmart.com', 'https://wallmart.com')):
        return WallmartGraber(driver,lang_index)

    logger.debug(f'No graber found for URL: {url}')
    ...
    return
```

**Описание работы**:

1.  Функция принимает URL страницы поставщика и индекс языка.
2.  Использует метод `startswith()` для проверки, соответствует ли URL известным префиксам URL поставщиков.
3.  Если URL соответствует префиксу, функция возвращает экземпляр соответствующего класса Graber, передавая ему драйвер и индекс языка.
4.  Если URL не соответствует ни одному из известных префиксов, в журнал записывается отладочное сообщение с использованием `logger.debug`, и функция возвращает `None`.

**Примеры**:

```python
from src.webdriver import Driver, Chrome
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url

# Создание экземпляра драйвера (пример с Chrome)
driver = Driver(Chrome)

# Пример вызова функции с URL Aliexpress
url = 'https://aliexpress.com/some/product'
graber = get_graber_by_supplier_url(driver, url, '2')
if graber:
    print(f'Нашли грабер: {graber.__class__.__name__}')
else:
    print('грабер для Aliexpress не найден')

# Пример вызова функции с URL Amazon
url = 'https://amazon.com/some/product'
graber = get_graber_by_supplier_url(driver, url, '2')
if graber:
    print(f'Нашли грабер: {graber.__class__.__name__}')
else:
    print('грабер для Amazon не найден')

# Пример вызова функции с неизвестным URL
url = 'https://unknown.com/some/product'
graber = get_graber_by_supplier_url(driver, url, '2')
if graber:
    print(f'Нашли грабер: {graber.__class__.__name__}')
else:
    print('грабер для unknown.com не найден')
```

### `get_graber_by_supplier_prefix`

```python
def get_graber_by_supplier_prefix(driver: 'Driver', supplier_prefix: str, lang_index:str = '2' ) -> Optional[Graber] | bool:
    """
    ...
    """
    ...

    if supplier_prefix == 'aliexpress':
        grabber = AliexpressGraber(driver,lang_index)
    if supplier_prefix == 'amazon':
        grabber = AmazonGraber(driver,lang_index)
    if supplier_prefix == 'ebay':
        grabber = EbayGraber(driver,lang_index)
    if supplier_prefix == 'gearbest':
        grabber = GearbestGraber(driver,lang_index)
    if supplier_prefix == 'grandadvance':
        grabber = GrandadvanceGraber(driver,lang_index)
    if supplier_prefix == 'hb':
        grabber = HBGraber(driver,lang_index)
    if supplier_prefix == 'ivory':
        grabber = IvoryGraber(driver,lang_index)
    if supplier_prefix == 'ksp':
        grabber = KspGraber(driver,lang_index)
    if supplier_prefix == 'kualastyle':
        grabber = KualaStyleGraber(driver,lang_index)
    if supplier_prefix == 'morlevi':
        grabber = MorleviGraber(driver,lang_index)
    if supplier_prefix == 'visualdg':
        grabber = VisualDGGraber(driver,lang_index)
    if supplier_prefix == 'wallashop':
        grabber = WallaShopGraber(driver,lang_index)
    if supplier_prefix == 'wallmart':
        grabber = WallmartGraber(driver,lang_index)

    return grabber or False
```

**Описание работы**:

1.  Функция принимает префикс поставщика, экземпляр веб-драйвера и индекс языка.
2.  В зависимости от префикса поставщика, функция создает экземпляр соответствующего класса Graber, передавая ему драйвер и индекс языка.
3.  Если префикс поставщика не соответствует ни одному из известных, функция вернет `False`.

**Примеры**:

```python
from src.webdriver import Driver, Chrome
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_prefix

# Создание экземпляра драйвера (пример с Chrome)
driver = Driver(Chrome)

# Пример вызова функции с префиксом Aliexpress
supplier_prefix = 'aliexpress'
graber = get_graber_by_supplier_prefix(driver, supplier_prefix, '2')
if graber:
    print(f'Нашли грабер: {graber.__class__.__name__}')
else:
    print('грабер для Aliexpress не найден')

# Пример вызова функции с префиксом Amazon
supplier_prefix = 'amazon'
graber = get_graber_by_supplier_prefix(driver, supplier_prefix, '2')
if graber:
    print(f'Нашли грабер: {graber.__class__.__name__}')
else:
    print('грабер для Amazon не найден')

# Пример вызова функции с неизвестным префиксом
supplier_prefix = 'unknown'
graber = get_graber_by_supplier_prefix(driver, supplier_prefix, '2')
if graber:
    print(f'Нашли грабер: {graber.__class__.__name__}')
else:
    print('грабер для unknown не найден')