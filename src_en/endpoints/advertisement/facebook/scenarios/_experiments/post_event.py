# # \file /src/endpoints/advertisement/facebook/scenarios/_experiments/post_event.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. module:: src.endpoints.advertisement.facebook.scenarios._experiments 
	:platform: Windows, Unix
	:synopsis:"""


""":platform: Windows, Unix
	:synopsis:"""

""":platform: Windows, Unix
	:synopsis:"""

""":platform: Windows, Unix"""
""":platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:"""
  
"""module: src.endpoints.advertisement.facebook.scenarios._experiments"""



"""The module controls the receipt and sending of data on events on Facebook.

It interacts with JSON files containing events about events, processes them and sends the appropriate messages to Facebook groups."""

import header
from pathlib import Path
from src.endpoints.advertisement.facebook import promoter
from src import gs
from src.webdriver.selenium.driver import Driver, Chrome
from src.endpoints.advertisement.facebook import FacebookPromoter, get_event_url
from src.endpoints.advertisement.facebook.scenarios import post_event
from src.utils.jjson import j_dumps, j_loads, j_loads_ns
from src.utils.file import get_filenames, get_directory_names
from src.utils.printer import pprint

def post_events():
    """Processes and sends events to Facebook.

    The function receives data on events from the specified directory, loads the details of measures from JSON files
    And sends them to Facebook. Events are stored in the structure of the Directory under the folder `Facebook/Events`.

    RAISES:
        Filenotfounderror: If there is no JSON file with information about the event."""
    ...
    d = Driver(Chrome)
    events_dirs = get_directory_names(gs.path.google_drive / 'aliexpress' / 'events') # <- I collect events from Aliexpress
    # Group_file_paths = ['my_managed_groups.json'] # <- groups to which I will send events
    group_file_paths:list = get_filenames(  gs.path.google_drive / 'facebook' / 'groups' )
    promoter = FacebookPromoter(d = d, group_file_paths = group_file_paths)
    for event_file in events_dirs:
        event = j_loads_ns(gs.path.google_drive / 'aliexpress' / 'events'  / event_file / f'{event_file}.json')
        promoter.process_groups(events = [event], is_event = True, group_file_paths = group_file_paths)

def post_to_my_group(event):
    """"""
    ...
    groups_ns = j_loads_ns( gs.path.google_drive / 'facebook' / 'groups' / 'my_managed_groups.json')
    d = Driver(Chrome)
    for group_url, group in vars(groups_ns).items():
        group.group_url = group_url
        pprint(group.group_url)
        d.get_url(get_event_url(group.group_url))
        post_event(d,event)


if __name__ == "__main__":
    event = j_loads_ns(gs.path.google_drive / 'aliexpress' / 'events'  / 'sep_11_2024_over60_pricedown' / 'sep_11_2024_over60_pricedown.json')
    # post_to_my_group(event)
    post_events()
    # Additional processing or logic, if required
