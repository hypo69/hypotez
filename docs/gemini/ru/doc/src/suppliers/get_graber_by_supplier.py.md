# Модуль для получения граббера на основе URL поставщика

## Обзор

Модуль предоставляет функциональность для получения соответствующего объекта граббера для заданного URL-адреса поставщика. У каждого поставщика есть свой собственный граббер, который извлекает значения полей из целевой HTML-страницы.

## Подробнее

Этот модуль содержит функции для определения граббера, соответствующего URL-адресу поставщика, и возврата экземпляра этого граббера. Это позволяет использовать специализированные методы извлечения данных для различных поставщиков.

## Функции

### `get_graber_by_supplier_url`

```python
def get_graber_by_supplier_url(driver: 'Driver', url: str, lang_index:int ) -> Graber | None:
    """
    Функция, которая возвращает соответствующий граббер для заданного URL-адреса поставщика.

    У каждого поставщика есть свой граббер, который извлекает значения полей из целевой HTML-страницы.

    Args:
        driver ('Driver'): Инстанс веб-драйвера для управления браузером.
        url (str): URL-адрес страницы поставщика.
        lang_index (int): Указывает индекс языка в магазине Prestashop

    Returns:
        Graber | None: Инстанс граббера, если он найден, иначе None.
    """
    driver.get_url(url)
    if url.startswith(('https://aliexpress.com', 'https://wwww.aliexpress.com')):\
        # Если URL начинается с aliexpress.com, функция возвращает граббер AliexpressGraber
        return AliexpressGraber(driver,lang_index)

    if url.startswith(('https://amazon.com', 'https://wwww.amazon.com')):\
        # Если URL начинается с amazon.com, функция возвращает граббер AmazonGraber
        return AmazonGraber(driver,lang_index)

    if url.startswith(('https://bangood.com', 'https://wwww.bangood.com')):\
        # Если URL начинается с bangood.com, функция возвращает граббер BangoodGraber
        return BangoodGraber(driver,lang_index)

    if url.startswith(('https://cdata.co.il', 'https://wwww.cdata.co.il')):\
        # Если URL начинается с cdata.co.il, функция возвращает граббер CdataGraber
        return CdataGraber(driver,lang_index)

    if url.startswith(('https://ebay.', 'https://wwww.ebay.')):\
        # Если URL начинается с ebay., функция возвращает граббер EbayGraber
        return EbayGraber(driver,lang_index)

    if url.startswith(('https://etzmaleh.co.il','https://www.etzmaleh.co.il')):\
        # Если URL начинается с etzmaleh.co.il, функция возвращает граббер EtzmalehGraber
        return EtzmalehGraber(driver,lang_index)

    if url.startswith(('https://gearbest.com', 'https://wwww.gearbest.com')):\
        # Если URL начинается с gearbest.com, функция возвращает граббер GearbestGraber
        return GearbestGraber(driver,lang_index)

    if url.startswith(('https://grandadvance.co.il', 'https://www.grandadvance.co.il')):\
        # Если URL начинается с grandadvance.co.il, функция возвращает граббер GrandadvanceGraber
        return GrandadvanceGraber(driver,lang_index)

    if url.startswith(('https://hb-digital.co.il', 'https://www.hb-digital.co.il')):\
        # Если URL начинается с hb-digital.co.il, функция возвращает граббер HBGraber
        return HBGraber(driver,lang_index)

    if url.startswith(('https://ivory.co.il', 'https://www.ivory.co.il')):\
        # Если URL начинается с ivory.co.il, функция возвращает граббер IvoryGraber
        return IvoryGraber(driver,lang_index)

    if url.startswith(('https://ksp.co.il', 'https://www.ksp.co.il')):\
        # Если URL начинается с ksp.co.il, функция возвращает граббер KspGraber
        return KspGraber(driver,lang_index)

    if url.startswith(('https://kualastyle.com', 'https://www.kualastyle.com')):\
        # Если URL начинается с kualastyle.com, функция возвращает граббер KualaStyleGraber
        return KualaStyleGraber(driver,lang_index)

    if url.startswith(('https://morlevi.co.il', 'https://www.morlevi.co.il')):\
        # Если URL начинается с morlevi.co.il, функция возвращает граббер MorleviGraber
        return MorleviGraber(driver,lang_index)

    if url.startswith(('https://www.visualdg.com', 'https://visualdg.com')):\
        # Если URL начинается с visualdg.com, функция возвращает граббер VisualDGGraber
        return VisualDGGraber(driver,lang_index)

    if url.startswith(('https://wallashop.co.il', 'https://www.wallashop.co.il')):\
        # Если URL начинается с wallashop.co.il, функция возвращает граббер WallaShopGraber
        return WallaShopGraber(driver,lang_index)

    if url.startswith(('https://www.wallmart.com', 'https://wallmart.com')):\
        # Если URL начинается с wallmart.com, функция возвращает граббер WallmartGraber
        return WallmartGraber(driver,lang_index)

    logger.debug(f'No graber found for URL: {url}')
    ...\
    # Если URL не соответствует ни одному из известных поставщиков, функция логирует отладочное сообщение и возвращает None
    return

### `get_graber_by_supplier_prefix`

```python
def get_graber_by_supplier_prefix(driver: 'Driver', supplier_prefix: str, lang_index:str = '2' ) -> Optional[Graber] | bool:
    """
    Функция возвращает граббер по префиксу поставщика

    Args:
        driver ('Driver'): Инстанс веб-драйвера для управления браузером.
        supplier_prefix (str): Префикс поставщика
        lang_index (str): Индекс языка

    Returns:
        Optional[Graber] | bool:  Возвращает граббер или False
    """
    ...\
    if supplier_prefix == 'aliexpress':\
        # Если префикс поставщика "aliexpress", то создается экземпляр граббера AliexpressGraber
        grabber = AliexpressGraber(driver,lang_index)
    if supplier_prefix == 'amazon':\
        # Если префикс поставщика "amazon", то создается экземпляр граббера AmazonGraber
        grabber = AmazonGraber(driver,lang_index)
    if supplier_prefix == 'ebay':\
        # Если префикс поставщика "ebay", то создается экземпляр граббера EbayGraber
        grabber = EbayGraber(driver,lang_index)
    if supplier_prefix == 'gearbest':\
        # Если префикс поставщика "gearbest", то создается экземпляр граббера GearbestGraber
        grabber = GearbestGraber(driver,lang_index)
    if supplier_prefix == 'grandadvance':\
        # Если префикс поставщика "grandadvance", то создается экземпляр граббера GrandadvanceGraber
        grabber = GrandadvanceGraber(driver,lang_index)
    if supplier_prefix == 'hb':\
        # Если префикс поставщика "hb", то создается экземпляр граббера HBGraber
        grabber = HBGraber(driver,lang_index)
    if supplier_prefix == 'ivory':\
        # Если префикс поставщика "ivory", то создается экземпляр граббера IvoryGraber
        grabber = IvoryGraber(driver,lang_index)
    if supplier_prefix == 'ksp':\
        # Если префикс поставщика "ksp", то создается экземпляр граббера KspGraber
        grabber = KspGraber(driver,lang_index)
    if supplier_prefix == 'kualastyle':\
        # Если префикс поставщика "kualastyle", то создается экземпляр граббера KualaStyleGraber
        grabber = KualaStyleGraber(driver,lang_index)
    if supplier_prefix == 'morlevi':\
        # Если префикс поставщика "morlevi", то создается экземпляр граббера MorleviGraber
        grabber = MorleviGraber(driver,lang_index)
    if supplier_prefix == 'visualdg':\
        # Если префикс поставщика "visualdg", то создается экземпляр граббера VisualDGGraber
        grabber = VisualDGGraber(driver,lang_index)
    if supplier_prefix == 'wallashop':\
        # Если префикс поставщика "wallashop", то создается экземпляр граббера WallaShopGraber
        grabber = WallaShopGraber(driver,lang_index)
    if supplier_prefix == 'wallmart':\
        # Если префикс поставщика "wallmart", то создается экземпляр граббера WallmartGraber
        grabber = WallmartGraber(driver,lang_index)

    # Функция возвращает созданный экземпляр граббера или False, если ни один из префиксов не совпал
    return grabber or False