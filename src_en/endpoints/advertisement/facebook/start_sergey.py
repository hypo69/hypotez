# # \file /src/endpoints/advertisement/facebook/start_sergey.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: SRC.endpoints.Advertisement.Facebook 
	: Platform: Windows, Unix
	: synopsis: sending advertisements to Facebook groups (Kazarinov?)"""


import header
import random
import time
import copy
from pathlib import Path 

from src import gs
from src.utils.file import get_directory_names, get_filenames
from src.webdriver.selenium.driver import Driver, Chrome
from src.endpoints.advertisement.facebook import FacebookPromoter
from src.logger.logger import logger
from src.utils.date_time import interval

# Determination of groups and categories
group_file_paths_ru: list[str] = ["sergey_pages.json"]
adv_file_paths_ru: list[str] = ["ru_ils.json"]
group_file_paths_he: list[str] = ["sergey_pages.json"]
adv_file_paths_he: list[str] = ["he_ils.json"]
group_categories_to_adv = ['sales', 'biz']

def run_campaign(d: Driver, promoter_name: str, campaigns: list | str, group_file_paths: list, language: str, currency: str):
    """Launch of an advertising campaign.

    Args:
        D (Driver): Driver copy.
        Promoter_name (str): the name of the advertiser.
        Campaigns (List): List of campaigns.
        Group_file_paths (List): Ways to files with groups.
        Language (StR): The language of the advertising campaign.
        Currency (str): currency of an advertising campaign."""

    promoter = FacebookPromoter(d, promoter=promoter_name)
    promoter.run_campaigns(
        campaigns=campaigns,
        group_file_paths=group_file_paths,
        group_categories_to_adv=group_categories_to_adv,
        language=language,
        currency=currency,
        no_video=False
    )


def campaign_cycle(d: Driver):
    """Cycle for managing the launch of campaigns.

    Args:
        D (Driver): Driver copy.
        AliExpress_Adv (Bool): flag for determining the advertiser."""
    
    file_paths_ru = copy.copy(group_file_paths_ru)
    file_paths_ru.extend(adv_file_paths_ru)    # <- Promo in groups
    file_paths_he = copy.copy(group_file_paths_he)
    file_paths_he.extend(adv_file_paths_he)

    # List of dictionaries [{Language: Currency}]
    language_currency_pairs = [{"HE": "ILS"},{"RU": "ILS"},]

    for lc in language_currency_pairs:
        # Extracting the tongue and currency from the dictionary
        for language, currency in lc.items():
            # Definition Group_file_Paths on Founding Language
            group_file_paths = file_paths_ru if language == "RU" else file_paths_he


            # Campaigns = ['Kazarinov_tips_ru', 'Kazarinov_ru'] if language == "ru" else ['Kazarinov_tips_he', 'kazarinov_he'
            campaigns = ['kazarinov_ru'] if language == "RU" else ['kazarinov_he']
            for c in campaigns:
                run_campaign(
                    d, 'kazarinov', c, 
                    group_file_paths=group_file_paths, 
                    language=language, 
                    currency=currency
                )

            campaigns = get_directory_names(gs.path.google_drive / 'aliexpress' / 'campaigns')
            run_campaign(
                d, 'aliexpress', campaigns, 
                group_file_paths=group_file_paths,
                language=language, 
                currency=currency 
                )
                    

    return True



def main():
    """The main function for launching advertising campaigns."""
    try:
        d = Driver(Chrome)
        d.get_url(r"https://facebook.com")
        aliexpress_adv = True

        while True:
            if interval():
                print("Good night!")
                time.sleep(1000)

            # The first cycle for Russian -speaking campaigns
            campaign_cycle(d)
            ...

            # Logging and delay
            logger.debug(f"going to sleep at {time.strftime('%H:%M:%S')}", None, False)
            t = random.randint(30, 360)
            print(f"sleeping {t} sec")
            time.sleep(t)

    except KeyboardInterrupt:
        logger.info("Campaign promotion interrupted.")

if __name__ == "__main__":
    main()
