## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код обучает и сравнивает две модели ИИ: OpenAI и Gemini, на основе текстовых данных о названиях товаров с AliExpress.

Шаги выполнения
-------------------------
1. **Инициализация переменных**:
    - Задается путь к папке с файлами, содержащими названия товаров (`.txt`) на Google Drive.
    - Задается путь к файлу с системной инструкцией для моделей.
    - Считывается системная инструкция из файла.
    - Создаются объекты моделей OpenAI и Gemini с использованием системной инструкции.
2. **Итерация по файлам с названиями товаров**:
    - Цикл перебирает файлы с названиями товаров в папке на Google Drive.
    - Считывается содержимое каждого файла с названиями товаров.
    - Модели OpenAI и Gemini обрабатывают названия товаров и возвращают ответы.
3. **Обработка ответов моделей**:
    - ... 

Пример использования
-------------------------

```python
# Импортируем необходимые модули
from src import gs
from src.llm import OpenAIModel, GoogleGenerativeAi
from src.utils.file import recursively_get_filenames, read_text_file

# Задаем путь к папке с файлами названий товаров на Google Drive
product_titles_files:list = recursively_get_filenames(gs.path.google_drive / 'aliexpress' / 'campaigns', 'product_titles.txt')

# Задаем путь к файлу с системной инструкцией
system_instruction_path = gs.path.src / 'ai' / 'prompts' / 'aliexpress_campaign' / 'system_instruction.txt'

# Считываем системную инструкцию
system_instruction: str = read_text_file(system_instruction_path)

# Создаем объекты моделей OpenAI и Gemini
openai = OpenAIModel(system_instruction = system_instruction)
gemini = GoogleGenerativeAi(system_instruction = system_instruction)

# Цикл по файлам с названиями товаров
for file in product_titles_files:
    # Считываем названия товаров из файла
    product_titles = read_text_file(file)
    # Получаем ответы от моделей
    response_openai = openai.ask(product_titles)
    response_gemini = gemini.ask(product_titles)
    # ... (дальнейшая обработка ответов)
```

**Дополнительно**:
- Код предполагает, что у вас есть доступ к Google Drive и учетная запись OpenAI.
- В части кода, которая обозначена как `...`,  должна быть реализована логика обработки ответов моделей, например, сравнение результатов, анализ качества, сохранение ответов в файлы и т.д.
- Этот код является примером использования моделей OpenAI и Gemini для задач обучения на текстах с AliExpress. 
- Можно модифицировать этот код для решения других задач с использованием различных данных и системных инструкций.