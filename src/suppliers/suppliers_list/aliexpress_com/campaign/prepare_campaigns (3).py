## \file /src/suppliers/aliexpress/campaign/prepare_campaigns (3).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.suppliers.suppliers_list.aliexpress_com.campaign """



"""
This module prepares AliExpress campaigns by processing categories, handling campaign data, and generating promotional materials.

### Examples:
To run the script for a specific campaign:

    python src/suppliers/aliexpress/campaigns/prepare_campaigns.py summer_sale -c electronics -l EN -cu USD -f

To process all campaigns:

    python src/suppliers/aliexpress/campaigns/prepare_campaigns.py --all -l EN -cu USD
"""
import header
import argparse
import asyncio
import datetime
import html
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional
from src import gs
from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress_com.campaign.html_generators import (
    ProductHTMLGenerator,
    CategoryHTMLGenerator,
    CampaignHTMLGenerator,
)
from src.utils import get_directory_names, get_filenames, save_text_file
from src.utils.jjson import j_dumps
from src.logger.logger import logger

# Define the path to the directory with campaigns
campaigns_directory = gs.path.google_drive / "aliexpress" / "campaigns"
locales:dict = {"EN": "USD", "HE": "ILS", "RU": "ILS"}

def process_new_campaign(self, campaign_name: str):
    """"""
    AliCampaignEditor(campaign_name).process_new_campaign()

def process_campaign_category(
    campaign_name: str, category_name: str, language: str, currency: str
) -> List[str]:
    """Processes a specific category within a campaign for all languages and currencies.

    Args:
        campaign_name (str): Name of the advertising campaign.
        category_name (str): Category for the campaign.
        language (str): Language for the campaign.
        currency (str): Currency for the campaign.

    Returns:
        List[str]: List of product titles within the category.

    Example:
        >>> titles: List[str] = process_campaign_category("summer_sale", "electronics", "EN", "USD")
        >>> print(titles)
        ['Product 1', 'Product 2']
    """
    return AliCampaignEditor(
        campaign_name=campaign_name, language=language, currency=currency
    ).process_campaign_category(category_name)

def process_campaign(
    campaign_name: str,
    language: str | None = None,
    currency: str | None = None,
    campaign_file: str | None = None,
) -> bool:
    """Processes a campaign and handles the campaign's setup and processing.

    Args:
        campaign_name (str): Name of the advertising campaign.
        language (Optional[str]): Language for the campaign. If not provided, process for all locales.
        currency (Optional[str]): Currency for the campaign. If not provided, process for all locales.
        campaign_file (Optional[str]): Optional path to a specific campaign file.

    Example:
        >>> res = process_campaign("summer_sale", "EN", "USD", "campaign_file.json")

    Returns:
        bool: True if campaign processed, else False.
    """
    locales_to_process = (
        [(language, currency)] if language and currency else locales.items()
    )

    for lang, curr in locales_to_process:
        editor = AliCampaignEditor(
            campaign_name=campaign_name,
            language=lang,
            currency=curr,
            campaign_file=campaign_file,
        )
        editor.process_campaign()

    return True  # Assuming the campaign is always processed successfully


def process_all_campaigns(language: Optional[str] = None, currency: Optional[str] = None) -> None:
    """Processes all campaigns in the 'campaigns' directory for the specified language and currency.

    Args:
        language (str): Language for the campaigns.
        currency (str): Currency for the campaigns.

    Example:
        >>> process_all_campaigns("EN", "USD")
    """
    for language, currency in locales.items():
        campaign_dirs = get_directory_names(campaigns_directory)
        for campaign_name in campaign_dirs:
            campaign_editor = AliCampaignEditor(
                campaign_name=campaign_name, language=language, currency=currency
            )
            logger.info(f"start {campaign_name=}, {language=}, {currency=} ")
            campaign_editor.process_campaign()
def main_process(campaign_name: str, categories: List[str], language: str, currency: str) -> None:
    """Main function to process a campaign.

    Args:
        campaign_name (str): Name of the advertising campaign.
        categories (List[str]): List of categories for the campaign.
        language (str): Language for the campaign.
        currency (str): Currency for the campaign.

    Example:
        >>> main_process("summer_sale", ["electronics"], "EN", "USD")
    """
    if not categories:
        # Always get all categories from the directory
        process_campaign(campaign_name = campaign_name, language = language, currency = currency)

    for category in categories:
        process_campaign_category(campaign_name, category, language, currency)                                                          
                                                          
def main() -> None:
    """Main function to parse arguments and initiate processing.

    Example:
        >>> main()
    """
    parser = argparse.ArgumentParser(description="Prepare AliExpress Campaign")
    parser.add_argument("campaign_name", type=str, help="Name of the campaign")
    parser.add_argument(
        "-c",
        "--categories",
        nargs="+",
        help="List of categories (if not provided, all categories will be used)",
    )
    parser.add_argument(
        "-l", "--language", type=str, default="EN", help="Language for the campaign"
    )
    parser.add_argument(
        "-cu", "--currency", type=str, default="USD", help="Currency for the campaign"
    )
    parser.add_argument(
        "-f", "--force_update", action="store_true", help="Force update categories"
    )
    parser.add_argument("--all", action="store_true", help="Process all campaigns")

    args = parser.parse_args()
                    
    if args.all:
        process_all_campaigns(args.language, args.currency)
    else:
        main_process(
            args.campaign_name, args.categories or [], args.language, args.currency
        )


if __name__ == "__main__":
    main()