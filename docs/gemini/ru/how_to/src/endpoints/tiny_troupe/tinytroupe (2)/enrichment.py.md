## Как использовать блок кода `TinyEnricher`
=========================================================================================

Описание
-------------------------
Блок кода `TinyEnricher`  предназначен для обогащения контента с использованием модели машинного обучения. Он использует информацию о требованиях,  контексте и типе контента для генерации улучшенного текста. 

Шаги выполнения
-------------------------
1. **Инициализация:**  Создается объект `TinyEnricher`, который хранит информацию о контексте и параметрах для использования прошлых результатов в текущем контексте.
2. **Формирование конфигурации:** Создается словарь `rendering_configs`, содержащий все необходимые данные для рендеринга шаблонов. Включает требования, контент, тип контента, информацию о контексте и кэш контекста.
3. **Формирование запросов:** Функция `utils.compose_initial_LLM_messages_with_templates`  создает начальные сообщения для модели машинного обучения, используя шаблоны `enricher.system.mustache` и `enricher.user.mustache` с использованием `rendering_configs`.
4. **Отправка запроса:** Функция `openai_utils.client().send_message` отправляет сообщения модели машинного обучения с заданной температурой (0.4) для генерации ответа.
5. **Обработка ответа:** Извлекается  текст ответа (`next_message["content"]`) и вызывается функция `utils.extract_code_block`, чтобы получить блок кода.
6. **Возврат результата:**  Возвращает полученный блок кода или `None`, если ответ не был получен.

Пример использования
-------------------------

```python
from tinytroupe.enrichment import TinyEnricher

# Создаем объект TinyEnricher
enricher = TinyEnricher()

# Задаем требования, контент и тип контента
requirements = "Пожалуйста, перефразируй этот текст, чтобы он звучал более формально."
content = "Привет, как дела? Я сегодня не очень хорошо себя чувствую."
content_type = "text"

# Добавляем контекст (опционально)
context_info = "Это сообщение от друга, который не очень хорошо себя чувствует."

# Вызываем функцию enrich_content
result = enricher.enrich_content(requirements, content, content_type, context_info)

# Выводим результат
print(result)
```