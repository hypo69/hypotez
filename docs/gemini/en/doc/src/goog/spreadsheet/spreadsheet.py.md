# Module: src.goog.spreadsheet.spreadsheet

## Overview

This module provides a class `SpreadSheet` for working with Google Sheets. It allows users to:

- **Create and manage spreadsheets:** Create new spreadsheets, open existing spreadsheets by ID, and manage worksheets within a spreadsheet.
- **Upload data to Google Sheets:** Upload data from CSV files to a specified Google Sheet.
- **Get worksheets by name:** Retrieve a specific worksheet from a spreadsheet by name.
- **Create new worksheets:** Create new worksheets within a spreadsheet.
- **Copy worksheets:** Copy an existing worksheet to a new worksheet with a specified name.

## Details

The `SpreadSheet` class utilizes the Google Sheets API to interact with Google Sheets. It is designed to be a simple and intuitive library for managing basic Google Sheets operations.

## Classes

### `SpreadSheet`

**Description**: This class facilitates interaction with Google Sheets through the Google Sheets API. It offers methods for creating and managing spreadsheets, uploading data from CSV files, retrieving worksheets, and creating new worksheets.

**Inherits**: None

**Attributes**:

- `spreadsheet_id` (`str` | `None`): The ID of the Google Sheets spreadsheet. If `None`, a new spreadsheet is created.
- `spreadsheet_name` (`str` | `None`): The name of the new spreadsheet if `spreadsheet_id` is `None`.
- `spreadsheet` (`Spreadsheet`): An instance of the `Spreadsheet` class from the `gspread` library representing the Google Sheets spreadsheet.
- `data_file` (`Path`): The path to the CSV file containing the data to upload.
- `sheet_name` (`str`): The name of the sheet in Google Sheets where data will be uploaded.
- `credentials` (`ServiceAccountCredentials`): Credentials for accessing the Google Sheets API.
- `client` (`gspread.Client`): An authorized client for working with the Google Sheets API.
- `worksheet` (`Worksheet`): An instance of the `Worksheet` class from the `gspread` library representing the active worksheet.
- `create_sheet` (`bool`): A flag indicating whether to create a new sheet if it doesn't exist.

**Methods**:

- `__init__(self, spreadsheet_id: str, *args, **kwargs)`: Initialize a `SpreadSheet` instance with the specified credentials and data file.
- `_create_credentials(self)`: Create credentials from a JSON file for accessing the Google Sheets API.
- `_authorize_client(self)`: Authorize the client to access the Google Sheets API.
- `get_worksheet(self, worksheet_name: str | Worksheet) -> Worksheet | None`: Get the worksheet by name. If the specified sheet doesn't exist and `create_if_not_present` is `True`, a new sheet is created.
- `create_worksheet(self, title: str, dim: dict = {'rows': 100, 'cols': 10}) -> Worksheet | None`: Creates a new worksheet with the given title and dimensions.
- `copy_worksheet(self, from_worksheet: str, to_worksheet: str)`: Copies an existing worksheet to a new worksheet with a specified name.
- `upload_data_to_sheet(self)`: Uploads data from a CSV file to the specified sheet in Google Sheets.

## Class Methods

### `__init__(self, spreadsheet_id: str, *args, **kwargs)`

```python
    def __init__(self, \
                 spreadsheet_id: str, *args, **kwargs):  # Name of the sheet in Google Sheets
        """ Initialize GoogleSheetHandler with specified credentials and data file.
        
        @param spreadsheet_id ID of the Google Sheets spreadsheet. Specify None to create a new Spreadsheet.
        @param spreadsheet_name Name of the new Spreadsheet if spreadsheet_id is not specified.
        @param sheet_name Name of the sheet in Google Sheets.
        """
        self.spreadsheet_id = spreadsheet_id
        self.credentials = self._create_credentials()
        self.client = self._authorize_client()
        
        try:
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            #logger.debug(f"Opened existing spreadsheet with ID: {self.spreadsheet_id}")
        except gspread.exceptions.SpreadsheetNotFound:
            logger.error(f"Spreadsheet with ID \'{self.spreadsheet_id}\' does not exist.")
            raise
```

**Purpose**: Initializes the `SpreadSheet` instance with specified credentials and data file.

**Parameters**:

- `spreadsheet_id` (`str`): ID of the Google Sheets spreadsheet. Specify `None` to create a new spreadsheet.
- `spreadsheet_name` (`str` | `None`): Name of the new spreadsheet if `spreadsheet_id` is `None`.
- `sheet_name` (`str`): Name of the sheet in Google Sheets.

**How the Method Works**:

