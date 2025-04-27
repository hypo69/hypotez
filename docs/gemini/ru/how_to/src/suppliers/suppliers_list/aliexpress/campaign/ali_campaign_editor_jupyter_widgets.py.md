## Как использовать класс `JupyterCampaignEditorWidgets`

=========================================================================================

Описание
-------------------------
Класс `JupyterCampaignEditorWidgets` предоставляет набор виджетов для управления кампаниями AliExpress в Jupyter Notebook. Виджеты позволяют:

- Выбрать кампанию и категорию товаров.
- Установить язык и валюту для кампании.
- Инициализировать редактор кампаний.
- Сохранить кампанию.
- Отобразить товары в выбранной категории.
- Открыть Google Spreadsheet с данными кампании.

Шаги выполнения
-------------------------
1. Импортируйте класс `JupyterCampaignEditorWidgets`:

   ```python
   from src.suppliers.aliexpress.campaign import JupyterCampaignEditorWidgets
   ```

2. Создайте экземпляр класса:

   ```python
   editor_widgets = JupyterCampaignEditorWidgets()
   ```

3. Отобразите виджеты:

   ```python
   editor_widgets.display_widgets()
   ```
   - В Jupyter Notebook появятся виджеты для выбора кампании, категории, языка и валюты, а также кнопки для инициализации редактора, сохранения кампании, отображения товаров и открытия Google Spreadsheet.

4. Выберите кампанию, категорию, язык и валюту.

5. Нажмите кнопку "Initialize Campaign Editor", чтобы инициализировать редактор кампании.

6. Используйте редактор для управления кампанией AliExpress.

7. Нажмите кнопку "Save Campaign", чтобы сохранить изменения в кампании.

8. Нажмите кнопку "Show Products", чтобы отобразить товары в выбранной категории.

9. Нажмите кнопку "Open Google Spreadsheet", чтобы открыть Google Spreadsheet с данными кампании.

Пример использования
-------------------------

```python
from src.suppliers.aliexpress.campaign import JupyterCampaignEditorWidgets

editor_widgets = JupyterCampaignEditorWidgets()
editor_widgets.display_widgets()
```