# get_graber_by_supplier.py
from urllib.parse import urlparse
# --- Импорты Graber классов ---
from urllib.parse import urlparse

# --- Импорты Graber классов ---
from src.suppliers.list_of_suppliers.ads_tec_iit_com.graber import Graber as AdsTecIitComGraber
from src.suppliers.list_of_suppliers.aliexpress.graber import Graber as AliexpressGraber
from src.suppliers.list_of_suppliers.amazon.graber import Graber as AmazonGraber
from src.suppliers.list_of_suppliers.apple_com.graber import Graber as AppleComGraber
from src.suppliers.list_of_suppliers.atlascopco_com.graber import Graber as AtlascopcoComGraber
from src.suppliers.list_of_suppliers.bangood.graber import Graber as BangoodGraber
from src.suppliers.list_of_suppliers.bucketmaster_com_cn.graber import Graber as BucketmasterComCnGraber
from src.suppliers.list_of_suppliers.cdata.graber import Graber as CdataGraber
from src.suppliers.list_of_suppliers.cisco_com.graber import Graber as CiscoComGraber
from src.suppliers.list_of_suppliers.de_de_ring_com.graber import Graber as DeDeRingComGraber
from src.suppliers.list_of_suppliers.de_hexcel_com.graber import Graber as DeHexcelComGraber
from src.suppliers.list_of_suppliers.de_rs_online_com.graber import Graber as DeRsOnlineComGraber
from src.suppliers.list_of_suppliers.denaliweld_com.graber import Graber as DenaliweldComGraber
from src.suppliers.list_of_suppliers.dewesoft_com.graber import Graber as DewesoftComGraber
from src.suppliers.list_of_suppliers.ebay.graber import Graber as EbayGraber
from src.suppliers.list_of_suppliers.elektrometal_eu.graber import Graber as ElektrometalEuGraber
from src.suppliers.list_of_suppliers.etzmaleh.graber import Graber as EtzmalehGraber
from src.suppliers.list_of_suppliers.findernet_com.graber import Graber as FindernetComGraber
from src.suppliers.list_of_suppliers.fresubin_com.graber import Graber as FresubinComGraber
from src.suppliers.list_of_suppliers.gearbest.graber import Graber as GearbestGraber
from src.suppliers.list_of_suppliers.generex_de.graber import Graber as GenerexDeGraber
from src.suppliers.list_of_suppliers.georgin_com.graber import Graber as GeorginComGraber
from src.suppliers.list_of_suppliers.german_micro_steppermotors_com.graber import Graber as GermanMicroSteppermotorsComGraber
from src.suppliers.list_of_suppliers.grandadvance.graber import Graber as GrandadvanceGraber
from src.suppliers.list_of_suppliers.hb.graber import Graber as HbGraber
from src.suppliers.list_of_suppliers.imos3d_com.graber import Graber as Imos3dComGraber
from src.suppliers.list_of_suppliers.induprogress_pl.graber import Graber as InduprogressPlGraber
from src.suppliers.list_of_suppliers.industrierat_west_de.graber import Graber as IndustrieratWestDeGraber
from src.suppliers.list_of_suppliers.it_alwsci_com.graber import Graber as ItAlwsciComGraber
from src.suppliers.list_of_suppliers.it_defelsko_com.graber import Graber as ItDefelskoComGraber
from src.suppliers.list_of_suppliers.it_jarvis_smart_com.graber import Graber as ItJarvisSmartComGraber
from src.suppliers.list_of_suppliers.it_superb_heater_com.graber import Graber as ItSuperbHeaterComGraber
from src.suppliers.list_of_suppliers.it_thermo_heater_com.graber import Graber as ItThermoHeaterComGraber
from src.suppliers.list_of_suppliers.ivory.graber import Graber as IvoryGraber
from src.suppliers.list_of_suppliers.janitza_com.graber import Graber as JanitzaComGraber
from src.suppliers.list_of_suppliers.jungbluth_com.graber import Graber as JungbluthComGraber
from src.suppliers.list_of_suppliers.ksp.graber import Graber as KspGraber
from src.suppliers.list_of_suppliers.kualastyle.graber import Graber as KualastyleGraber
from src.suppliers.list_of_suppliers.ledodm_com.graber import Graber as LedodmComGraber
from src.suppliers.list_of_suppliers.leybold_com.graber import Graber as LeyboldComGraber
from src.suppliers.list_of_suppliers.mecalux_it.graber import Graber as MecaluxItGraber
from src.suppliers.list_of_suppliers.megatron_de.graber import Graber as MegatronDeGraber
from src.suppliers.list_of_suppliers.megger_com.graber import Graber as MeggerComGraber
from src.suppliers.list_of_suppliers.mococonnectors_com.graber import Graber as MococonnectorsComGraber
from src.suppliers.list_of_suppliers.mordorintelligence_it.graber import Graber as MordorintelligenceItGraber
from src.suppliers.list_of_suppliers.morlevi.graber import Graber as MorleviGraber
from src.suppliers.list_of_suppliers.omnipod_com.graber import Graber as OmnipodComGraber
from src.suppliers.list_of_suppliers.opel_de.graber import Graber as OpelDeGraber
from src.suppliers.list_of_suppliers.pfannenberg_com.graber import Graber as PfannenbergComGraber
from src.suppliers.list_of_suppliers.pl_dmgmori_com.graber import Graber as PlDmgmoriComGraber
from src.suppliers.list_of_suppliers.plm_sw_siemens_com.graber import Graber as PlmSwSiemensComGraber
from src.suppliers.list_of_suppliers.prebiel_pl.graber import Graber as PrebielPlGraber
from src.suppliers.list_of_suppliers.prusa3d_com.graber import Graber as Prusa3dComGraber
from src.suppliers.list_of_suppliers.ridgid_eu.graber import Graber as RidgidEuGraber
from src.suppliers.list_of_suppliers.sensysmagnetometer_com.graber import Graber as SensysmagnetometerComGraber
from src.suppliers.list_of_suppliers.shop_loxone_com.graber import Graber as ShopLoxoneComGraber
from src.suppliers.list_of_suppliers.shop_scheppach_com.graber import Graber as ShopScheppachComGraber
from src.suppliers.list_of_suppliers.sigmaaldrich_com.graber import Graber as SigmaaldrichComGraber
from src.suppliers.list_of_suppliers.sphinxitalia_it.graber import Graber as SphinxitaliaItGraber
from src.suppliers.list_of_suppliers.vidaxl_pl.graber import Graber as VidaxlPlGraber
from src.suppliers.list_of_suppliers.visualdg.graber import Graber as VisualdgGraber
from src.suppliers.list_of_suppliers.wallashop.graber import Graber as WallashopGraber
from src.suppliers.list_of_suppliers.wallmart.graber import Graber as WallmartGraber
from src.suppliers.list_of_suppliers.zebra_com.graber import Graber as ZebraComGraber


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
    "https://ivory.com/": IvoryGraber,
    "https://janitza.com/": JanitzaComGraber,
    "https://jungbluth.com/": JungbluthComGraber,
    "https://ksp.com/": KspGraber,
    "https://kualastyle.com/": KualastyleGraber,
    "https://ledodm.com/": LedodmComGraber,
    "https://leybold.com/": LeyboldComGraber,
    "https://mecalux.it/": MecaluxItGraber,
    "https://megatron.de/": MegatronDeGraber,
    "https://megger.com/": MeggerComGraber,
    "https://mococonnectors.com/": MococonnectorsComGraber,
    "https://mordorintelligence.it/": MordorintelligenceItGraber,
    "https://morlevi.com/": MorleviGraber,
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
    "https://visualdg.com/": VisualdgGraber,
    "https://wallashop.com/": WallashopGraber,
    "https://wallmart.com/": WallmartGraber,
    "https://zebra.com/": ZebraComGraber,
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
