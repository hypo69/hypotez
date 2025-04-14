# Модуль `converstions_parser.py`

## Обзор

Модуль предназначен для извлечения бесед из HTML-файлов, предположительно содержащих историю чатов, с использованием библиотеки `BeautifulSoup`. Он предоставляет функцию-генератор для последовательного извлечения содержимого каждого элемента `<div class="conversation">` из указанного файла.

## Подробней

Модуль `converstions_parser.py` играет роль парсера HTML-файлов, содержащих историю чатов. Он использует библиотеку `BeautifulSoup` для анализа структуры HTML и извлечения содержимого, заключенного в элементы `<div class="conversation">`. Это позволяет эффективно извлекать отдельные беседы из файла, что может быть полезно для анализа, обработки или экспорта данных чата.

## Функции

### `extract_conversations_from_html`

```python
def extract_conversations_from_html(file_path: Path):
    """Генератор, который читает один .html файл и извлекает все <div class="conversation">.

    Args:
        file_path (Path): Путь к .html файлу.
    """
    # Открываем файл и парсим его содержимое
    with file_path.open('r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        # Ищем все <div class="conversation">
        conversations = soup.find_all('div', class_='conversation')
        ...
    # Возвращаем каждую найденную conversation
    for conversation in conversations:
        yield conversation
```

**Назначение**: Извлекает все элементы `<div class="conversation">` из HTML-файла, используя генератор для экономии памяти.

**Параметры**:

-   `file_path` (Path): Путь к .html файлу, из которого нужно извлечь беседы.

**Возвращает**:

-   Генератор, который выдает поочередно каждый элемент `<div class="conversation">`, найденный в файле.

**Как работает функция**:

1.  Открывает HTML-файл, указанный в `file_path`, в режиме чтения с кодировкой UTF-8.
2.  Создает объект `BeautifulSoup` для парсинга содержимого файла.
3.  Ищет все элементы `<div class="conversation">` в HTML-структуре.
4.  Итерируется по найденным элементам и возвращает каждый из них с помощью `yield`, что делает функцию генератором.

**Примеры**:

```python
from pathlib import Path
from src import gs  # Предполагается, что gs определен в вашем проекте

file_path = Path(gs.path.data / 'chat_gpt' / 'chat.html')
for conversation in extract_conversations_from_html(file_path):
    print(conversation.prettify())