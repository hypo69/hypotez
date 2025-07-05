# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль возвращает экземпляр pydoll вебдрайвера (Graber) для каждого конкретного поставщика

```rst
.. :module:: src.suppliers.get_pydoll_graber_by_supplier 
```
"""

from urllib.parse import urlparse
from typing import Optional

# --- Импорты Graber классов ---
# Убедитесь, что все эти импорты корректны и ведут к классам Graber
from src.suppliers.suppliers_list.ads_tec_iit_com.graber_via_pydoll import Graber as AdsTecIitComGraber
from src.suppliers.suppliers_list.aliexpress.graber_via_pydoll import Graber as AliexpressGraber
from src.suppliers.suppliers_list.amazon.graber_via_pydoll import Graber as AmazonGraber
from src.suppliers.suppliers_list.apple_com.graber_via_pydoll import Graber as AppleComGraber
from src.suppliers.suppliers_list.atlascopco_com.graber_via_pydoll import Graber as AtlascopcoComGraber
from src.suppliers.suppliers_list.bangood.graber_via_pydoll import Graber as BangoodGraber
from src.suppliers.suppliers_list.bucketmaster_com_cn.graber_via_pydoll import Graber as BucketmasterComCnGraber
from src.suppliers.suppliers_list.cdata.graber_via_pydoll import Graber as CdataGraber
from src.suppliers.suppliers_list.cisco_com.graber_via_pydoll import Graber as CiscoComGraber
from src.suppliers.suppliers_list.de_de_ring_com.graber_via_pydoll import Graber as DeDeRingComGraber
from src.suppliers.suppliers_list.de_hexcel_com.graber_via_pydoll import Graber as DeHexcelComGraber
from src.suppliers.suppliers_list.de_rs_online_com.graber_via_pydoll import Graber as DeRsOnlineComGraber
from src.suppliers.suppliers_list.denaliweld_com.graber_via_pydoll import Graber as DenaliweldComGraber
from src.suppliers.suppliers_list.dewesoft_com.graber_via_pydoll import Graber as DewesoftComGraber
from src.suppliers.suppliers_list.ebay.graber_via_pydoll import Graber as EbayGraber
from src.suppliers.suppliers_list.elektrometal_eu.graber_via_pydoll import Graber as ElektrometalEuGraber
from src.suppliers.suppliers_list.etzmaleh.graber_via_pydoll import Graber as EtzmalehGraber
from src.suppliers.suppliers_list.findernet_com.graber_via_pydoll import Graber as FindernetComGraber
from src.suppliers.suppliers_list.fresubin_com.graber_via_pydoll import Graber as FresubinComGraber
from src.suppliers.suppliers_list.gearbest.graber_via_pydoll import Graber as GearbestGraber
from src.suppliers.suppliers_list.generex_de.graber_via_pydoll import Graber as GenerexDeGraber
from src.suppliers.suppliers_list.georgin_com.graber_via_pydoll import Graber as GeorginComGraber
from src.suppliers.suppliers_list.german_micro_steppermotors_com.graber_via_pydoll import Graber as GermanMicroSteppermotorsComGraber
from src.suppliers.suppliers_list.grandadvance.graber_via_pydoll import Graber as GrandadvanceGraber
from src.suppliers.suppliers_list.hb.graber_via_pydoll import Graber as HbGraber
from src.suppliers.suppliers_list.imos3d_com.graber_via_pydoll import Graber as Imos3dComGraber
from src.suppliers.suppliers_list.induprogress_pl.graber_via_pydoll import Graber as InduprogressPlGraber
from src.suppliers.suppliers_list.industrierat_west_de.graber_via_pydoll import Graber as IndustrieratWestDeGraber
from src.suppliers.suppliers_list.it_alwsci_com.graber_via_pydoll import Graber as ItAlwsciComGraber
from src.suppliers.suppliers_list.it_defelsko_com.graber_via_pydoll import Graber as ItDefelskoComGraber
from src.suppliers.suppliers_list.it_jarvis_smart_com.graber_via_pydoll import Graber as ItJarvisSmartComGraber
from src.suppliers.suppliers_list.it_superb_heater_com.graber_via_pydoll import Graber as ItSuperbHeaterComGraber
from src.suppliers.suppliers_list.it_thermo_heater_com.graber_via_pydoll import Graber as ItThermoHeaterComGraber
from src.suppliers.suppliers_list.ivory.graber_via_pydoll import Graber as IvoryGraber
from src.suppliers.suppliers_list.janitza_com.graber_via_pydoll import Graber as JanitzaComGraber
from src.suppliers.suppliers_list.jungbluth_com.graber_via_pydoll import Graber as JungbluthComGraber
from src.suppliers.suppliers_list.ksp.graber_via_pydoll import Graber as KspGraber
from src.suppliers.suppliers_list.kualastyle.graber_via_pydoll import Graber as KualastyleGraber
from src.suppliers.suppliers_list.ledodm_com.graber_via_pydoll import Graber as LedodmComGraber
from src.suppliers.suppliers_list.leybold_com.graber_via_pydoll import Graber as LeyboldComGraber
from src.suppliers.suppliers_list.mecalux_it.graber_via_pydoll import Graber as MecaluxItGraber
from src.suppliers.suppliers_list.megatron_de.graber_via_pydoll import Graber as MegatronDeGraber
from src.suppliers.suppliers_list.megger_com.graber_via_pydoll import Graber as MeggerComGraber
from src.suppliers.suppliers_list.mococonnectors_com.graber_via_pydoll import Graber as MococonnectorsComGraber
from src.suppliers.suppliers_list.mordorintelligence_it.graber_via_pydoll import Graber as MordorintelligenceItGraber
from src.suppliers.suppliers_list.morlevi.graber_via_pydoll import Graber as MorleviGraber
from src.suppliers.suppliers_list.omnipod_com.graber_via_pydoll import Graber as OmnipodComGraber
from src.suppliers.suppliers_list.opel_de.graber_via_pydoll import Graber as OpelDeGraber
from src.suppliers.suppliers_list.pfannenberg_com.graber_via_pydoll import Graber as PfannenbergComGraber
from src.suppliers.suppliers_list.pl_dmgmori_com.graber_via_pydoll import Graber as PlDmgmoriComGraber
from src.suppliers.suppliers_list.plm_sw_siemens_com.graber_via_pydoll import Graber as PlmSwSiemensComGraber
from src.suppliers.suppliers_list.prebiel_pl.graber_via_pydoll import Graber as PrebielPlGraber
from src.suppliers.suppliers_list.prusa3d_com.graber_via_pydoll import Graber as Prusa3dComGraber
from src.suppliers.suppliers_list.ridgid_eu.graber_via_pydoll import Graber as RidgidEuGraber
from src.suppliers.suppliers_list.sensysmagnetometer_com.graber_via_pydoll import Graber as SensysmagnetometerComGraber
from src.suppliers.suppliers_list.shop_loxone_com.graber_via_pydoll import Graber as ShopLoxoneComGraber
from src.suppliers.suppliers_list.shop_scheppach_com.graber_via_pydoll import Graber as ShopScheppachComGraber
from src.suppliers.suppliers_list.sigmaaldrich_com.graber_via_pydoll import Graber as SigmaaldrichComGraber
from src.suppliers.suppliers_list.sphinxitalia_it.graber_via_pydoll import Graber as SphinxitaliaItGraber
from src.suppliers.suppliers_list.vidaxl_pl.graber_via_pydoll import Graber as VidaxlPlGraber
from src.suppliers.suppliers_list.visualdg.graber_via_pydoll import Graber as VisualdgGraber
from src.suppliers.suppliers_list.wallashop.graber_via_pydoll import Graber as WallashopGraber
from src.suppliers.suppliers_list.wallmart.graber_via_pydoll import Graber as WallmartGraber
from src.suppliers.suppliers_list.zebra_com.graber_via_pydoll import Graber as ZebraComGraber

# Импорт типа Page для аннотации типов
from pydoll.browser.page import Page 


# Словарь для соответствия доменов классам Graber
URL_PREFIX_MAP = {
    "ads-tec-iit.com":AdsTecIitComGraber,
    "aliexpress.com":AliexpressGraber,
    "amazon.com":AmazonGraber,
    "apple.com":AppleComGraber,
    "atlascopco.com":AtlascopcoComGraber,
    "bangood.com":BangoodGraber,
    "bucketmaster.com.cn":BucketmasterComCnGraber,
    "cdata.com":CdataGraber,
    "chat.openai.com":"chat_gpt", # Специальный случай, если нужно обрабатывать, но возвращает строку.
    "cisco.com":CiscoComGraber,
    "de.de-ring.com":DeDeRingComGraber,
    "de.hexcel.com":DeHexcelComGraber,
    "de.rs-online.com":DeRsOnlineComGraber,
    "denaliweld.com":DenaliweldComGraber,
    "dewesoft.com":DewesoftComGraber,
    "ebay.com":EbayGraber,
    "elektrometal.eu":ElektrometalEuGraber,
    "etzmaleh.com":EtzmalehGraber,
    "findernet.com":FindernetComGraber,
    "fresubin.com":FresubinComGraber,
    "gearbest.com":GearbestGraber,
    "generex.de":GenerexDeGraber,
    "georgin.com":GeorginComGraber,
    "german.micro-steppermotors.com":GermanMicroSteppermotorsComGraber,
    "grandadvance.co.il":GrandadvanceGraber,
    "hb.com":HbGraber,
    "imos3d.com":Imos3dComGraber,
    "induprogress.pl":InduprogressPlGraber,
    "industrierat-west.de":IndustrieratWestDeGraber,
    "it.alwsci.com":ItAlwsciComGraber,
    "it.defelsko.com":ItDefelskoComGraber,
    "it.jarvis-smart.com":ItJarvisSmartComGraber,
    "it.superb-heater.com":ItSuperbHeaterComGraber,
    "it.thermo-heater.com":ItThermoHeaterComGraber,
    "ivory.co.il":IvoryGraber,
    "janitza.com":JanitzaComGraber,
    "jungbluth.com":JungbluthComGraber,
    "ksp.co.il":KspGraber,
    "kualastyle.co.il":KualastyleGraber,
    "ledodm.com":LedodmComGraber,
    "leybold.com":LeyboldComGraber,
    "mecalux.it":MecaluxItGraber,
    "megatron.de":MegatronDeGraber,
    "megger.com":MeggerComGraber,
    "mococonnectors.com":MococonnectorsComGraber,
    "mordorintelligence.it":MordorintelligenceItGraber,
    "morlevi.co.il":MorleviGraber,
    "omnipod.com":OmnipodComGraber,
    "opel.de":OpelDeGraber,
    "pfannenberg.com":PfannenbergComGraber,
    "pl.dmgmori.com":PlDmgmoriComGraber,
    "plm.sw.siemens.com":PlmSwSiemensComGraber,
    "prebiel.pl":PrebielPlGraber,
    "prusa3d.com":Prusa3dComGraber,
    "ridgid.eu":RidgidEuGraber,
    "sensysmagnetometer.com":SensysmagnetometerComGraber,
    "shop.loxone.com":ShopLoxoneComGraber,
    "shop.scheppach.com":ShopScheppachComGraber,
    "sigmaaldrich.com":SigmaaldrichComGraber,
    "sphinxitalia.it":SphinxitaliaItGraber,
    "vidaxl.pl":VidaxlPlGraber,
    "visualdg.co.il":VisualdgGraber,
    "wallashop.co.il":WallashopGraber,
    "wallmart.com":WallmartGraber,
    "zebra.com":ZebraComGraber,
}

SUPPLIER_PREFIX_MAP = {
    "ads_tec_iit_com": AdsTecIitComGraber,
    "aliexpress": AliexpressGraber,
    "amazon": AmazonGraber,
    "apple_com": AppleComGraber,
    "atlascopco_com": AtlascopcoComGraber,
    "bangood": BangoodGraber,
    "bucketmaster_com_cn": BucketmasterComCnGraber,
    "cdata": CdataGraber,
    "cisco_com": CiscoComGraber,
    "de_de_ring_com": DeDeRingComGraber,
    "de_hexcel_com": DeHexcelComGraber,
    "de_rs_online_com": DeRsOnlineComGraber,
    "denaliweld_com": DenaliweldComGraber,
    "dewesoft_com": DewesoftComGraber,
    "ebay": EbayGraber,
    "elektrometal_eu": ElektrometalEuGraber,
    "etzmaleh": EtzmalehGraber,
    "findernet_com": FindernetComGraber,
    "fresubin_com": FresubinComGraber,
    "gearbest": GearbestGraber,
    "generex_de": GenerexDeGraber,
    "georgin_com": GeorginComGraber,
    "german_micro_steppermotors_com": GermanMicroSteppermotorsComGraber,
    "grandadvance": GrandadvanceGraber,
    "hb": HbGraber,
    "imos3d_com": Imos3dComGraber,
    "induprogress_pl": InduprogressPlGraber,
    "industrierat_west_de": IndustrieratWestDeGraber,
    "it_alwsci_com": ItAlwsciComGraber,
    "it_defelsko_com": ItDefelskoComGraber,
    "it_jarvis_smart_com": ItJarvisSmartComGraber,
    "it_superb_heater_com": ItSuperbHeaterComGraber,
    "it_thermo_heater_com": ItThermoHeaterComGraber,
    "ivory": IvoryGraber,
    "janitza_com": JanitzaComGraber,
    "jungbluth_com": JungbluthComGraber,
    "ksp": KspGraber,
    "kualastyle": KualastyleGraber,
    "ledodm_com": LedodmComGraber,
    "leybold_com": LeyboldComGraber,
    "mecalux_it": MecaluxItGraber,
    "megatron_de": MegatronDeGraber,
    "megger_com": MeggerComGraber,
    "mococonnectors_com": MococonnectorsComGraber,
    "mordorintelligence_it": MordorintelligenceItGraber,
    "morlevi": MorleviGraber,
    "omnipod_com": OmnipodComGraber,
    "opel_de": OpelDeGraber,
    "pfannenberg_com": PfannenbergComGraber,
    "pl_dmgmori_com": PlDmgmoriComGraber,
    "plm_sw_siemens_com": PlmSwSiemensComGraber,
    "prebiel_pl": PrebielPlGraber,
    "prusa3d_com": Prusa3dComGraber,
    "ridgid_eu": RidgidEuGraber,
    "sensysmagnetometer_com": SensysmagnetometerComGraber,
    "shop_loxone_com": ShopLoxoneComGraber,
    "shop_scheppach_com": ShopScheppachComGraber,
    "sigmaaldrich_com": SigmaaldrichComGraber,
    "sphinxitalia_it": SphinxitaliaItGraber,
    "vidaxl_pl": VidaxlPlGraber,
    "visualdg": VisualdgGraber,
    "wallashop": WallashopGraber,
    "wallmart": WallmartGraber,
    "zebra_com": ZebraComGraber,
}


def get_graber_by_supplier_prefix(supplier_prefix: str, ) -> 'Graber':
    """
    Возвращает ЭКЗЕМПЛЯР Graber для данного ключа поставщика.

    :param supplier_prefix: ключ поставщика, например 'aliexpress'
    :param driver: Опциональный экземпляр Page для передачи в конструктор Graber.
    :return: экземпляр Graber
    :raises ValueError: если класс для поставщика не найден, или экземпляр не может быть создан.
    """
    # Преобразуем префикс, чтобы он соответствовал ключам в SUPPLIER_PREFIX_MAP
    supplier_alias: str = supplier_prefix.replace('.', '_').replace('-', '_')

    try:
        GraberClass = SUPPLIER_PREFIX_MAP[supplier_alias]
    except KeyError:
        # Попробуем найти по домену, если префикс не найден напрямую
        # (хотя это может быть избыточно, если supplier_prefix всегда должен быть в SUPPLIER_PREFIX_MAP)
        try:
            # Пытаемся использовать supplier_prefix напрямую как ключ, если он уже в формате домена
            GraberClass = URL_PREFIX_MAP[supplier_alias] 
        except KeyError:
            raise ValueError(f"Graber класс не найден для поставщика: {supplier_alias}")

    try:
        # Создаем экземпляр Graber, передавая supplier_prefix и драйвер.
        # Предполагается, что конструктор Graber принимает эти аргументы.
        graber_instance = GraberClass()
        return graber_instance
    except Exception as e:
        raise ValueError(f"Не удалось создать экземпляр Graber для {supplier_alias}: {e}") from e


def get_graber_by_supplier_url(url: str):
    """
    Извлекает домен из URL, находит соответствующий класс Graber и возвращает ЕГО ЭКЗЕМПЛЯР.

    Args:
        url (str): Входной URL или домен в любом формате.
        driver (Optional[Page]): Опциональный экземпляр Page для передачи в конструктор Graber.

    Returns:
        Graber: Экземпляр подходящего класса Graber.

    Raises:
        ValueError: Если URL недействителен, домен не может быть определен,
                    класс Graber не найден, или экземпляр Graber не может быть создан.
    """
    if not url.startswith(('http://', 'https://')):
        # Добавляем схему, если она отсутствует, для корректной работы urlparse
        url = 'http://' + url  

    parsed_url = urlparse(url)
    domain = parsed_url.netloc or parsed_url.path

    # Очищаем домен: удаляем порт и префикс 'www.'
    domain = domain.split(':')[0].replace('www.','')

    if not domain:
        raise ValueError(f"Не удалось извлечь домен из URL: {url}")

    # Получаем класс Graber по домену из URL_PREFIX_MAP
    try:
        GraberClass = URL_PREFIX_MAP[domain]
    except KeyError:
        raise ValueError(f"Graber класс не найден для поставщика (домен): {domain}")

    try:
        # Создаем экземпляр Graber, передавая ему supplier_prefix и опциональный драйвер.
        # Важно: предполагается, что конструктор Graber принимает supplier_prefix и driver.
        graber_instance = GraberClass()
        return graber_instance
    except Exception as ex:
        # Логируем ошибку создания экземпляра, чтобы было понятно, почему не удалось
        raise ValueError(f"Не удалось создать экземпляр Graber для домена {domain}:\n{ex}") from ex
