# Модуль `main`

## Обзор

Модуль `main` представляет собой основной интерфейс графического приложения для управления рекламными кампаниями, категориями и продуктами. Приложение предоставляет три вкладки: "JSON Editor", "Campaign Editor" и "Product Editor", каждая из которых отвечает за свою область функциональности. Модуль использует библиотеку PyQt6 для создания графического интерфейса и qasync для интеграции с асинхронным кодом.

## Подробнее

Этот модуль является отправной точкой для запуска графического интерфейса пользователя (GUI) приложения. Он объединяет различные редакторы (JSON, кампании, продукты) в единое окно с вкладками, предоставляя пользователю удобный способ управления данными и настройками, связанными с рекламными кампаниями.

## Классы

### `MainApp`

**Описание**: Основной класс приложения, представляющий главное окно с вкладками для редактирования JSON, кампаний и продуктов.

**Наследует**: `QtWidgets.QMainWindow`

**Атрибуты**:
- `tab_widget` (QtWidgets.QTabWidget): Виджет с вкладками для переключения между различными редакторами.
- `tab1` (QtWidgets.QWidget): Виджет, представляющий вкладку "JSON Editor".
- `promotion_app` (CampaignEditor): Экземпляр редактора кампаний, связанный с вкладкой "JSON Editor".
- `tab2` (QtWidgets.QWidget): Виджет, представляющий вкладку "Campaign Editor".
- `campaign_editor_app` (CategoryEditor): Экземпляр редактора категорий, связанный с вкладкой "Campaign Editor".
- `tab3` (QtWidgets.QWidget): Виджет, представляющий вкладку "Product Editor".
- `product_editor_app` (ProductEditor): Экземпляр редактора продуктов, связанный с вкладкой "Product Editor".

**Методы**:
- `__init__()`: Инициализирует главное окно приложения, создает вкладки и добавляет их в виджет с вкладками.
- `create_menubar()`: Создает строку меню с опциями для работы с файлами и командами редактирования.
- `open_file()`: Открывает диалоговое окно выбора файла для загрузки JSON-файла.
- `save_file()`: Сохраняет текущий файл в зависимости от выбранной вкладки.
- `exit_application()`: Завершает работу приложения.
- `copy()`: Копирует выделенный текст в буфер обмена.
- `paste()`: Вставляет текст из буфера обмена.
- `load_file(campaign_file: str)`: Загружает JSON-файл.

#### `__init__`
```python
def __init__(self):
    """ Initialize the main application with tabs """
    ...
```
**Назначение**: Инициализирует главное окно приложения с вкладками.

**Как работает функция**:
- Вызывает конструктор базового класса `QtWidgets.QMainWindow`.
- Устанавливает заголовок окна.
- Устанавливает размеры окна.
- Создает виджет с вкладками `QTabWidget`.
- Создает три вкладки (`QWidget`) для JSON Editor, Campaign Editor и Product Editor.
- Добавляет вкладки в виджет с вкладками.
- Создает экземпляры редакторов `CampaignEditor`, `CategoryEditor` и `ProductEditor` и связывает их с соответствующими вкладками.
- Вызывает метод `create_menubar()` для создания меню.

#### `create_menubar`
```python
def create_menubar(self):
    """ Create a menu bar with options for file operations and edit commands """
    ...
```
**Назначение**: Создает строку меню с опциями для работы с файлами и командами редактирования.

**Как работает функция**:
- Получает строку меню (`menuBar`) главного окна.
- Создает меню "File" и добавляет в него действия "Open", "Save" и "Exit".
- Создает меню "Edit" и добавляет в него действия "Copy" и "Paste".
- Связывает действия меню с соответствующими методами класса `MainApp` и редакторов.

#### `open_file`
```python
def open_file(self):
    """ Open a file dialog to select and load a JSON file """
    ...
```
**Назначение**: Открывает диалоговое окно выбора файла для загрузки JSON-файла.

**Как работает функция**:
- Создает экземпляр `QFileDialog`.
- Открывает диалоговое окно выбора файла с фильтром для JSON-файлов.
- Если файл выбран, вызывает метод `load_file()` для загрузки файла, если активна вкладка "JSON Editor".

#### `save_file`
```python
def save_file(self):
    """ Save the current file """
    ...
```
**Назначение**: Сохраняет текущий файл в зависимости от выбранной вкладки.

**Как работает функция**:
- Определяет индекс текущей активной вкладки.
- В зависимости от активной вкладки вызывает метод сохранения соответствующего редактора.

#### `exit_application`
```python
def exit_application(self):
    """ Exit the application """
    ...
```
**Назначение**: Завершает работу приложения.

**Как работает функция**:
- Вызывает метод `close()` для закрытия главного окна приложения.

#### `copy`
```python
def copy(self):
    """ Copy selected text to the clipboard """
    ...
```
**Назначение**: Копирует выделенный текст в буфер обмена.

**Как работает функция**:
- Получает виджет, находящийся в фокусе.
- Если виджет является текстовым редактором (`QLineEdit`, `QTextEdit`, `QPlainTextEdit`), вызывает метод `copy()` виджета для копирования текста в буфер обмена.
- Если виджет не является текстовым редактором, выводит предупреждающее сообщение.

#### `paste`
```python
def paste(self):
    """ Paste text from the clipboard """
    ...
```
**Назначение**: Вставляет текст из буфера обмена.

**Как работает функция**:
- Получает виджет, находящийся в фокусе.
- Если виджет является текстовым редактором (`QLineEdit`, `QTextEdit`, `QPlainTextEdit`), вызывает метод `paste()` виджета для вставки текста из буфера обмена.
- Если виджет не является текстовым редактором, выводит предупреждающее сообщение.

#### `load_file`
```python
def load_file(self, campaign_file: str):
    """ Load the JSON file """
    ...
```
**Назначение**: Загружает JSON-файл.

**Параметры**:
- `campaign_file` (str): Путь к JSON-файлу.

**Как работает функция**:
- Пытается загрузить JSON-файл с помощью метода `load_file()` редактора кампаний (`self.promotion_app`).
- В случае ошибки выводит сообщение об ошибке.

## Функции

### `main`
```python
def main():
    """ Initialize and run the application """
    ...
```
**Назначение**: Инициализирует и запускает приложение.

**Как работает функция**:
- Создает экземпляр `QApplication`.
- Создает цикл событий (`QEventLoop`) для асинхронных операций.
- Устанавливает цикл событий.
- Создает экземпляр главного окна приложения (`MainApp`).
- Отображает главное окно приложения.
- Запускает цикл событий для обработки событий GUI.

**Примеры**:
```python
if __name__ == "__main__":
    main()
```