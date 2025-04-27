## Как использовать блок кода `SpreadSheet(spreadsheet_name = '030724_men_summer_fashion')`

=========================================================================================

Описание
-------------------------
Этот блок кода создает объект класса `SpreadSheet`  с именем `ss`,  подключенный к Google-таблице с названием `030724_men_summer_fashion`. 

Шаги выполнения
-------------------------
1. **Импортируется модуль `header`.**
2. **Импортируется класс `SpreadSheet` из модуля `src.google`.**
3. **Создается экземпляр класса `SpreadSheet`  с именем `ss`.**
4. **В качестве аргумента при создании экземпляра `SpreadSheet` передается название Google-таблицы `spreadsheet_name = '030724_men_summer_fashion'`.**


Пример использования
-------------------------

```python
import header
from src.google import SpreadSheet

ss = SpreadSheet(spreadsheet_name = '030724_men_summer_fashion')
# После этого с помощью `ss` можно взаимодействовать с Google-таблицей.
# Например,  можно получить данные из таблицы:
data = ss.get_all_data()
print(data) 
```