# Модуль для управления контекстным меню в Qt6

## Обзор

Модуль `main.py` предназначен для добавления и удаления пунктов контекстного меню для рабочего стола и фона папок с использованием PyQt6. Он предоставляет графический интерфейс для управления пользовательским пунктом контекстного меню "hypo AI assistant", которое добавляется в контекстное меню фона директорий и рабочего стола в Windows Explorer.

## Подробнее

Модуль использует реестр Windows для добавления или удаления пунктов контекстного меню. Логика реализована таким образом, чтобы пункт меню появлялся при клике правой кнопкой мыши на пустом месте (не на файлах или папках).

## Классы

### `ContextMenuManager`

**Описание**: Основной класс приложения для управления пунктами контекстного меню.

**Наследует**: `QtWidgets.QWidget`

**Атрибуты**:
- `self`: экземпляр класса `ContextMenuManager`.

**Методы**:
- `__init__(self)`: Инициализирует класс `ContextMenuManager` и вызывает метод `initUI` для инициализации пользовательского интерфейса.
- `initUI(self)`: Инициализирует пользовательский интерфейс с кнопками для добавления, удаления и выхода из приложения.

#### `__init__`
```python
    def __init__(self):
        super().__init__()
        self.initUI()
```
- **Назначение**: Инициализирует класс `ContextMenuManager`, вызывая конструктор родительского класса `QtWidgets.QWidget` и метод `initUI` для инициализации пользовательского интерфейса.
- **Как работает функция**:
    1. Вызывает конструктор базового класса `QtWidgets.QWidget` с помощью `super().__init__()`.
    2. Вызывает метод `self.initUI()` для инициализации пользовательского интерфейса.

#### `initUI`
```python
    def initUI(self):
        """Initializes the user interface with buttons to add, remove, or exit."""
        
        # Set the window title
        self.setWindowTitle("Управление контекстным меню")
        
        # Create a layout to organize buttons vertically
        layout = QtWidgets.QVBoxLayout()

        # Button to add the custom context menu item
        add_button = QtWidgets.QPushButton("Добавить пункт меню")
        add_button.clicked.connect(add_context_menu_item)
        layout.addWidget(add_button)

        # Button to remove the custom context menu item
        remove_button = QtWidgets.QPushButton("Удалить пункт меню")
        remove_button.clicked.connect(remove_context_menu_item)
        layout.addWidget(remove_button)

        # Button to exit the program
        exit_button = QtWidgets.QPushButton("Выход")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        # Apply the layout to the main window
        self.setLayout(layout)
```
- **Назначение**: Инициализирует пользовательский интерфейс приложения, создавая кнопки для добавления, удаления и выхода из контекстного меню.
- **Как работает функция**:
    1. Устанавливает заголовок окна на "Управление контекстным меню" с помощью `self.setWindowTitle("Управление контекстным меню")`.
    2. Создает вертикальный макет (`QVBoxLayout`) для организации кнопок в окне.
    3. Создает кнопку "Добавить пункт меню", назначает ей функцию `add_context_menu_item` при нажатии и добавляет её в макет.
    4. Создает кнопку "Удалить пункт меню", назначает ей функцию `remove_context_menu_item` при нажатии и добавляет её в макет.
    5. Создает кнопку "Выход", назначает ей функцию `self.close` (закрытие окна) при нажатии и добавляет её в макет.
    6. Устанавливает созданный макет в качестве основного макета для окна приложения с помощью `self.setLayout(layout)`.

## Функции

### `add_context_menu_item`

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

**Назначение**: Добавляет пункт контекстного меню "hypo AI assistant" для фона рабочего стола и папок.

**Как работает функция**:
1. Определяет путь в реестре, где будет создан ключ для нового пункта меню (`key_path`).
2. Использует `reg.CreateKey` для создания ключа в `HKEY_CLASSES_ROOT`.
3. Устанавливает значение по умолчанию для созданного ключа, которое является отображаемым именем пункта меню ("hypo AI assistant").
4. Создает подраздел `command` для указания выполняемой команды при выборе пункта меню.
5. Определяет путь к Python-скрипту, который будет выполняться (`command_path`).
6. Проверяет существование файла скрипта и отображает сообщение об ошибке, если файл не найден.
7. Устанавливает команду для выполнения скрипта с использованием Python и передает путь к скрипту в качестве аргумента.
8. Отображает сообщение об успешном добавлении пункта меню.
9. В случае возникновения исключений отображает сообщение об ошибке.

**Примеры**:
```python
add_context_menu_item()
```
### `remove_context_menu_item`

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

**Назначение**: Удаляет пункт контекстного меню "hypo AI assistant".

**Как работает функция**:
1. Определяет путь в реестре, где расположен ключ пункта меню (`key_path`).
2. Использует `reg.DeleteKey` для удаления ключа.
3. Отображает сообщение об успешном удалении пункта меню.
4. В случае, если ключ не найден, отображает предупреждение.
5. В случае возникновения других исключений, отображает сообщение об ошибке.

**Примеры**:
```python
remove_context_menu_item()
```
```markdown