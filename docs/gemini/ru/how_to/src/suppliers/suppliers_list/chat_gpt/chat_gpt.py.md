## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
[Блок кода определяет класс `ChatGpt`, который содержит метод `yeld_conversations_htmls`. Метод предназначен для итерации по файлам с расширением `*.html` в директории `conversations`, расположенной в директории `chat_gpt`, которая, в свою очередь, находится в директории `data`. Файлы `*.html` в директории `conversations` представляют собой записи диалогов.]

Шаги выполнения
-------------------------
1. [Инициализируется класс `ChatGpt`.]
2. [Вызывается метод `yeld_conversations_htmls`, который возвращает итератор по файлам с расширением `*.html` в директории `conversations`.]
3. [Итератор может быть использован для обработки каждого файла с помощью цикла `for`.]

Пример использования
-------------------------

```python
from src.suppliers.chat_gpt.chat_gpt import ChatGpt
from src.utils.file import recursively_read_text_files

chat_gpt = ChatGpt()

for conversation_html in chat_gpt.yeld_conversations_htmls():
    # Обработка файла с диалогом
    print(f'Обрабатываю файл: {conversation_html}')
    text = recursively_read_text_files(conversation_html)
    # дальнейшая обработка text
    print(text)
```