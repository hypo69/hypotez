## \file /src/suppliers/aliexpress/gui/product (3).py
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


""" Window interface for managing and editing product parameters """



import header
import sys
import asyncio
from pathlib import Path
from types import SimpleNamespace
from PyQt6 import QtWidgets, QtGui, QtCore
from qasync import QEventLoop
from src.utils.jjson import j_loads_ns, j_dumps
from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignEditor

class ProductEditor(QtWidgets.QWidget):

    data: SimpleNamespace = None
    current_file_path: str = None

    def __init__(self, parent=None, main_app=None):
        """ Initialize the ProductEditor widget """
        super().__init__(parent)
        self.main_app = main_app  # Save the MainApp instance

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        """ Setup the user interface """
        self.setWindowTitle("Product Editor")
        self.resize(800, 600)

        # Define UI components
        self.open_button = QtWidgets.QPushButton("Open JSON File")
        self.open_button.clicked.connect(self.open_file)
        
        self.file_name_label = QtWidgets.QLabel("No file selected")
        
        self.product_name_label = QtWidgets.QLabel("Product Name:")
        self.product_name_edit = QtWidgets.QLineEdit()
        
        self.product_price_label = QtWidgets.QLabel("Product Price:")
        self.product_price_edit = QtWidgets.QLineEdit()
        
        self.save_button = QtWidgets.QPushButton("Save Product")
        self.save_button.clicked.connect(self.save_product)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.open_button)
        layout.addWidget(self.file_name_label)
        layout.addWidget(self.product_name_label)
        layout.addWidget(self.product_name_edit)
        layout.addWidget(self.product_price_label)
        layout.addWidget(self.product_price_edit)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def setup_connections(self):
        """ Setup signal-slot connections """
        # No additional connections needed
        pass

    def open_file(self):
        """ Open a file dialog to select and load a JSON file """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open JSON File",
            "c:/user/documents/repos/hypotez/data/aliexpress/products",
            "JSON files (*.json)"
        )
        if not file_path:
            return  # No file selected

        self.load_file(file_path)

    def load_file(self, file_path):
        """ Load a JSON file """
        try:
            self.data = j_loads_ns(file_path)
            self.current_file_path = file_path
            self.file_name_label.setText(f"File: {self.current_file_path}")
            self.populate_fields()
        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load JSON file: {ex}")

    def populate_fields(self):
        """ Populate the fields with data from the loaded JSON file """
        if not self.data:
            return
        self.product_name_edit.setText(self.data.product_name)
        self.product_price_edit.setText(str(self.data.product_price))

    def save_product(self):
        """ Save the changes made to the product """
        if not self.data:
            QtWidgets.QMessageBox.warning(self, "Warning", "No data loaded.")
            return
        
        self.data.product_name = self.product_name_edit.text()
        self.data.product_price = float(self.product_price_edit.text())

        try:
            with open(self.current_file_path, 'w', encoding='utf-8') as file:
                file.write(j_dumps(self.data))
            QtWidgets.QMessageBox.information(self, "Success", "Product data saved successfully.")
        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save product data: {ex}")

# Main function for initializing and running the application
def main():
    """ Initialize and run the application """
    app = QtWidgets.QApplication(sys.argv)

    # Create an event loop for asynchronous operations
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_app = ProductEditor()
    main_app.show()

    # Run the event loop
    with loop:
        loop.run_forever()

if __name__ == "__main__":
    main()

