### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код добавляет или удаляет пункт контекстного меню "hypo AI assistant" для фона рабочего стола и папок в Windows, используя PyQt6 для графического интерфейса и реестр Windows для внесения изменений.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `winreg` для взаимодействия с реестром Windows, `os` для работы с путями, `PyQt6` для создания графического интерфейса, `header` и `src.gs` как пользовательские модули для настроек и структуры проекта.

2. **Функция `add_context_menu_item()`**:
   - Определяется путь в реестре, где будет создан ключ для нового пункта меню.
   - Используется `reg.CreateKey` для создания ключа `hypo_AI_assistant` в `HKEY_CLASSES_ROOT\\Directory\\Background\\shell`.
   - Устанавливается отображаемое имя пункта меню через `reg.SetValue`.
   - Создается подраздел `command` для определения действия при выборе пункта меню.
   - Проверяется существование скрипта `main.py`, который будет запускаться при выборе пункта меню. Если скрипт не найден, отображается сообщение об ошибке.
   - Устанавливается команда для запуска скрипта Python с передачей аргумента `%1` (текущий путь) через `reg.SetValue`.
   - Выводится сообщение об успешном добавлении пункта меню или сообщение об ошибке в случае неудачи.

3. **Функция `remove_context_menu_item()`**:
   - Определяется путь к ключу реестра, который нужно удалить.
   - Используется `reg.DeleteKey` для удаления ключа `hypo_AI_assistant` из реестра.
   - Выводится сообщение об успешном удалении пункта меню, предупреждение, если пункт меню не найден, или сообщение об ошибке в случае неудачи.

4. **Класс `ContextMenuManager`**:
   - Создается класс `ContextMenuManager`, наследуемый от `QtWidgets.QWidget`, для управления главным окном приложения.
   - В методе `initUI` создаются кнопки "Добавить пункт меню", "Удалить пункт меню" и "Выход".
   - К кнопкам привязываются функции `add_context_menu_item`, `remove_context_menu_item` и `self.close` соответственно.
   - Размещает кнопки вертикально в окне.

5. **Запуск приложения**:
   - В блоке `if __name__ == "__main__":` создается экземпляр приложения `QtWidgets.QApplication`.
   - Создается и отображается главное окно `ContextMenuManager`.
   - Запускается цикл обработки событий приложения (`app.exec()`).

Пример использования
-------------------------

