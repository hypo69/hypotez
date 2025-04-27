# Module: `hypotez/src/endpoints/bots/telegram/digital_market/bot/admin/kbs.py`

## Overview

This module contains functions for creating inline keyboard markup for the Telegram bot's admin panel. The keyboard markup is used for navigating between various features and actions within the admin panel.

## Details

This file is part of the `hypotez` project, which provides a framework for developing Telegram bots for digital markets. This specific file focuses on creating keyboard markup for the admin panel, offering interactive options for managing products, statistics, and general administration tasks.

## Table of Contents

- [Functions](#functions)
    - [catalog_admin_kb](#catalog_admin_kb)
    - [admin_send_file_kb](#admin_send_file_kb)
    - [admin_kb](#admin_kb)
    - [admin_kb_back](#admin_kb_back)
    - [dell_product_kb](#dell_product_kb)
    - [product_management_kb](#product_management_kb)
    - [cancel_kb_inline](#cancel_kb_inline)
    - [admin_confirm_kb](#admin_confirm_kb)

## Functions

### `catalog_admin_kb`

**Purpose**: Creates an inline keyboard markup for selecting categories within the catalog.

**Parameters**:

- `catalog_data` (List[Category]): A list of `Category` objects representing available categories.

**Returns**:

- InlineKeyboardMarkup: An inline keyboard markup with buttons for each category and an "Отмена" (Cancel) button.

**How the Function Works**:

1.  The function iterates through the provided `catalog_data`, creating a button for each category with the category name as the text and the category ID as the callback data.
2.  An "Отмена" (Cancel) button is added to the keyboard, with "admin_panel" as the callback data.
3.  The keyboard buttons are arranged in two columns (`kb.adjust(2)`).

### `admin_send_file_kb`

**Purpose**: Creates an inline keyboard markup for choosing whether to send a file or not.

**Parameters**:

- None

**Returns**:

- InlineKeyboardMarkup: An inline keyboard markup with buttons for "Без файла" (Without file) and "Отмена" (Cancel).

**How the Function Works**:

1.  The function creates two buttons: "Без файла" (Without file) and "Отмена" (Cancel).
2.  The "Без файла" button has the callback data "without_file", and the "Отмена" button has "admin_panel".
3.  The buttons are arranged in two columns (`kb.adjust(2)`).

### `admin_kb`

**Purpose**: Creates an inline keyboard markup for the main admin panel.

**Parameters**:

- None

**Returns**:

- InlineKeyboardMarkup: An inline keyboard markup with buttons for "📊 Статистика" (Statistics), "🛍️ Управлять товарами" (Manage products), and "🏠 На главную" (Home).

**How the Function Works**:

1.  The function creates buttons for "📊 Статистика" (Statistics), "🛍️ Управлять товарами" (Manage products), and "🏠 На главную" (Home).
2.  Each button is assigned a corresponding callback data: "statistic", "process_products", and "home", respectively.
3.  The buttons are arranged in two columns (`kb.adjust(2)`).

### `admin_kb_back`

**Purpose**: Creates an inline keyboard markup for going back to the admin panel or the main screen.

**Parameters**:

- None

**Returns**:

- InlineKeyboardMarkup: An inline keyboard markup with buttons for "⚙️ Админ панель" (Admin Panel) and "🏠 На главную" (Home).

**How the Function Works**:

1.  The function creates two buttons: "⚙️ Админ панель" (Admin Panel) and "🏠 На главную" (Home).
2.  Each button is assigned a corresponding callback data: "admin_panel" and "home", respectively.
3.  The buttons are arranged in one column (`kb.adjust(1)`).

### `dell_product_kb`

**Purpose**: Creates an inline keyboard markup for confirming deletion of a product.

**Parameters**:

- `product_id` (int): The ID of the product to be deleted.

**Returns**:

- InlineKeyboardMarkup: An inline keyboard markup with buttons for "🗑️ Удалить" (Delete), "⚙️ Админ панель" (Admin Panel), and "🏠 На главную" (Home).

**How the Function Works**:

1.  The function creates three buttons: "🗑️ Удалить" (Delete), "⚙️ Админ панель" (Admin Panel), and "🏠 На главную" (Home).
2.  The "🗑️ Удалить" button has the callback data `f"dell_{product_id}"`. The "⚙️ Админ панель" and "🏠 На главную" buttons have the callback data "admin_panel" and "home", respectively.
3.  The buttons are arranged in a specific layout with two buttons in the first two rows and one button in the third row (`kb.adjust(2, 2, 1)`).

### `product_management_kb`

**Purpose**: Creates an inline keyboard markup for managing products within the admin panel.

**Parameters**:

- None

**Returns**:

- InlineKeyboardMarkup: An inline keyboard markup with buttons for "➕ Добавить товар" (Add product), "🗑️ Удалить товар" (Delete product), "⚙️ Админ панель" (Admin Panel), and "🏠 На главную" (Home).

**How the Function Works**:

1.  The function creates four buttons: "➕ Добавить товар" (Add product), "🗑️ Удалить товар" (Delete product), "⚙️ Админ панель" (Admin Panel), and "🏠 На главную" (Home).
2.  Each button is assigned a corresponding callback data: "add_product", "delete_product", "admin_panel", and "home", respectively.
3.  The buttons are arranged in a specific layout with two buttons in the first two rows and one button in the third row (`kb.adjust(2, 2, 1)`).

### `cancel_kb_inline`

**Purpose**: Creates an inline keyboard markup with a single "Отмена" (Cancel) button.

**Parameters**:

- None

**Returns**:

- InlineKeyboardMarkup: An inline keyboard markup with a single "Отмена" (Cancel) button.

**How the Function Works**:

1.  The function creates a single button: "Отмена" (Cancel).
2.  The button has the callback data "cancel".

### `admin_confirm_kb`

**Purpose**: Creates an inline keyboard markup for confirming an action.

**Parameters**:

- None

**Returns**:

- InlineKeyboardMarkup: An inline keyboard markup with buttons for "Все верно" (All correct) and "Отмена" (Cancel).

**How the Function Works**:

1.  The function creates two buttons: "Все верно" (All correct) and "Отмена" (Cancel).
2.  The "Все верно" button has the callback data "confirm_add", and the "Отмена" button has "admin_panel".
3.  The buttons are arranged in one column (`kb.adjust(1)`).