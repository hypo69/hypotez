## \file /src/goog/spreadsheet/spreadsheet.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с Google Sheets.
==================================
Предоставляет минимальную библиотеку для взаимодействия с Google Sheets API,
включая создание, управление таблицами и загрузку данных.

 ```rst
 .. module:: src.goog.spreadsheet
 ```
"""

import header
from header import __root__

from pathlib import Path
from typing import List, Dict, Any # Retained for potential future use, though not strictly necessary for current code
import gspread
from gspread import Spreadsheet as GSpreadsheet, Worksheet # Renamed Spreadsheet to GSpreadsheet to avoid class name clash
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from src import gs
from src.logger.logger import logger
from src.utils.printer import pprint as print # Rule 10: Using custom pprint


class SpreadSheet:
    """
    Class for working with Google Sheets.

    This class provides methods for accessing the Google Sheets API,
    creating and managing spreadsheets, and uploading data from CSV files.
    """

    # Class variable declarations (documenting instance attributes)
    spreadsheet_id: str | None
    spreadsheet_name: str | None
    spreadsheet: GSpreadsheet | None # gspread.Spreadsheet object
    data_file: Path | None
    sheet_name: str | None
    credentials: ServiceAccountCredentials | None
    client: gspread.Client | None
    worksheet: Worksheet | None
    # create_sheet: bool # Declared in original, but not used. Kept for reference.

    # Path to the credentials file for accessing Google Sheets.
    # creds_file = gs.path.root / 'secrets' / 'hypo69-c32c8736ca62.json' # Original commented out path

    """ оригинал файла хранится в базе данных вместе с паролями
    @todo организовать копирование файла в прогамно созаданом `tmp`,чтобы не хранить файл в физической директории
    """

    def __init__(self,
                 spreadsheet_id: str | None = None,
                 spreadsheet_name: str | None = None,
                 sheet_name: str | None = None,
                 data_file: Path | str | None = None):
        """
        Initializes the SpreadSheet handler.

        The method authenticates with Google Sheets API. If `spreadsheet_id` is provided,
        it attempts to open that spreadsheet. Otherwise, if `spreadsheet_name` is provided,
        it creates a new spreadsheet. If `sheet_name` is also provided, it attempts to
        get or create that specific worksheet.

        Args:
            spreadsheet_id (str | None, optional): ID of the Google Sheets spreadsheet.
                If `None`, a new spreadsheet might be created if `spreadsheet_name` is provided. Defaults to `None`.
            spreadsheet_name (str | None, optional): Name for a new spreadsheet if `spreadsheet_id` is `None`.
                Defaults to `None`.
            sheet_name (str | None, optional): Name of the worksheet to work with.
                If the sheet doesn't exist, it will be created. Defaults to `None`.
            data_file (Path | str | None, optional): Path to a CSV data file for potential operations.
                Defaults to `None`.
        
        Raises:
            gspread.exceptions.SpreadsheetNotFound: If `spreadsheet_id` is provided but the spreadsheet does not exist.
            Exception: For errors during credential creation, client authorization, or spreadsheet creation.
        """
        self.spreadsheet_id: str | None = spreadsheet_id
        self.spreadsheet_name: str | None = spreadsheet_name
        self.sheet_name: str | None = sheet_name
        self.data_file: Path | None = Path(data_file) if data_file else None
        
        self.credentials: ServiceAccountCredentials | None = None
        self.client: gspread.Client | None = None
        self.spreadsheet: GSpreadsheet | None = None
        self.worksheet: Worksheet | None = None

        self.credentials = self._create_credentials()
        if not self.credentials:
            # Error already logged in _create_credentials
            # Raising an exception to halt initialization if credentials fail
            raise Exception('Failed to create Google API credentials.')

        self.client = self._authorize_client()
        if not self.client:
            # Error already logged in _authorize_client
            # Raising an exception to halt initialization if client authorization fails
            raise Exception('Failed to authorize Google API client.')

        try:
            if self.spreadsheet_id:
                self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
                # logger.debug(f"Opened existing spreadsheet with ID: {self.spreadsheet_id}")
            elif self.spreadsheet_name:
                self.spreadsheet = self.client.create(self.spreadsheet_name)
                self.spreadsheet_id = self.spreadsheet.id # Update ID from new spreadsheet
                # logger.debug(f"Created new spreadsheet: '{self.spreadsheet_name}' with ID: {self.spreadsheet_id}")
            else:
                logger.warning('Neither spreadsheet_id nor spreadsheet_name provided. No spreadsheet opened or created.')
                # No spreadsheet to work with, but not necessarily an error depending on use case.
                # Consider raising an error if a spreadsheet is strictly required.
                # raise ValueError("Either spreadsheet_id or spreadsheet_name must be provided.")

            if self.spreadsheet and self.sheet_name:
                self.worksheet = self.get_worksheet(self.sheet_name)

        except gspread.exceptions.SpreadsheetNotFound as ex:
            logger.error(f"Spreadsheet with ID '{self.spreadsheet_id}' does not exist.", ex) # exc_info=False as ex is passed
            raise
        except Exception as ex:
            logger.error('Error during spreadsheet access or creation.', ex, exc_info=True)
            raise

    def _create_credentials(self) -> ServiceAccountCredentials | None:
        """
        Function creates credentials from a JSON key file.

        Returns:
            ServiceAccountCredentials | None: Credentials for accessing Google Sheets, or `None` on failure.
        
        Raises:
            Exception: Propagates exceptions from credential creation process after logging.
        """
        creds_file: Path
        SCOPES: List[str]
        credentials: ServiceAccountCredentials | None = None
        
        try:
            # Path to the service account key file.
            creds_file = gs.path.secrets / 'e-cat-346312-137284f4419e.json' # <- e.cat.co.il@gmail.com
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                str(creds_file), SCOPES # Ensure creds_file is string for some versions
            )
            # logger.debug("Credentials created successfully.")
            return credentials
        except Exception as ex:
            logger.error('Error creating credentials.', ex, exc_info=True)
            # Raising an exception allows the caller to handle the failure appropriately.
            # Or return None and let caller check. Returning None for now.
            return None


    def _authorize_client(self) -> gspread.Client | None:
        """
        Function authorizes a client to access the Google Sheets API.

        Uses the credentials created by `_create_credentials`.

        Returns:
            gspread.Client | None: Authorized client for Google Sheets, or `None` on failure.
        
        Raises:
            Exception: Propagates exceptions from client authorization after logging.
        """
        client: gspread.Client | None = None
        try:
            if not self.credentials:
                logger.error('Cannot authorize client: credentials not available.')
                return None
            client = gspread.authorize(self.credentials)
            # logger.debug("Client authorized successfully.")
            return client
        except Exception as ex:
            logger.error('Error authorizing client.', ex, exc_info=True)
            return None

    def get_worksheet(self, worksheet_name: str) -> Worksheet | None:
        """
        Function retrieves a worksheet by its name.

        If the worksheet does not exist, it attempts to create it.

        Args:
            worksheet_name (str): The name of the worksheet in Google Sheets.

        Returns:
            Worksheet | None: The gspread Worksheet object, or `None` if the spreadsheet is not available
                              or an error occurs.
        """
        ws: Worksheet | None = None
        if not self.spreadsheet:
            logger.error('Cannot get worksheet: spreadsheet not loaded or created.')
            return None
        try:
            ws = self.spreadsheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            logger.info(f"Worksheet '{worksheet_name}' not found. Attempting to create it.")
            ws = self.create_worksheet(worksheet_name)
        except Exception as ex:
            logger.error(f"Error getting worksheet '{worksheet_name}'.", ex, exc_info=True)
            return None # Return None on other errors
        return ws

    def create_worksheet(self, title: str, dim: Dict[str, int] = {'rows': 100, 'cols': 26}) -> Worksheet | None:
        """
        Function creates a new worksheet with the given title and dimensions.

        Args:
            title (str): The title for the new worksheet.
            dim (Dict[str, int], optional): A dictionary specifying 'rows' and 'cols' for the new worksheet.
                                            Defaults to {'rows': 100, 'cols': 26}.

        Returns:
            Worksheet | None: The created gspread Worksheet object, or `None` on failure.
        """
        ws: Worksheet | None = None
        if not self.spreadsheet:
            logger.error('Cannot create worksheet: spreadsheet not loaded or created.')
            return None
        try:
            ws = self.spreadsheet.add_worksheet(title=title, rows=dim['rows'], cols=dim['cols'])
            logger.info(f"Successfully created worksheet '{title}'.")
            return ws
        except Exception as ex:
            logger.error(f"Error creating new worksheet '{title}'.", ex, exc_info=True)
            return None

    def copy_worksheet(self, from_worksheet_name: str, to_worksheet_name: str) -> Worksheet | None:
        """
        Function copies an existing worksheet to a new worksheet with a specified name.

        Args:
            from_worksheet_name (str): The name of the source worksheet to copy.
            to_worksheet_name (str): The name for the new (copied) worksheet.

        Returns:
            Worksheet | None: The newly created gspread Worksheet object, or `None` on failure.
        """
        original_worksheet: Worksheet | None = None
        new_worksheet: Worksheet | None = None

        if not self.spreadsheet:
            logger.error('Cannot copy worksheet: spreadsheet not loaded or created.')
            return None
        try:
            original_worksheet = self.spreadsheet.worksheet(from_worksheet_name)
            # The method `duplicate` creates and returns the new worksheet.
            new_worksheet = original_worksheet.duplicate(new_sheet_name=to_worksheet_name)
            logger.info(f"Worksheet '{from_worksheet_name}' copied to '{to_worksheet_name}' successfully.")
            return new_worksheet
        except gspread.exceptions.WorksheetNotFound:
            logger.error(f"Source worksheet '{from_worksheet_name}' not found for copying.", exc_info=False) # No ex object here
            return None
        except Exception as ex:
            logger.error(f"Error copying worksheet '{from_worksheet_name}' to '{to_worksheet_name}'.", ex, exc_info=True)
            return None

    def upload_data_to_sheet(self, data_file: Path | str | None = None, worksheet_name: str | None = None) -> bool:
        """
        Function uploads data from a CSV file to a specified Google Sheet worksheet.

        Uses `self.data_file` and `self.worksheet` if parameters are not provided.
        If `worksheet_name` is provided, it will attempt to get/create that worksheet.

        Args:
            data_file (Path | str | None, optional): Path to the CSV data file. If None, uses `self.data_file`.
                                                    Defaults to `None`.
            worksheet_name (str | None, optional): Name of the target worksheet. If None, uses `self.worksheet`.
                                                   Defaults to `None`.

        Returns:
            bool: `True` if data uploaded successfully, `False` otherwise.
        
        Raises:
            ValueError: If data file path is not set or the file does not exist.
                        (This is effectively handled by returning False and logging)
        """
        df_data: pd.DataFrame
        data_list: List[List[Any]]
        target_data_file: Path | None = None
        target_worksheet: Worksheet | None = None
        
        # Determine the data file to use
        if data_file:
            target_data_file = Path(data_file)
        elif self.data_file:
            target_data_file = self.data_file
        else:
            logger.error('Data file path is not specified for upload.')
            return False

        if not target_data_file.exists():
            logger.error(f"Data file does not exist: {target_data_file}")
            return False # Changed from raise ValueError to return False as per file operation rules

        # Determine the worksheet to use
        if worksheet_name:
            target_worksheet = self.get_worksheet(worksheet_name)
        elif self.worksheet:
            target_worksheet = self.worksheet
        else:
            logger.error('Worksheet is not specified or available for upload.')
            return False
            
        if not target_worksheet:
            logger.error('Failed to get or create target worksheet for upload.')
            return False

        try:
            df_data = pd.read_csv(target_data_file)
            # Prepare data for writing to Google Sheets (header + values)
            data_list = [df_data.columns.values.tolist()] + df_data.values.tolist()
            target_worksheet.update('A1', data_list)  # Write data to Google Sheets
            # logger.debug(f"Data from '{target_data_file}' has been uploaded to worksheet '{target_worksheet.title}' successfully.")
            return True
        except FileNotFoundError: # Should be caught by exists() check, but good practice
            logger.error(f"Data file not found during read: {target_data_file}", exc_info=True)
            return False
        except Exception as ex:
            logger.error(f"Error uploading data from '{target_data_file}' to worksheet '{target_worksheet.title}'.", ex, exc_info=True)
            return False


# Example usage, adjusted for the refactored class
if __name__ == '__main__':
    # This import is for the example itself, not strictly for the class if gs is not used inside directly
    # from src import gs 

    # Define path for data file. Ensure it's correct for your environment.
    # Example: creating a dummy CSV for the example to run
    dummy_csv_path: Path = __root__ / 'temp_sample_data.csv'
    try:
        dummy_csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dummy_csv_path, 'w') as f:
            f.write('col1,col2\nval1,val2\nval3,val4')
    except Exception as ex:
        print(f'Could not create dummy CSV: {ex}') # Using the custom print
        dummy_csv_path = None # Ensure it's None if creation fails

    example_sheet_name: str = 'ExampleSheet1'
    example_new_spreadsheet_name: str = 'MyAutoCreatedSpreadsheet'

    print(f'Attempting to use/create spreadsheet: "{example_new_spreadsheet_name}" and sheet: "{example_sheet_name}"')

    # Create a new Spreadsheet (spreadsheet_id=None)
    # Pass data_file path to __init__ or to upload_data_to_sheet method
    sheet_handler: SpreadSheet | None = None
    try:
        sheet_handler = SpreadSheet(
            spreadsheet_id=None,  # Specify None to create a new Spreadsheet
            spreadsheet_name=example_new_spreadsheet_name,
            sheet_name=example_sheet_name,
            # data_file=dummy_csv_path # Option 1: pass data_file to constructor
        )

        if sheet_handler and sheet_handler.spreadsheet and sheet_handler.worksheet:
            print(f"Spreadsheet '{sheet_handler.spreadsheet.title}' (ID: {sheet_handler.spreadsheet_id}) is ready.")
            print(f"Worksheet '{sheet_handler.worksheet.title}' is ready.")

            # Upload data if dummy_csv_path is valid
            if dummy_csv_path and dummy_csv_path.exists():
                # Option 2: pass data_file to method
                if sheet_handler.upload_data_to_sheet(data_file=dummy_csv_path):
                    print(f"Data from '{dummy_csv_path.name}' uploaded successfully to '{sheet_handler.worksheet.title}'.")
                else:
                    print(f"Failed to upload data from '{dummy_csv_path.name}'.")
            else:
                print(f"Skipping data upload: dummy CSV file '{dummy_csv_path}' not available.")
            
            # Example of copying a worksheet
            copied_sheet_name = f'{example_sheet_name}_copy'
            copied_ws = sheet_handler.copy_worksheet(example_sheet_name, copied_sheet_name)
            if copied_ws:
                print(f"Worksheet '{example_sheet_name}' successfully copied to '{copied_ws.title}'.")
            else:
                print(f"Failed to copy worksheet '{example_sheet_name}'.")

        else:
            if sheet_handler:
                 print(f"Failed to initialize Spreadsheet handler fully. Spreadsheet ready: {bool(sheet_handler.spreadsheet)}, Worksheet ready: {bool(sheet_handler.worksheet)}")
            else:
                print("Failed to create SpreadSheet object.")

    except Exception as ex:
        # Exceptions from __init__ (like auth failures) will be caught here
        print(f"An error occurred during Spreadsheet setup or operations: {ex}")
    finally:
        # Clean up dummy CSV
        if dummy_csv_path and dummy_csv_path.exists():
            try:
                dummy_csv_path.unlink()
                print(f"Cleaned up dummy CSV: {dummy_csv_path}")
            except OSError as ex_os:
                print(f"Error cleaning up dummy CSV {dummy_csv_path}: {ex_os}")
