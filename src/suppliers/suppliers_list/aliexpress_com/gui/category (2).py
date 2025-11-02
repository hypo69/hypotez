## \file /src/suppliers/aliexpress/gui/category (2).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.gui 
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
  
""" module: src.suppliers.suppliers_list.aliexpress_com.gui """


""" Window interface for preparing advertising campaigns """



import header
import sys
import asyncio
from pathlib import Path
from types import SimpleNamespace
from PyQt6 import QtWidgets, QtGui, QtCore
from qasync import QEventLoop, asyncSlot
from src.utils.jjson import j_loads_ns, j_dumps
from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignEditor

class CategoryEditor(QtWidgets.QWidget):
    campaign_name: str = None
    data: SimpleNamespace = None
    language: str = 'EN'
    currency: str = 'USD'
    file_path: str = None
    editor: AliCampaignEditor
    
    def __init__(self, parent=None, main_app=None):
        """ Initialize the main window"""
        super().__init__(parent)
        self.main_app = main_app  # Save the MainApp instance

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        """ Setup the user interface"""
        self.setWindowTitle("Campaign Editor")
        self.resize(1800, 800)

        # Define UI components
        self.open_button = QtWidgets.QPushButton("Open JSON File")
        self.open_button.clicked.connect(self.open_file)
        
        self.file_name_label = QtWidgets.QLabel("No file selected")
        
        self.prepare_all_button = QtWidgets.QPushButton("Prepare All")
        self.prepare_all_button.clicked.connect(self.prepare_all_categories_async)  # Changed to async

        self.prepare_specific_button = QtWidgets.QPushButton("Prepare Category")
        self.prepare_specific_button.clicked.connect(self.prepare_category_async)  # Changed to async

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.open_button)
        layout.addWidget(self.file_name_label)
        layout.addWidget(self.prepare_all_button)
        layout.addWidget(self.prepare_specific_button)

        self.setLayout(layout)

    def setup_connections(self):
        """ Setup signal-slot connections"""
        pass

    def open_file(self):
        """ Open a file dialog to select and load a JSON file """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open JSON File",
            "c:/user/documents/repos/hypotez/data/aliexpress/campaigns",
            "JSON files (*.json)"
        )
        if not file_path:
            return  # No file selected

        self.load_file(file_path)

    def load_file(self, campaign_file):
        """ Load a JSON file """
        try:
            self.data = j_loads_ns(campaign_file)
            self.campaign_file = campaign_file
            self.file_name_label.setText(f"File: {self.campaign_file}")
            self.campaign_name = self.data.campaign_name
            path = Path(campaign_file)
            self.language = path.stem  # This will give you the file name without extension
            self.editor = AliCampaignEditor(campaign_file=campaign_file)
            self.create_widgets(self.data)
        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load JSON file: {ex}")

    def create_widgets(self, data):
        """ Create widgets based on the data loaded from the JSON file """
        layout = self.layout()

        # Remove previous widgets except open button and file label
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget not in [self.open_button, self.file_name_label, self.prepare_all_button, self.prepare_specific_button]:
                widget.deleteLater()

        title_label = QtWidgets.QLabel(f"Title: {data.title}")
        layout.addWidget(title_label)

        campaign_label = QtWidgets.QLabel(f"Campaign Name: {data.campaign_name}")
        layout.addWidget(campaign_label)

        # Correct way to handle SimpleNamespace as a dictionary
        categories = data.category.__dict__
        self.category_widgets = {}
        for category_name, category_data in categories.items():
            frame = QtWidgets.QWidget()
            frame_layout = QtWidgets.QHBoxLayout(frame)

            category_label = QtWidgets.QLabel(f"Category: {category_name}")
            frame_layout.addWidget(category_label)

            prepare_button = QtWidgets.QPushButton(f"Prepare {category_name}")
            prepare_button.clicked.connect(lambda _, name=category_name: self.prepare_category_async(name))
            frame_layout.addWidget(prepare_button)

            layout.addWidget(frame)

    @asyncSlot()
    async def prepare_all_categories_async(self):
        """ Prepare all categories asynchronously """
        if self.editor is not None:
            await self.editor.prepare_all_categories()

    @asyncSlot()
    async def prepare_category_async(self, category_name=None):
        """ Prepare a specific category asynchronously """
        if self.editor is not None and category_name:
            await self.editor.prepare_category(category_name)

    def save_changes(self):
        """ Save changes to the current file """
        try:
            if self.campaign_file and self.data:
                data_dict = self.data.__dict__
                json_data = j_dumps(data_dict)
                path = Path(self.campaign_file)
                with path.open("w", encoding="utf-8") as file:
                    file.write(json_data)
                QtWidgets.QMessageBox.information(self, "Success", "File saved successfully.")
            else:
                raise ValueError("No file loaded or no data to save.")
        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save changes: {ex}")

