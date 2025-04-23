### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для добавления и удаления пункта контекстного меню "hypo AI assistant" в Windows Explorer (проводнике). Он предоставляет графический интерфейс пользователя (GUI) на основе tkinter для управления этими действиями.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - `winreg` используется для взаимодействия с реестром Windows.
   - `os` используется для работы с путями файлов.
   - `tkinter` используется для создания графического интерфейса.
   - `messagebox` из `tkinter` используется для отображения сообщений пользователю.
   - `header` и `src.gs` — это пользовательские модули, предполагается, что они содержат настройки и пути.
2. **Функция `add_context_menu_item()`**:
   - Определяет путь в реестре, где будет создан пункт меню.
   - Создает ключ реестра для пункта меню "hypo AI assistant".
   - Устанавливает отображаемое имя пункта меню.
   - Создает под-ключ `command`, который определяет команду для запуска при выборе пункта меню.
   - Проверяет существование скрипта `main.py`. Если скрипт не найден, отображается сообщение об ошибке.
   - Устанавливает команду для выполнения скрипта Python с передачей текущего пути в качестве аргумента.
   - Выводит сообщение об успешном добавлении пункта меню.
   - Обрабатывает возможные исключения и отображает сообщение об ошибке.
3. **Функция `remove_context_menu_item()`**:
   - Определяет путь в реестре, где находится пункт меню.
   - Удаляет ключ реестра, соответствующий пункту меню.
   - Выводит сообщение об успешном удалении пункта меню.
   - Обрабатывает исключение `FileNotFoundError`, если пункт меню не найден, и отображает предупреждение.
   - Обрабатывает другие возможные исключения и отображает сообщение об ошибке.
4. **Функция `create_gui()`**:
   - Создает основное окно GUI с заголовком "Управление контекстным меню".
   - Создает кнопки "Добавить пункт меню", "Удалить пункт меню" и "Выход".
   - Назначает командам кнопок вызов соответствующих функций (`add_context_menu_item`, `remove_context_menu_item`, `root.quit`).
   - Запускает основной цикл обработки событий GUI.
5. **Основной блок `if __name__ == "__main__":`**:
   - Запускает функцию `create_gui()`, когда скрипт запускается напрямую.

Пример использования
-------------------------

