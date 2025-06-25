from pathlib import Path
from types import SimpleNamespace
from typing import Optional, List

from pydoll.browser.chrome import Chrome
from pydoll.browser.page import Page

from header import __root__
from src import gs
from src.webdriver.executor_pydoll import execute_locator
from src.utils.file import get_filenames_from_directory
from src.utils.jjson import j_loads_ns
from src.endpoints.prestashop.product_fields import ProductFields
from src.logger.logger import logger

# --- config.py ---
class Config:
    """Script-wide configuration (not supplier-specific)."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    SCENARIOS_DIR: Path = ENDPOINT / 'scenarios'
    SUPPLIERS_ENDPOINT: Path = __root__ / 'src' / 'suppliers' / 'suppliers_list'

    PRESTA_API_KEY: str = gs.credentials.prestashop.store_davidka_net.api_key
    PRESTA_API_DOMAIN: str = gs.credentials.prestashop.store_davidka_net.api_domain



    @property
    def scenarios_files(self) -> List[str]:
        return get_filenames_from_directory(self.SCENARIOS_DIR)
# --- end config.py ---

class Graber:
    """Grabs product/category info for a given supplier."""

    browser: Chrome = None
    page: Page = None
    product_locators: SimpleNamespace = None
    category_locators: SimpleNamespace = None  
    
    def __init__(self, config: Config, supplier_prefix: str):
        self.config = config
        self.supplier_prefix: str = supplier_prefix
        self.supplier_alias: str = supplier_prefix.replace('.', '_').replace('-', '_')

        self.supplier_config_path: Path = config.SUPPLIERS_ENDPOINT / self.supplier_alias
        self.locators_path: Path = self.supplier_config_path / 'locators'

        self.product_locators: SimpleNamespace = j_loads_ns(self.locators_path / 'product.json')
        self.category_locators: SimpleNamespace = j_loads_ns(self.locators_path / 'category.json')

        self.product_url: str = 'https://he.aliexpress.com/item/1005007819575751.html'  # может переопределяться
        self.browser: Optional[Chrome] = config.browser
        self.page: Optional[Page] = config.page

    async def grab_product(self, product_url: str, page: Page) -> ProductFields:
        """Grab product fields."""
        locator:SimpleNamespace = self.product_locators
        f:ProductFields = ProductFields()

        await page.go_to(product_url)
        f.id_supplier = locator.id_supplier
        f.name = await execute_locator(page, locator.name)
        f.price = await execute_locator(page, locator.price)
        f.description = await execute_locator(page, locator.description)
        f.description_short = await execute_locator(page, locator.description_short)
        
        return f

    async def run_scenario(self, supplier_prefix: str, scenario: SimpleNamespace) -> bool:
        """Run a grabbing scenario."""
        try:
            async with self.browser:
                await self.browser.start()
                page = await self.browser.get_page()
                await self.grab_product(self.product_url, page)
                return True
        except Exception as ex:
            logger.error("Ошибка при выполнении сценария", ex)
            return False

