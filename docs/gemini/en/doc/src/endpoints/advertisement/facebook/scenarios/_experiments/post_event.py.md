# Module for Managing Facebook Event Posts
## Overview
This module manages the retrieval and posting of Facebook event data. It interacts with JSON files containing event data, processes them, and sends corresponding messages to Facebook groups. 
## Details
The module utilizes the `FacebookPromoter` class to handle the posting process. Events are stored in a directory structure within the `facebook/events` folder. The script iterates through the event directories, reads the event details from their JSON files, and sends them to Facebook groups.
## Classes
### `FacebookPromoter`
**Description**: The `FacebookPromoter` class encapsulates the logic for posting Facebook events. It interacts with Facebook groups and handles event posting.
**Inherits**: No inheritance.
**Attributes**:
- `d` (Driver): A driver instance (Chrome) used for navigating and interacting with the Facebook website.
- `group_file_paths` (list): A list of file paths for JSON files containing information about Facebook groups to target for posting.
**Methods**:
- `process_groups`: Processes a list of events and posts them to the specified Facebook groups.
## Functions
### `post_events`
**Purpose**: Processes and posts events to Facebook groups.
**Parameters**: None.
**Returns**: None.
**Raises Exceptions**:
- `FileNotFoundError`: If the JSON file with event information is not found.
**How the Function Works**:
- The function iterates through event directories located in the `facebook/events` folder.
- It loads event data from the JSON files associated with each directory.
- For each event, it calls the `process_groups` method of the `FacebookPromoter` class to post it to the designated Facebook groups.
**Examples**:
```python
post_events()
```
### `post_to_my_group`
**Purpose**: Posts an event to specific groups.
**Parameters**:
- `event`: A dictionary containing event data.
**Returns**: None.
**Raises Exceptions**: None.
**How the Function Works**:
- The function loads group information from the `my_managed_groups.json` file.
- It iterates through each group in the file.
- For each group, it retrieves the event URL and posts the `event` to the group using the `post_event` function.
**Examples**:
```python
event = j_loads_ns(gs.path.google_drive / 'aliexpress' / 'events'  / 'sep_11_2024_over60_pricedown' / 'sep_11_2024_over60_pricedown.json')
post_to_my_group(event)
```
## Parameter Details
- `event_file`: This parameter represents the filename of the JSON file containing event data. It is used to identify and load the event information from the appropriate file.
- `gs.path.google_drive / 'aliexpress' / 'events'  / event_file / f'{event_file}.json'`: This path string is used to construct the full path to the JSON file containing event data. It combines the Google Drive root path, the 'aliexpress' folder, the 'events' folder, the `event_file` name, and the filename with the `.json` extension.
- `events`: This parameter represents a list of dictionaries containing event data. It is used to pass multiple event details to the `process_groups` function for posting to Facebook groups.
- `group_file_paths`: This parameter represents a list of file paths for JSON files containing information about Facebook groups. It is used to specify which groups to target for posting the events.
- `is_event`: This parameter indicates whether the provided data is an event or not. This is used by the `process_groups` function to determine how to process and handle the data.
- `group_url`: This parameter represents the URL of a specific Facebook group. It is used to identify and access the target group for posting the event.
- `group`: This parameter represents a dictionary containing information about a specific Facebook group. It may include details such as the group's name, URL, and other relevant information.
- `event`: This parameter represents a dictionary containing event data. It is used to pass the event details to the `post_event` function for posting to the Facebook group.
- `d`: This parameter represents a driver instance used for interacting with the Facebook website. It provides the necessary functionality for navigating and performing actions on the site.
- `groups_ns`: This parameter represents a dictionary containing information about multiple Facebook groups. It is loaded from the `my_managed_groups.json` file.
- `close_banner`: This parameter is a dictionary representing a web element locator on the Facebook website. It's used to locate and interact with the element.

## Examples
```python
# Creating a driver instance (example with Chrome)
driver = Driver(Chrome)
```
```python
close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```
## Key Points
- The module uses a `Driver` instance to interact with the Facebook website.
- The `process_groups` method of the `FacebookPromoter` class handles the event posting logic.
- The script utilizes the `j_loads_ns` function to load JSON data from files.
- The `pprint` function is used to display output in a readable format.
- Event information is retrieved from JSON files located in the `facebook/events` folder.
- The module interacts with Facebook groups using a list of group file paths.
- The `post_event` function handles the actual posting of events to Facebook groups.
- The script utilizes various file and path manipulation functions from the `src.utils` module.