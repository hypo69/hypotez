## Как использовать блок кода `extract_conversations_from_html`

=========================================================================================

### Описание

-------------------------

Функция `extract_conversations_from_html` извлекает все блоки HTML-кода, содержащие диалоги из HTML-файла. 
Каждый блок соответствует одному разговору. 

### Шаги выполнения

-------------------------

1. **Открытие и парсинг HTML-файла**: Функция открывает файл по указанному пути (`file_path`) и парсит его содержимое с помощью библиотеки BeautifulSoup. 
2. **Поиск блоков с диалогами**: Функция ищет все элементы HTML с классом `conversation` (`<div class="conversation">`). 
3. **Возврат каждого блока диалога**: Функция возвращает каждый найденный блок HTML-кода, содержащий диалог, в виде итератора. 

### Пример использования

-------------------------

```python
from pathlib import Path
from src import gs
from src.suppliers.chat_gpt.converstions_parser import extract_conversations_from_html

# Путь к файлу с диалогами
file_path = Path(gs.path.data / 'chat_gpt' / 'chat.html')

# Извлечение всех блоков диалогов из файла
for conversation in extract_conversations_from_html(file_path):
    print(conversation.prettify())  # Печатаем содержимое каждого найденного диалога
```