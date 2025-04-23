# Модуль для добавления или удаления пунктов контекстного меню для рабочего стола и фона папок.

## Обзор

Модуль предоставляет функции для добавления или удаления пользовательского пункта контекстного меню под названием "hypo AI assistant" для фона каталогов и рабочего стола в проводнике Windows. Он использует реестр Windows для достижения этой цели, с путями и логикой, реализованными для нацеливания на контекстное меню правой кнопки мыши на пустых местах (не на файлах или папках).

## Подробнее

Этот модуль позволяет пользователям добавлять или удалять пункт "hypo AI assistant" в контекстное меню, которое появляется при щелчке правой кнопкой мыши на пустом месте рабочего стола или в папке. Это достигается путем манипулирования реестром Windows. Модуль также включает в себя простой графический интерфейс на основе `tkinter`, который позволяет пользователям легко добавлять, удалять или выходить из программы управления контекстным меню.

## Классы

### `Нет классов`

В этом модуле нет классов.

## Функции

### `add_context_menu_item`

**Назначение**: Добавляет пункт контекстного меню на рабочий стол и фон папок.

```python
def add_context_menu_item():
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
```

**Как работает функция**:

1.  Определяет путь в реестре, где будет создан новый пункт меню.
2.  Создает ключ реестра `hypo_AI_assistant` в `HKEY_CLASSES_ROOT\\Directory\\Background\\shell`.
3.  Устанавливает строковое значение для созданного ключа, определяющее отображаемое имя пункта меню ("hypo AI assistant").
4.  Создает подраздел `command`, который указывает, какую команду следует выполнить при выборе пункта меню.
5.  Проверяет существование скрипта, который должен быть запущен при выборе пункта меню.
6.  Устанавливает команду для выполнения скрипта Python с передачей пути к текущей директории в качестве аргумента.
7.  В случае успеха выводит сообщение об успешном добавлении пункта меню.
8.  В случае ошибки выводит сообщение об ошибке.

**Вызывает исключения**:

*   `FileNotFoundError`: Если файл скрипта не найден.
*   `Exception`: Если произошла ошибка при работе с реестром.

**Примеры**:

```python
# Пример вызова функции для добавления пункта меню
add_context_menu_item()
```

### `remove_context_menu_item`

**Назначение**: Удаляет пункт контекстного меню "hypo AI assistant".

```python
def remove_context_menu_item():
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
```

**Как работает функция**:

1.  Определяет путь в реестре, где находится пункт меню для удаления.
2.  Пытается удалить ключ реестра `hypo_AI_assistant` из `HKEY_CLASSES_ROOT\\Directory\\Background\\shell`.
3.  В случае успеха выводит сообщение об успешном удалении пункта меню.
4.  Если пункт меню не найден, выводит предупреждение.
5.  В случае ошибки выводит сообщение об ошибке.

**Вызывает исключения**:

*   `FileNotFoundError`: Если ключ реестра не найден.
*   `Exception`: Если произошла ошибка при работе с реестром.

**Примеры**:

```python
# Пример вызова функции для удаления пункта меню
remove_context_menu_item()
```

### `create_gui`

**Назначение**: Создает простой графический интерфейс для управления пользовательским пунктом контекстного меню.

```python
def create_gui():
    """Creates a simple GUI for managing the custom context menu item.

    This function initializes a tkinter-based GUI with buttons to add, remove,
    or exit the menu manager. It provides user-friendly interaction for registry
    modifications.
    """
```

**Как работает функция**:

1.  Инициализирует основное окно `tkinter`.
2.  Устанавливает заголовок окна.
3.  Создает кнопку "Добавить пункт меню", которая вызывает функцию `add_context_menu_item` при нажатии.
4.  Создает кнопку "Удалить пункт меню", которая вызывает функцию `remove_context_menu_item` при нажатии.
5.  Создает кнопку "Выход", которая закрывает окно при нажатии.
6.  Запускает основной цикл обработки событий GUI.

**Примеры**:

```python
# Пример вызова функции для создания GUI
create_gui()
```

### `__main__`

**Назначение**: Запускает GUI приложение.

**Как работает функция**:

1.  Проверяет, является ли текущий файл главным запускаемым скриптом.
2.  Если да, то вызывает функцию `create_gui()` для запуска графического интерфейса.

**Примеры**:

```python
if __name__ == "__main__":
    create_gui()