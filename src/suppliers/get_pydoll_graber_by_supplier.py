## \file /src/suppliers/get_pydoll_graber_by_supplier.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль возвращает класс pydoll вебдрайвера  для каждого конкретного поставщика

```rst
.. :module:: src.suppliers.get_pydoll_graber_by_supplier 
```
"""

# get_graber_by_supplier.py
from urllib.parse import urlparse
# --- Импорты Graber классов ---
from urllib.parse import urlparse

# --- Импорты Graber классов ---
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


URL_PREFIX_MAP = {
    "https://ads-tec-iit.com/": AdsTecIitComGraber,
    "https://aliexpress.com/": AliexpressGraber,
    "https://amazon.com/": AmazonGraber,
    "https://apple.com/": AppleComGraber,
    "https://atlascopco.com/": AtlascopcoComGraber,
    "https://bangood.com/": BangoodGraber,
    "https://bucketmaster.com.cn/": BucketmasterComCnGraber,
    "https://cdata.com/": CdataGraber,
    "https://chat.openai.com/": "chat_gpt",
    "https://cisco.com/": CiscoComGraber,
    "https://de-de.ring.com/": DeDeRingComGraber,
    "https://de.hexcel.com/": DeHexcelComGraber,
    "https://de.rs-online.com/": DeRsOnlineComGraber,
    "https://denaliweld.com/": DenaliweldComGraber,
    "https://dewesoft.com/": DewesoftComGraber,
    "https://ebay.com/": EbayGraber,
    "https://elektrometal.eu/": ElektrometalEuGraber,
    "https://etzmaleh.com/": EtzmalehGraber,
    "https://findernet.com/": FindernetComGraber,
    "https://fresubin.com/": FresubinComGraber,
    "https://gearbest.com/": GearbestGraber,
    "https://generex.de/": GenerexDeGraber,
    "https://georgin.com/": GeorginComGraber,
    "https://german.micro-steppermotors.com/": GermanMicroSteppermotorsComGraber,
    "https://grandadvance.com/": GrandadvanceGraber,
    "https://hb.com/": HbGraber,
    "https://imos3d.com/": Imos3dComGraber,
    "https://induprogress.pl/": InduprogressPlGraber,
    "https://industrierat-west.de/": IndustrieratWestDeGraber,
    "https://it.alwsci.com/": ItAlwsciComGraber,
    "https://it.defelsko.com/": ItDefelskoComGraber,
    "https://it.jarvis-smart.com/": ItJarvisSmartComGraber,
    "https://it.superb-heater.com/": ItSuperbHeaterComGraber,
    "https://it.thermo-heater.com/": ItThermoHeaterComGraber,
    "https://ivory.co.il/": IvoryGraber,
    "https://janitza.com/": JanitzaComGraber,
    "https://jungbluth.com/": JungbluthComGraber,
    "https://ksp.co.il/": KspGraber,
    "https://kualastyle.co.il/": KualastyleGraber,
    "https://ledodm.com/": LedodmComGraber,
    "https://leybold.com/": LeyboldComGraber,
    "https://mecalux.it/": MecaluxItGraber,
    "https://megatron.de/": MegatronDeGraber,
    "https://megger.com/": MeggerComGraber,
    "https://mococonnectors.com/": MococonnectorsComGraber,
    "https://mordorintelligence.it/": MordorintelligenceItGraber,
    "https://morlevi.co.il/": MorleviGraber,
    "https://omnipod.com/": OmnipodComGraber,
    "https://opel.de/": OpelDeGraber,
    "https://pfannenberg.com/": PfannenbergComGraber,
    "https://pl.dmgmori.com/": PlDmgmoriComGraber,
    "https://plm.sw.siemens.com/": PlmSwSiemensComGraber,
    "https://prebiel.pl/": PrebielPlGraber,
    "https://prusa3d.com/": Prusa3dComGraber,
    "https://ridgid.eu/": RidgidEuGraber,
    "https://sensysmagnetometer.com/": SensysmagnetometerComGraber,
    "https://shop.loxone.com/": ShopLoxoneComGraber,
    "https://shop.scheppach.com/": ShopScheppachComGraber,
    "https://sigmaaldrich.com/": SigmaaldrichComGraber,
    "https://sphinxitalia.it/": SphinxitaliaItGraber,
    "https://vidaxl.pl/": VidaxlPlGraber,
    "https://visualdg.co.il/": VisualdgGraber,
    "https://wallashop.com/": WallashopGraber,
    "https://wallmart.com/": WallmartGraber,
    "https://zebra.com/": ZebraComGraber,
}

SUPPLIER_PREFIX_MAP = {
    "ads-tec-iit.com": AdsTecIitComGraber,
    "aliexpress": AliexpressGraber,
    "amazon": AmazonGraber,
    "apple.com": AppleComGraber,
    "atlascopco.com": AtlascopcoComGraber,
    "bangood": BangoodGraber,
    "bucketmaster.com.cn": BucketmasterComCnGraber,
    "cdata": CdataGraber,
    "cisco.com": CiscoComGraber,
    "de.de_ring.com": DeDeRingComGraber,
    "de.hexcel.com": DeHexcelComGraber,
    "de.rs_online.com": DeRsOnlineComGraber,
    "denaliweld.com": DenaliweldComGraber,
    "dewesoft.com": DewesoftComGraber,
    "ebay": EbayGraber,
    "elektrometal.eu": ElektrometalEuGraber,
    "etzmaleh": EtzmalehGraber,
    "findernet.com": FindernetComGraber,
    "fresubin.com": FresubinComGraber,
    "gearbest": GearbestGraber,
    "generex.de": GenerexDeGraber,
    "georgin.com": GeorginComGraber,
    "german_micro_steppermotors.com": GermanMicroSteppermotorsComGraber,
    "grandadvance": GrandadvanceGraber,
    "hb": HbGraber,
    "imos3d.com": Imos3dComGraber,
    "induprogress.pl": InduprogressPlGraber,
    "industrierat_west.de": IndustrieratWestDeGraber,
    "it.alwsci.com": ItAlwsciComGraber,
    "it.defelsko.com": ItDefelskoComGraber,
    "it.jarvis_smart.com": ItJarvisSmartComGraber,
    "it.superb_heater_com": ItSuperbHeaterComGraber,
    "it.thermo_heater_com": ItThermoHeaterComGraber,
    "ivory": IvoryGraber,
    "janitza_com": JanitzaComGraber,
    "jungbluth_com": JungbluthComGraber,
    "ksp": KspGraber,
    "kualastyle": KualastyleGraber,
    "ledodm.com": LedodmComGraber,
    "leybold.com": LeyboldComGraber,
    "mecalux.it": MecaluxItGraber,
    "megatron.de": MegatronDeGraber,
    "megger.com": MeggerComGraber,
    "mococonnectors.com": MococonnectorsComGraber,
    "mordorintelligence.it": MordorintelligenceItGraber,
    "morlevi": MorleviGraber,
    "omnipod.com": OmnipodComGraber,
    "opel.de": OpelDeGraber,
    "pfannenberg.com": PfannenbergComGraber,
    "pl.dmgmori.com": PlDmgmoriComGraber,
    "plm_sw_siemens.com": PlmSwSiemensComGraber,
    "prebiel.pl": PrebielPlGraber,
    "prusa3d.com": Prusa3dComGraber,
    "ridgid.eu": RidgidEuGraber,
    "sensysmagnetometer.com": SensysmagnetometerComGraber,
    "shop.loxone.com": ShopLoxoneComGraber,
    "shop.scheppach.com": ShopScheppachComGraber,
    "sigmaaldrich.com": SigmaaldrichComGraber,
    "sphinxitalia.it": SphinxitaliaItGraber,
    "vidaxl.pl": VidaxlPlGraber,
    "visualdg": VisualdgGraber,
    "wallashop": WallashopGraber,
    "wallmart": WallmartGraber,
    "zebra.com": ZebraComGraber,
}

def get_graber_by_supplier_prefix(supplier_prefix: str):
    """
    Возвращает класс Graber для данного ключа поставщика.

    :param supplier_key: ключ поставщика, например 'aliexpress'
    :return: класс Graber
    :raises ValueError: если класс для поставщика не найден
    """
    supplier_alias:str = supplier_prefix.replace('.','_').replace('-','_')

    try:
        return SUPPLIER_PREFIX_MAP[supplier_alias]
    except KeyError as ex:
        raise ValueError(f"Graber class not found for supplier: {supplier_alias}") from ex


def get_graber_by_supplier_url(url: str) -> str:
    """
    Возвращает URL-префикс, соответствующий поставщику по входному URL.

    :param url: исходный URL (например, 'https://aliexpress.com/item/abc123')
    :return: базовый URL-префикс (например, 'https://aliexpress.com/')
    :raises ValueError: если URL не соответствует ни одному из известных поставщиков
    """
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}/"

    try:
        return URL_PREFIX_MAP[base_url]
    except KeyError as ex:
        raise ValueError(f"Supplier not found for this URL base: {base_url}") from ex