- Initializes the `spreadsheet_id`, `credentials`, and `client` attributes.
- Attempts to open the specified spreadsheet by its ID using `self.client.open_by_key(self.spreadsheet_id)`.
- If the spreadsheet is not found, it raises a `gspread.exceptions.SpreadsheetNotFound` exception with an error message logged using the `logger` module.

**Examples**:

```python
# Create a new spreadsheet
google_sheet_handler = SpreadSheet(
    spreadsheet_id=None,
    sheet_name='Sheet1',
    spreadsheet_name='My New Spreadsheet'
)

# Open an existing spreadsheet
spreadsheet_id = 'your_spreadsheet_id'
google_sheet_handler = SpreadSheet(
    spreadsheet_id=spreadsheet_id,
    sheet_name='Sheet1'
)
```

### `_create_credentials(self)`

```python
    def _create_credentials(self):
        """ Create credentials from a JSON file.
        
        Creates credentials for accessing the Google Sheets API based on the key file.
        @return Credentials for accessing Google Sheets.
        """
        try:
            creds_file:Path = gs.path.secrets / \'e-cat-346312-137284f4419e.json\' # <-  e.cat.co.il@gmail.com
            SCOPES: list = [\'https://www.googleapis.com/auth/spreadsheets\', \'https://www.googleapis.com/auth/drive\']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                creds_file, SCOPES
            )
            #logger.debug("Credentials created successfully.")
            return credentials
        except Exception as ex:
            logger.error("Error creating credentials.", ex, exc_info=True)
            raise
```

**Purpose**: Creates credentials for accessing the Google Sheets API based on a JSON file.

**Parameters**: None

**Returns**:

- `ServiceAccountCredentials`: Credentials for accessing Google Sheets.

**Raises Exceptions**:

- `Exception`: If an error occurs during credential creation.

**How the Method Works**:

- Reads the Google Sheets API key from the `creds_file` path, which is defined as `gs.path.secrets / 'e-cat-346312-137284f4419e.json'`.
- Defines the required scopes: `'https://www.googleapis.com/auth/spreadsheets'` and `'https://www.googleapis.com/auth/drive'`.
- Creates `ServiceAccountCredentials` using `ServiceAccountCredentials.from_json_keyfile_name(creds_file, SCOPES)`.
- Returns the generated `credentials` object.

**Examples**:

```python
# Example of using the _create_credentials method (within the SpreadSheet class)
credentials = self._create_credentials()
```

### `_authorize_client(self)`

```python
    def _authorize_client(self):
        """ Authorize client to access the Google Sheets API.
        
        Creates and authorizes a client for the Google Sheets API based on the provided credentials.
        @return Authorized client for working with Google Sheets.
        """
        try:
            client = gspread.authorize(self.credentials)
            #logger.debug("Client authorized successfully.")
            return client
        except Exception as ex:
            logger.error("Error authorizing client.", ex, exc_info=True)
            raise
```

**Purpose**: Authorizes the client to access the Google Sheets API based on the provided credentials.

**Parameters**: None

**Returns**:

- `gspread.Client`: An authorized client for working with Google Sheets.

**Raises Exceptions**:

- `Exception`: If an error occurs during client authorization.

**How the Method Works**:

- Uses the `gspread.authorize(self.credentials)` method to authorize the client using the `self.credentials` object.
- Returns the authorized `client` object.

**Examples**:

```python
# Example of using the _authorize_client method (within the SpreadSheet class)
client = self._authorize_client()
```

### `get_worksheet(self, worksheet_name: str | Worksheet) -> Worksheet | None`

```python
    def get_worksheet(self, worksheet_name: str | Worksheet) -> Worksheet | None:
        """ Get the worksheet by name.
        
        If the sheet with the specified name does not exist and the `create_if_not_present` flag is set to True, a new sheet is created.
        
        @param worksheet Name of the sheet in Google Sheets.
        @param create_if_not_present Flag to create a new sheet if it does not exist. If False and the sheet does not exist, an exception is raised.
        @return Worksheet for working with data.
        """
        
        try:
            ws: Worksheet = self.spreadsheet.worksheet(worksheet_name) 
        except gspread.exceptions.WorksheetNotFound:
            ws: Worksheet  = self.create_worksheet(worksheet_name)
        return ws
```

**Purpose**: Retrieves the worksheet from the spreadsheet by name. If the specified sheet doesn't exist, a new sheet with the given name is created.

**Parameters**:

- `worksheet_name` (`str` | `Worksheet`): The name of the sheet in Google Sheets.

**Returns**:

- `Worksheet` | `None`: The worksheet for working with data or `None` if an error occurs.

**How the Method Works**:

