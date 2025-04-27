## Как использовать класс ResultsExtractor
=========================================================================================

Описание
-------------------------
Класс ResultsExtractor предназначен для извлечения результатов из истории взаимодействия агентов TinyPerson и TinyWorld. Он использует OpenAI API для выполнения запросов на извлечение ключевых моментов из текста. 

Шаги выполнения
-------------------------
1. **Инициализация**:  Создается экземпляр класса ResultsExtractor, используя путь к шаблону запроса для извлечения, дефолтные цели извлечения,  ситуацию,  поля для извлечения и их подсказки, а также уровень детализации.
2. **Извлечение результатов**: Вызываются методы  `extract_results_from_agents` или `extract_results_from_world` для извлечения информации из агентов или мира.
3. **Обработка результатов**:  Извлеченные результаты сохраняются в кэш и могут быть сохранены в файл JSON с помощью метода `save_as_json`.

Пример использования
-------------------------

```python
from tinytroupe.extraction import ResultsExtractor

# Инициализация класса ResultsExtractor
extractor = ResultsExtractor(extraction_objective="Извлеките ключевые моменты из истории взаимодействия агентов.")

# Создаем список агентов 
agents = [
    TinyPerson(name="Alice", role="friend"),
    TinyPerson(name="Bob", role="enemy")
]

# Извлекаем результаты из списка агентов
results = extractor.extract_results_from_agents(agents, situation="Агенты обсуждают план.")

# Сохраняем результаты в файл
extractor.save_as_json("extraction_results.json")
```

**Дополнительные сведения:**

- **`extract_results_from_agents(agents, extraction_objective, situation, fields, fields_hints, verbose)`**: Извлекает информацию из списка агентов.
- **`extract_results_from_agent(tinyperson, extraction_objective, situation, fields, fields_hints, verbose)`**: Извлекает информацию из одного агента.
- **`extract_results_from_world(tinyworld, extraction_objective, situation, fields, fields_hints, verbose)`**: Извлекает информацию из мира TinyWorld.
- **`save_as_json(filename, verbose)`**: Сохраняет результаты извлечения в файл JSON.

**Важно**:

-  В классах `TinyPerson` и `TinyWorld` должна быть доступна история взаимодействия агентов.
- Класс `ResultsExtractor` использует шаблон запроса для извлечения, который находится в файле `interaction_results_extractor.mustache`.
-  В зависимости от ситуации, можно использовать различные цели извлечения, поля и подсказки для оптимизации результатов.