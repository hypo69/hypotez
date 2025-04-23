### Как использовать класс `JupyterCampaignEditorWidgets`
=========================================================================================

Описание
-------------------------
Класс `JupyterCampaignEditorWidgets` предоставляет набор виджетов для взаимодействия с редактором кампаний AliExpress в Jupyter Notebook. Он позволяет выбирать кампании, категории и языки, а также выполнять действия, такие как инициализация редактора, сохранение кампании и отображение товаров.

Шаги выполнения
-------------------------
1. **Инициализация класса**:
   - Создайте экземпляр класса `JupyterCampaignEditorWidgets`. Это настроит все необходимые виджеты и установит значения по умолчанию.
   ```python
   editor_widgets: JupyterCampaignEditorWidgets = JupyterCampaignEditorWidgets()
   ```
2. **Отображение виджетов**:
   - Вызовите метод `display_widgets`, чтобы отобразить виджеты в Jupyter Notebook.
   ```python
   editor_widgets.display_widgets()
   ```
3. **Взаимодействие с виджетами**:
   - Используйте выпадающие списки для выбора имени кампании, категории и языка/валюты.
   - Нажмите кнопку "Initialize Campaign Editor", чтобы инициализировать редактор кампании с выбранными параметрами.
   - Нажмите кнопку "Save Campaign", чтобы сохранить кампанию и ее категории.
   - Нажмите кнопку "Show Products", чтобы отобразить товары в выбранной категории.
   - Нажмите кнопку "Open Google Spreadsheet", чтобы открыть Google Spreadsheet кампании в браузере.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.campaign.ali_campaign_editor_jupyter_widgets import JupyterCampaignEditorWidgets

# Инициализация виджетов редактора кампаний
editor_widgets: JupyterCampaignEditorWidgets = JupyterCampaignEditorWidgets()

# Отображение виджетов в Jupyter Notebook
editor_widgets.display_widgets()

# После выполнения этого кода в Jupyter Notebook отобразятся виджеты, с которыми можно взаимодействовать для управления кампаниями AliExpress.