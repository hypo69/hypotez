# Module for Managing and Posting Facebook Events

## Overview

This module is designed for managing the retrieval and posting of event data to Facebook. It interacts with JSON files containing event details, processes them, and posts the corresponding messages to Facebook groups. Events are stored in a directory structure under the `facebook/events` folder.

## More Details

This module automates the process of posting events to Facebook groups. It reads event details from JSON files, iterates through a list of Facebook groups, and posts the event to each group. The module uses a `FacebookPromoter` class to handle the actual posting process.

## Table of Contents

- [Functions](#Functions)
  - [`post_events`](#post_events)
  - [`post_to_my_group`](#post_to_my_group)

## Functions

### `post_events`

```python
def post_events():
    """Обрабатывает и отправляет мероприятия на Facebook.

    Функция получает данные о мероприятиях из указанной директории, загружает детали мероприятий из JSON-файлов
    и отправляет их на Facebook. Мероприятия хранятся в структуре директорий под папкой `facebook/events`.

    Raises:
        FileNotFoundError: Если JSON-файл с информацией о мероприятии отсутствует.
    """
```

**Purpose**: Processes and posts events to Facebook.

**How it works**:
1.  Initializes a Chrome driver instance.
2.  Retrieves directory names of events from the `aliexpress/events` directory in Google Drive.
3.  Retrieves filenames of group files from the `facebook/groups` directory in Google Drive.
4.  Initializes a `FacebookPromoter` with the driver and group file paths.
5.  Iterates through each event directory, loads the event details from the JSON file, and uses the promoter to process and post the event to the specified Facebook groups.

**Parameters**:

*   None

**Returns**:

*   None

**Internal functions**: None

**Examples**:

```python
post_events()
```

### `post_to_my_group`

```python
def post_to_my_group(event):
    """"""
```

**Purpose**: Posts an event to a predefined Facebook group.

**How it works**:
1.  Loads group details from the `my_managed_groups.json` file in the `facebook/groups` directory in Google Drive.
2.  Initializes a Chrome driver instance.
3.  Iterates through each group in the loaded group data.
4.  Navigates to the event URL for each group.
5.  Calls the `post_event` function to post the event to the group.

**Parameters**:

*   `event`: The event data to be posted.

**Returns**:

*   None

**Internal functions**: None

**Examples**:

```python
event = j_loads_ns(gs.path.google_drive / 'aliexpress' / 'events'  / 'sep_11_2024_over60_pricedown' / 'sep_11_2024_over60_pricedown.json')
post_to_my_group(event)
```