```python
    import sys
    from PyQt6 import QtWidgets
    from src.gui.context_menu.qt6.main import ContextMenuManager

    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        window = ContextMenuManager()
        window.show()
        sys.exit(app.exec())
```
```python
## \file /src/gui/context_menu/qt6/main.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.gui.context_menu.qt6
	:platform: Windows, Unix
	:synopsis: Module to add or remove context menu items for the desktop and folder background using PyQt6.

This module provides functions to add or remove a custom context menu item called 
'hypo AI assistant' for the background of directories and the desktop in Windows Explorer.
It uses the Windows Registry to achieve this, with paths and logic implemented to target
the right-click menu on empty spaces (not on files or folders).
"""

import winreg as reg  # Module for interacting with Windows Registry
import os  # Module for OS path manipulation and checks
from PyQt6 import QtWidgets  # Module for GUI creation with PyQt6

import header  # Custom import, assuming it initializes settings or constants
from src import gs  # Custom import, likely for path settings or project structure


def add_context_menu_item() -> None:
    """Adds a context menu item to the desktop and folder background.

    This function creates a registry key under 'HKEY_CLASSES_ROOT\\Directory\\Background\\shell' 
    to add a menu item named 'hypo AI assistant' to the background context menu in Windows Explorer.
    The item runs a Python script when selected.

    Registry Path Details:
        - `key_path`: Directory\\Background\\shell\\hypo_AI_assistant
            This path adds the context menu item to the background of folders and 
            the desktop, allowing users to trigger it when right-clicking on empty space.
        
        - `command_key`: Directory\\Background\\shell\\hypo_AI_assistant\\command
            This subkey specifies the action for the context menu item and links it to a script 
            or command (in this case, a Python script).
    
    Raises:
        Displays an error message if the script file does not exist.
    """
    # Registry path for adding a menu item to the background of folders and the desktop
    key_path: str = r"Directory\\Background\\shell\\hypo_AI_assistant"

    try:
        # Create a new key for the menu item under the specified registry path
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path) as key:
            reg.SetValue(key, "", reg.REG_SZ, "hypo AI assistant")  # Display name of the context menu item

            # Sub-key to define the command to run when the menu item is selected
            command_key: str = rf"{key_path}\\command"
            with reg.CreateKey(reg.HKEY_CLASSES_ROOT, command_key) as command:
                # Define the path to the Python script that will be executed
                command_path: Path = gs.path.src / 'gui' / 'context_menu' / 'main.py'  # Path to the script
                if not os.path.exists(command_path):
                    QtWidgets.QMessageBox.critical(None, "Ошибка", f"Файл {command_path} не найден.")
                    return

                # Set the command to execute the script with Python when the context menu item is clicked
                reg.SetValue(command, "", reg.REG_SZ, f"python \"{command_path}\" \"%1\"")

        # Confirmation message for successful addition
        QtWidgets.QMessageBox.information(None, "Успех", "Пункт меню успешно добавлен!")
    except Exception as ex:
        # Display any error that occurs during the registry modification
        QtWidgets.QMessageBox.critical(None, "Ошибка", f"Ошибка: {ex}")


def remove_context_menu_item() -> None:
    """Removes the 'hypo AI assistant' context menu item.

    This function deletes the registry key responsible for displaying the custom
    context menu item, effectively removing it from the background context menu.

    Registry Path Details:
        - `key_path`: Directory\\Background\\shell\\hypo_AI_assistant
            This path targets the custom context menu item and deletes it from the 
            background context menu of the desktop and folders.
    
    Raises:
        Displays a warning if the menu item does not exist, and an error if the operation fails.
    """
    # Registry path for the custom menu item
    key_path: str = r"Directory\\Background\\shell\\hypo_AI_assistant"

    try:
        # Attempt to delete the registry key associated with the context menu item
        reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_path)
        # Confirmation message for successful removal
        QtWidgets.QMessageBox.information(None, "Успех", "Пункт меню успешно удален!")
    except FileNotFoundError:
        # Warn if the context menu item was not found
        QtWidgets.QMessageBox.warning(None, "Предупреждение", "Пункт меню не найден.")
    except Exception as e:
        # Display any other errors encountered during the key deletion
        QtWidgets.QMessageBox.critical(None, "Ошибка", f"Ошибка: {e}")


class ContextMenuManager(QtWidgets.QWidget):
    """Main application window for managing the custom context menu item."""

    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self) -> None:
        """Initializes the user interface with buttons to add, remove, or exit."""
        # Set the window title
        self.setWindowTitle("Управление контекстным меню")

        # Create a layout to organize buttons vertically
        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()

        # Button to add the custom context menu item
        add_button: QtWidgets.QPushButton = QtWidgets.QPushButton("Добавить пункт меню")
        add_button.clicked.connect(add_context_menu_item)
        layout.addWidget(add_button)

        # Button to remove the custom context menu item
        remove_button: QtWidgets.QPushButton = QtWidgets.QPushButton("Удалить пункт меню")
        remove_button.clicked.connect(remove_context_menu_item)
        layout.addWidget(remove_button)

        # Button to exit the program
        exit_button: QtWidgets.QPushButton = QtWidgets.QPushButton("Выход")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        # Apply the layout to the main window
        self.setLayout(layout)


if __name__ == "__main__":
    # Initialize the Qt application
    app = QtWidgets.QApplication([])

    # Create and display the main application window
    window = ContextMenuManager()
    window.show()

    # Execute the application event loop
    app.exec()