```python
## \file /src/gui/context_menu/tkinter/main.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.gui.context_menu.tkinter 
\t:platform: Windows, Unix
\t:synopsis:  Module to add or remove context menu items for the desktop and folder background.


This module provides functions to add or remove a custom context menu item called 
'hypo AI assistant' for the background of directories and the desktop in Windows Explorer.
It uses the Windows Registry to achieve this, with paths and logic implemented to target
the right-click menu on empty spaces (not on files or folders).
"""

import winreg as reg  # Module for interacting with Windows Registry
import os  # Module for OS path manipulation and checks
import tkinter as tk  # Module for GUI creation
from tkinter import messagebox  # Submodule for GUI message boxes

import header  # Custom import, assuming it initializes settings or constants
from src import gs  # Custom import, likely for path settings or project structure

def add_context_menu_item():
    """Функция создает пункт контекстного меню для фона рабочего стола и папок.

    Функция создает ключ в реестре `HKEY_CLASSES_ROOT\\Directory\\Background\\shell`, 
    для добавления пункта меню "hypo AI assistant" в контекстное меню фона в Windows Explorer.
    Пункт меню запускает Python-скрипт при выборе.

    Пути в реестре:
        - `key_path`: Directory\\Background\\shell\\hypo_AI_assistant
            Этот путь добавляет пункт контекстного меню в фон папок и рабочего стола, 
            позволяя пользователям запускать его при щелчке правой кнопкой мыши в пустом месте.
        
        - `command_key`: Directory\\Background\\shell\\hypo_AI_assistant\\command
            Этот подраздел определяет действие для пункта контекстного меню и связывает его со скриптом 
            или командой (в данном случае, Python-скрипт).
    
    Raises:
        Выводит сообщение об ошибке, если файл скрипта не существует.
    """

    # Путь в реестре для добавления пункта меню в фон папок и рабочего стола
    key_path = r"Directory\\Background\\shell\\hypo_AI_assistant"

    try:
        # Функция создает новый ключ для пункта меню в указанном пути реестра
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path) as key:
            reg.SetValue(key, "", reg.REG_SZ, "hypo AI assistant")  # Функция задает отображаемое имя пункта меню
            
            # Подраздел для определения команды, выполняемой при выборе пункта меню
            command_key = rf"{key_path}\\command"
            with reg.CreateKey(reg.HKEY_CLASSES_ROOT, command_key) as command:
                
                # Функция определяет путь к Python-скрипту, который будет выполнен
                command_path = gs.path.src / 'gui' / 'context_menu' / 'main.py'  # Путь к скрипту
                if not os.path.exists(command_path):
                    # Функция показывает ошибку, если скрипт не найден в указанном месте
                    messagebox.showerror("Ошибка", f"Файл {command_path} не найден.")
                    return
                
                # Функция устанавливает команду для выполнения скрипта с помощью Python при щелчке на пункте контекстного меню
                reg.SetValue(command, "", reg.REG_SZ, f"python \"{command_path}\" \"%1\"")
        
        # Сообщение об успешном добавлении
        messagebox.showinfo("Успех", "Пункт меню успешно добавлен!")
    except Exception as ex:
        # Функция отображает любую ошибку, возникающую при изменении реестра
        messagebox.showerror("Ошибка", f"Ошибка: {ex}")

def remove_context_menu_item():
    """Функция удаляет пункт контекстного меню "hypo AI assistant".

    Функция удаляет ключ реестра, который отвечает за отображение пользовательского
    пункта контекстного меню, тем самым удаляя его из контекстного меню фона.

    Пути в реестре:
        - `key_path`: Directory\\Background\\shell\\hypo_AI_assistant
            Этот путь предназначен для пользовательского пункта контекстного меню и удаляет его из
            контекстного меню фона рабочего стола и папок.
    
    Raises:
        Выводит предупреждение, если пункт меню не существует, и ошибку, если операция завершается неудачей.
    """

    # Путь в реестре для пользовательского пункта меню
    key_path = r"Directory\\Background\\shell\\hypo_AI_assistant"

    try:
        # Функция пытается удалить ключ реестра, связанный с пунктом контекстного меню
        reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_path)
        # Сообщение об успешном удалении
        messagebox.showinfo("Успех", "Пункт меню успешно удален!")
    except FileNotFoundError:
        # Предупреждение, если пункт контекстного меню не найден
        messagebox.showwarning("Предупреждение", "Пункт меню не найден.")
    except Exception as e:
        # Функция отображает любые другие ошибки, возникшие при удалении ключа
        messagebox.showerror("Ошибка", f"Ошибка: {e}")

def create_gui():
    """Функция создает простой графический интерфейс для управления пользовательским пунктом контекстного меню.

    Функция инициализирует GUI на основе tkinter с кнопками для добавления, удаления
    или выхода из менеджера меню. Она обеспечивает удобное взаимодействие с пользователем для изменений в реестре.
    """
    
    root = tk.Tk()  # Главное окно
    root.title("Управление контекстным меню")  # Заголовок окна

    # Кнопка для добавления пользовательского пункта контекстного меню
    add_button = tk.Button(root, text="Добавить пункт меню", command=add_context_menu_item)
    add_button.pack(pady=10)

    # Кнопка для удаления пользовательского пункта контекстного меню
    remove_button = tk.Button(root, text="Удалить пункт меню", command=remove_context_menu_item)
    remove_button.pack(pady=10)

    # Кнопка для выхода из программы
    exit_button = tk.Button(root, text="Выход", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()  # Функция запускает цикл обработки событий GUI

if __name__ == "__main__":
    create_gui()  # Функция запускает GUI-приложение