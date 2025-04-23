### **Инструкция: Использование блока кода `ask_model.py`**

=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для запроса и обработки ответов от языковой модели Gemini на основе предоставленных инструкций и данных о товарах. Он включает в себя настройку модели, формирование запросов на разных языках (русский и иврит) и сохранение полученных ответов в формате JSON.

Шаги выполнения
-------------------------
1. **Инициализация переменных**:
   - Определяются пути к директориям и файлам, содержащим данные о товарах и инструкции для модели.
   - Загружаются данные о товарах из JSON-файла в список `products_list`.
   - Считываются инструкции для модели на русском и иврите из файлов `.md`.
   - Получается API-ключ для доступа к модели Gemini.

2. **Настройка модели Gemini**:
   - Создается экземпляр класса `GoogleGenerativeAi` с использованием API-ключа, системных инструкций и конфигурации генерации.

3. **Формирование запросов**:
   - Формируются запросы `q_ru` и `q_he` на русском и иврите соответственно, объединяющие инструкции и данные о товарах.

4. **Функция `model_ask`**:
   - Принимает язык (`lang`) и количество попыток (`attempts`) в качестве аргументов.
   - Вызывает метод `ask` у экземпляра модели, передавая сформированный запрос.
   - Обрабатывает ответ от модели:
     - Если ответ отсутствует, логируется ошибка.
     - Пытается распарсить ответ в формат JSON.
     - Если парсинг не удался, логируется ошибка и, если есть еще попытки, функция вызывается рекурсивно.
   - Возвращает распарсенный ответ в виде словаря.

5. **Запрос и сохранение ответов**:
   - Вызывается функция `model_ask` для русского и иврита, ответы сохраняются в отдельные JSON-файлы с указанием языка и текущего времени.

Пример использования
-------------------------

```python
from pathlib import Path
from src import gs
from src.llm.gemini.gemini import GoogleGenerativeAi
from src.utils.jjson import j_dumps, j_loads
from src.logger.logger import logger

# Путь к директории с тестовыми данными
test_directory = gs.path.external_storage / 'kazarinov' / 'mexironim' / '24_12_07_19_06_40_508' 
products_in_test_dir = test_directory /  'products'
products_list = j_loads(products_in_test_dir)

# Чтение инструкций для модели
system_instruction = Path(gs.path.endpoints / 'kazarinov' / 'instructions' / 'system_instruction_mexiron.md').read_text(encoding='UTF-8')
command_instruction_ru = Path(gs.path.endpoints / 'kazarinov' / 'instructions' / 'command_instruction_mexiron_ru.md').read_text(encoding='UTF-8')
command_instruction_he = Path(gs.path.endpoints / 'kazarinov' / 'instructions' / 'command_instruction_mexiron_he.md').read_text(encoding='UTF-8')

# Получение API-ключа
api_key = gs.credentials.gemini.kazarinov

# Инициализация модели
model = GoogleGenerativeAi(
    api_key=api_key,
    system_instruction=system_instruction,
    generation_config={'response_mime_type': 'application/json'}
)

# Формирование запросов
q_ru = command_instruction_ru + str(products_list)
q_he = command_instruction_he + str(products_list)

def model_ask(lang: str, attempts: int = 3) -> dict:
    """
    Запрашивает ответ от модели Gemini на указанном языке.

    Args:
        lang (str): Язык запроса ('ru' для русского, 'he' для иврита).
        attempts (int): Количество попыток запроса.

    Returns:
        dict: Ответ от модели в виде словаря или пустой словарь в случае ошибки.
    """
    global model, q_ru, q_he

    response = model.ask(q_ru if lang == 'ru' else q_he)
    if not response:
        logger.error("Нет ответа от модели")
        return {}

    response_dict = j_loads(response)
    if not response_dict:
        logger.error("Ошибка парсинга ")
        if attempts > 1:
            return model_ask(lang, attempts - 1)
        return {}

    return response_dict

# Получение и сохранение ответов
response_ru_dict = model_ask('ru')
j_dumps(response_ru_dict, gs.path.external_storage / 'kazarinov' / 'mexironim' / '24_12_07_19_06_40_508' / f'ru_{gs.now}.json')
response_he_dict = model_ask('he')
j_dumps(response_he_dict, gs.path.external_storage / 'kazarinov' / 'mexironim' / '24_12_07_19_06_40_508' / f'he_{gs.now}.json')