- Tries to get the worksheet by name using `self.spreadsheet.worksheet(worksheet_name)`.
- If the sheet is not found (`gspread.exceptions.WorksheetNotFound`), it calls the `create_worksheet` method to create a new sheet with the specified name.
- Returns the `ws` object, which is either the retrieved worksheet or the newly created worksheet.

**Examples**:

```python
# Get an existing worksheet
worksheet = google_sheet_handler.get_worksheet('Sheet1')

# Create a new worksheet if it doesn't exist
worksheet = google_sheet_handler.get_worksheet('New Sheet')
```

### `create_worksheet(self, title: str, dim: dict = {'rows': 100, 'cols': 10}) -> Worksheet | None`

```python
    def create_worksheet(self, title:str, dim:dict = {\'rows\':100,\'cols\':10}) -> Worksheet | None:
        """ функция создает новую страницу с именем `title` и размерностью `dim`"""
        try:
            ws: Worksheet = self.spreadsheet.add_worksheet(title=title, rows=dim[\'rows\'], cols=dim[\'cols\']) 
            return(ws)
        except Exception as ex:
            logger.error(f"Ошибка создания нового листа {title}")
```

**Purpose**: Creates a new worksheet with the given title and dimensions.

**Parameters**:

- `title` (`str`): The name of the new worksheet.
- `dim` (`dict`, optional): A dictionary specifying the dimensions of the new worksheet. Defaults to `{'rows': 100, 'cols': 10}`.

**Returns**:

- `Worksheet` | `None`: The newly created worksheet or `None` if an error occurs.

**Raises Exceptions**:

- `Exception`: If an error occurs during worksheet creation.

**How the Method Works**:

- Creates a new worksheet using `self.spreadsheet.add_worksheet(title=title, rows=dim['rows'], cols=dim['cols'])`.
- Returns the newly created `ws` object.

**Examples**:

```python
# Create a new worksheet with the default dimensions
worksheet = google_sheet_handler.create_worksheet('My New Sheet')

# Create a new worksheet with custom dimensions
worksheet = google_sheet_handler.create_worksheet('Custom Sheet', dim={'rows': 50, 'cols': 20})
```

### `copy_worksheet(self, from_worksheet: str, to_worksheet: str)`

```python
    def copy_worksheet(self, from_worksheet: str, to_worksheet: str):
        """ Copy worksheet by name."""
        ...
        worksheet: Worksheet = self.spreadsheet.worksheet(from_worksheet)
        worksheet.duplicate(new_sheet_name=to_worksheet)
        return worksheet
```

**Purpose**: Copies an existing worksheet to a new worksheet with a specified name.

**Parameters**:

- `from_worksheet` (`str`): The name of the worksheet to be copied.
- `to_worksheet` (`str`): The name of the new worksheet.

**Returns**:

- `Worksheet`: The newly created worksheet.

**How the Method Works**:

- Gets the `worksheet` object using `self.spreadsheet.worksheet(from_worksheet)`.
- Duplicates the worksheet using `worksheet.duplicate(new_sheet_name=to_worksheet)`.
- Returns the duplicated `worksheet` object.

**Examples**:

```python
# Copy 'Sheet1' to a new worksheet named 'Sheet1_Copy'
copied_worksheet = google_sheet_handler.copy_worksheet('Sheet1', 'Sheet1_Copy')
```

### `upload_data_to_sheet(self)`

```python
    def upload_data_to_sheet(self):
        """ Upload data from a CSV file to Google Sheets.
        
        Uploads data from the CSV file specified in `self.data_file` to the specified sheet in Google Sheets.
        """
        try:
            if not self.data_file or not self.data_file.exists():
                raise ValueError("Data file path is not set or the file does not exist.")
            
            data = pd.read_csv(self.data_file)  # Read data from the CSV file
            data_list = [data.columns.values.tolist()] + data.values.tolist()  # Prepare data for writing to Google Sheets
            self.worksheet.update('A1', data_list)  # Write data to Google Sheets
            #logger.debug("Data has been uploaded to Google Sheets successfully.")
        except Exception as ex:
            logger.error("Error uploading data to Google Sheets.", ex, exc_info=True)
            raise
```

**Purpose**: Uploads data from a CSV file to the specified sheet in Google Sheets.

**Parameters**: None

**How the Method Works**:

- Checks if the `self.data_file` attribute is set and the file exists. If not, it raises a `ValueError`.
- Reads data from the CSV file using `pd.read_csv(self.data_file)`.
- Prepares the data for writing to Google Sheets by combining the column headers and data values into a list of lists.
- Updates the specified worksheet with the prepared data using `self.worksheet.update('A1', data_list)`.

**Examples**:

```python
# Set the data file path and upload data
google_sheet_handler.data_file = Path('/mnt/data/google_extracted/your_data_file.csv')
google_sheet_handler.upload_data_to_sheet()