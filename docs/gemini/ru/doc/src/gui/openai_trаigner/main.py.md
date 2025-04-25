# Модуль `src.gui.openai_trаigner.main`

## Обзор

Модуль `src.gui.openai_trаigner.main` содержит класс `AssistantMainWindow`, отвечающий за создание графического интерфейса (GUI) для взаимодействия с AI-ассистентами. 

GUI предоставляет пользователю возможность вводить URL, открывать его в встроенном веб-браузере, а также сворачивать приложение в системный трей. 

## Подробнее

В модуле реализован класс `AssistantMainWindow` с использованием библиотеки `PyQt6`, которая обеспечивает создание кроссплатформенных GUI-приложений. 

## Классы

### `AssistantMainWindow`

**Описание**: Класс, реализующий главное окно приложения для взаимодействия с AI-ассистентами.

**Наследует**: 
 - `QMainWindow` (библиотека `PyQt6`)

**Атрибуты**:

 - `browser` (`QWebEngineView`):  Объект, представляющий встроенный веб-браузер. 
 - `profile` (`QWebEngineProfile`):  Объект, представляющий профиль пользователя выбранного браузера.
 - `title_bar` (`QWidget`):  Объект, представляющий верхнюю панель окна с кнопками управления. 
 - `url_input` (`QLineEdit`):  Поле для ввода URL.
 - `load_button` (`QPushButton`):  Кнопка для загрузки URL.
 - `minimize_button` (`QPushButton`):  Кнопка для сворачивания приложения в системный трей. 
 - `fullscreen_button` (`QPushButton`):  Кнопка для переключения окна в полноэкранный режим. 
 - `close_button` (`QPushButton`):  Кнопка для закрытия окна. 
 - `tray_icon` (`QSystemTrayIcon`):  Иконка приложения в системном трее.
 - `tray_menu` (`QMenu`):  Контекстное меню для иконки приложения в системном трее. 
 - `url_menu` (`QMenu`):  Меню для выбора сервисов Google. 
 - `model_menu` (`QMenu`):  Меню для выбора модели AI-ассистента. 
 - `url_button` (`QPushButton`):  Кнопка для открытия меню выбора сервисов Google. 
 - `model_button` (`QPushButton`):  Кнопка для открытия меню выбора модели AI-ассистента.

**Методы**:

 - `__init__()`:  Инициализирует объект класса `AssistantMainWindow`. Создает все необходимые компоненты GUI, настраивает layout и события (например, нажатие кнопок). 
 - `ask_for_browser()`:  Запрашивает у пользователя название браузера, который используется по умолчанию.
 - `load_url(url: str = None)`:  Загружает URL в встроенный веб-браузер. 
 - `hide_to_tray()`:  Сворачивает приложение в системный трей. 
 - `quit_app()`:  Закрывает приложение.
 - `closeEvent(event)`:  Переопределяет стандартный метод `closeEvent` для скрытия окна в трей при закрытии через "X" окна.

**Пример**:

```python
# Создание экземпляра класса AssistantMainWindow
window = AssistantMainWindow()
# Отображение окна
window.show()
```


## Методы класса

### `load_url`

```python
    def load_url(self, url: str = None):
        """
        Загружает URL в встроенный веб-браузер.

        Args:
            url (str, optional): URL для загрузки. По умолчанию `None`, 
            в этом случае URL берётся из поля ввода `self.url_input`.

        Returns:
            None.

        Raises:
            None.

        Example:
            >>> window.load_url("https://www.google.com/")
            >>> window.load_url() # загружает URL из поля ввода
        """
        url = self.url_input.text() if not url else url

        if url:
            if not url.startswith("http"):
                url = "http://" + url  # Добавляем http, если не указано
            self.browser.setUrl(QUrl(url))
```

### `hide_to_tray`

```python
    def hide_to_tray(self):
        """
        Сворачивает приложение в системный трей.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.

        Example:
            >>> window.hide_to_tray()
        """
        self.hide()
```

### `quit_app`

```python
    def quit_app(self):
        """
        Закрывает приложение.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.

        Example:
            >>> window.quit_app()
        """
        self.tray_icon.hide()
        QApplication.quit()
```


## Параметры класса

 - `browser_choice` (str):  Название браузера, выбранного пользователем (`Chrome`, `Firefox`, `Edge`).
 - `profile_path` (str):  Путь к папке профиля пользователя выбранного браузера.
 - `url` (str):  URL для загрузки.
 - `choice` (str):  Название выбранного браузера.
 - `ok` (bool):  Флаг, указывающий, была ли кнопка "OK" нажата в диалоговом окне выбора браузера.

## Примеры

```python
from src.gui.openai_trаigner.main import AssistantMainWindow

# Создание экземпляра класса AssistantMainWindow
window = AssistantMainWindow()

# Отображение окна
window.show()

# Загрузка URL
window.load_url("https://www.google.com/")

# Сворачивание в системный трей
window.hide_to_tray()

# Выход из приложения
window.quit_app()