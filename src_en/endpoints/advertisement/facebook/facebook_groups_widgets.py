# # \file /src/endpoints/advertisement/facebook/facebook_groups_widgets.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: SRC.endpoints.Advertisement.Facebook 
	: Platform: Windows, Unix
	: synopsis: opening menu for selection of groups for serving"""


import header 
from IPython.display import display
from ipywidgets import Dropdown
from src.utils.jjson import j_loads_ns
from types import SimpleNamespace
from pathlib import Path

class FacebookGroupsWidget:
    """Creates a falling list with URL Facebook groups from the JSON provided."""

    def __init__(self, json_file_path: Path):
        """Initialization of a widget with a falling list for Facebook groups.

        Args:
            JSON_FILE_PATH (PATH): the path to the JSON file containing information about Facebook groups."""
        self.groups_data: SimpleNamespace = j_loads_ns(json_file_path)
        self.dropdown = self.create_dropdown()

    def create_dropdown(self) -> Dropdown:
        """Creates and returns the widget of a drop -down list based on these groups.

        Returns:
            Dropdown: a widget of a drop -down list with URL Facebook groups."""
        group_urls = list(self.groups_data.__dict__.keys())
        dropdown = Dropdown(
            options=group_urls,
            description='Facebook Groups:',
            disabled=False,
        )
        return dropdown

    def display_widget(self):
        """Displays the widget of the drop -down list."""
        display(self.dropdown)


