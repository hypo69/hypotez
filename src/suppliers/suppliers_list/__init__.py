## \file /src/suppliers/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Импорты классов поставщиков
"""

import header
from src.suppliers.suppliers_list.aliexpress.graber import Graber as AliexpressGraber  
from src.suppliers.suppliers_list.amazon.graber import Graber as AmazonGraber
from src.suppliers.suppliers_list.bangood.graber import Graber as BangoodGraber
from src.suppliers.suppliers_list.cdata.graber import Graber as CadtaGraber
from src.suppliers.suppliers_list.ebay.graber import Graber as EbayGraber
from src.suppliers.suppliers_list.etzmaleh.graber import Graber as EtzmalehGraber
from src.suppliers.suppliers_list.gearbest.graber import Graber as GearbestGraber
from src.suppliers.suppliers_list.grandadvance.graber import Graber as GrandvanceGraber
from src.suppliers.suppliers_list.hb.graber import Graber as HbGraber
from src.suppliers.suppliers_list.ivory.graber import Graber as IvoryGraber
from src.suppliers.suppliers_list.ksp.graber import Graber as KspGraber
from src.suppliers.suppliers_list.kualastyle.graber import Graber as KualastyleGraber
from src.suppliers.suppliers_list.morlevi.graber import Graber as MorleviGraber
from src.suppliers.suppliers_list.visualdg.graber import Graber as VisualdgGraber
from src.suppliers.suppliers_list.wallashop.graber import Graber as WallashhopleGraber
from src.suppliers.suppliers_list.wallmart.graber import Graber as WallmartGraber