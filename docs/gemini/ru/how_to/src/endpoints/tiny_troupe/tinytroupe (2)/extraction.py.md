### Как использовать класс `ResultsExtractor`
=========================================================================================

Описание
-------------------------
Класс `ResultsExtractor` предназначен для извлечения данных из экземпляров `TinyPerson` (агентов) и `TinyWorld` (миров) в TinyTroupe. Он использует шаблоны и OpenAI API для структурированного извлечения информации, кэширует результаты и предоставляет методы для сохранения этих результатов в формате JSON.

Шаги выполнения
-------------------------
1.  **Инициализация `ResultsExtractor`**:
    -   Создается экземпляр класса `ResultsExtractor`. При этом определяется путь к шаблону промпта для извлечения данных и инициализируются кэши для хранения извлеченных данных агентов и миров.
2.  **Извлечение данных из агента (`extract_results_from_agent`)**:
    -   Вызывается метод `extract_results_from_agent` с указанием экземпляра `TinyPerson`, цели извлечения (`extraction_objective`), контекста (`situation`), списка полей (`fields`) и подсказок для полей (`fields_hints`).
    -   Формируется запрос к OpenAI API на основе истории взаимодействий агента и предоставленных параметров.
    -   Результат, полученный от OpenAI, извлекается в формате JSON и кэшируется.
3.  **Извлечение данных из мира (`extract_results_from_world`)**:
    -   Вызывается метод `extract_results_from_world` с указанием экземпляра `TinyWorld`, цели извлечения, контекста, списка полей и подсказок для полей.
    -   Формируется запрос к OpenAI API на основе истории взаимодействий агентов в мире и предоставленных параметров.
    -   Результат, полученный от OpenAI, извлекается в формате JSON и кэшируется.
4.  **Сохранение результатов в JSON (`save_as_json`)**:
    -   Вызывается метод `save_as_json` с указанием имени файла.
    -   Кэшированные результаты извлечения данных агентов и миров сохраняются в указанный файл в формате JSON.

Пример использования
-------------------------

```python
    from tinytroupe.agent import TinyPerson
    from tinytroupe.environment import TinyWorld
    from tinytroupe.extraction import ResultsExtractor

    # Создание экземпляров агента и мира (предположим, что они уже созданы и настроены)
    agent = TinyPerson(name="Alice")
    world = TinyWorld(name="Wonderland")

    # Инициализация ResultsExtractor
    extractor = ResultsExtractor()

    # Извлечение данных из агента
    agent_results = extractor.extract_results_from_agent(
        tinyperson=agent,
        extraction_objective="Summarize the agent's key interactions.",
        situation="In a bustling marketplace.",
        fields=["interaction_summary", "key_participants"]
    )

    # Извлечение данных из мира
    world_results = extractor.extract_results_from_world(
        tinyworld=world,
        extraction_objective="Identify the main events in the world.",
        situation="During a royal festival.",
        fields=["event_name", "participants"]
    )

    # Сохранение результатов в JSON
    extractor.save_as_json("extraction_results.json", verbose=True)
```

В этом примере демонстрируется создание экземпляров `TinyPerson` и `TinyWorld`, инициализация `ResultsExtractor`, извлечение данных из агента и мира, а также сохранение результатов в файл `extraction_results.json`.
```

```markdown
### Как использовать класс `ResultsReducer`
=========================================================================================

Описание
-------------------------
Класс `ResultsReducer` предназначен для сведения (редукции) данных, извлеченных из агентов `TinyPerson`. Он позволяет применять определенные правила к сообщениям в памяти агента и формировать на их основе структурированное представление данных.

Шаги выполнения
-------------------------
1.  **Инициализация `ResultsReducer`**:
    -   Создается экземпляр класса `ResultsReducer`. При этом инициализируются атрибуты `results` (для хранения результатов редукции) и `rules` (для хранения правил редукции).
2.  **Добавление правил редукции (`add_reduction_rule`)**:
    -   Вызывается метод `add_reduction_rule` с указанием триггера (события или типа стимула) и функции, которая будет применяться для обработки этого триггера.
    -   Если правило для указанного триггера уже существует, вызывается исключение.
3.  **Редукция данных агента (`reduce_agent`)**:
    -   Вызывается метод `reduce_agent` с указанием экземпляра `TinyPerson`.
    -   Происходит перебор всех сообщений в эпизодической памяти агента.
    -   Для каждого сообщения определяется его роль (`system`, `user` или `assistant`).
    -   В зависимости от роли сообщения и типа стимула/действия, применяется соответствующее правило редукции (если оно определено).
    -   Результаты применения правил добавляются в список `reduction`.
4.  **Преобразование результатов в DataFrame (`reduce_agent_to_dataframe`)**:
    -   Вызывается метод `reduce_agent_to_dataframe` с указанием экземпляра `TinyPerson` и списка имен столбцов для DataFrame.
    -   Вызывается метод `reduce_agent` для получения списка результатов редукции.
    -   На основе полученного списка и указанных имен столбцов формируется DataFrame.

Пример использования
-------------------------

```python
    import pandas as pd
    from tinytroupe.agent import TinyPerson
    from tinytroupe.extraction import ResultsReducer

    # Создание экземпляра агента (предположим, что он уже создан и настроен)
    agent = TinyPerson(name="Bob")

    # Инициализация ResultsReducer
    reducer = ResultsReducer()

    # Пример правила редукции для стимула типа "greeting"
    def greeting_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
        return {
            "timestamp": timestamp,
            "event": event,
            "content": content,
            "source": source_agent.name,
            "target": target_agent.name
        }

    # Добавление правила редукции
    reducer.add_reduction_rule("greeting", greeting_rule)

    # Редукция данных агента
    reduction_results = reducer.reduce_agent(agent)

    # Преобразование результатов в DataFrame
    df = reducer.reduce_agent_to_dataframe(agent, column_names=["timestamp", "event", "content", "source", "target"])

    # Вывод DataFrame
    print(df)
```

В этом примере демонстрируется создание экземпляра `TinyPerson`, инициализация `ResultsReducer`, добавление правила редукции для стимула типа `greeting`, редукция данных агента и преобразование результатов в DataFrame.
```

```markdown
### Как использовать класс `ArtifactExporter`
=========================================================================================

Описание
-------------------------
Класс `ArtifactExporter` предназначен для экспорта артефактов (данных) из элементов TinyTroupe, таких как агенты и миры, в различные форматы файлов (JSON, TXT, DOCX). Он позволяет сохранять синтетические данные, сгенерированные в процессе симуляций, для дальнейшего использования.

Шаги выполнения
-------------------------
1.  **Инициализация `ArtifactExporter`**:
    -   Создается экземпляр класса `ArtifactExporter` с указанием базовой директории для сохранения артефактов (`base_output_folder`).
2.  **Экспорт артефакта (`export`)**:
    -   Вызывается метод `export` с указанием имени артефакта (`artifact_name`), данных артефакта (`artifact_data`), типа контента (`content_type`), формата контента (`content_format`) и целевого формата (`target_format`).
    -   В зависимости от целевого формата, вызывается соответствующий метод для экспорта данных:
        -   `_export_as_json` для сохранения в формате JSON.
        -   `_export_as_txt` для сохранения в формате TXT.
        -   `_export_as_docx` для сохранения в формате DOCX.
3.  **Формирование пути к файлу (`_compose_filepath`)**:
    -   Метод `_compose_filepath` формирует путь к файлу на основе базовой директории, типа контента, имени артефакта и формата файла.
    -   Создаются промежуточные директории, если они не существуют.
4.  **Экспорт в JSON (`_export_as_json`)**:
    -   Метод `_export_as_json` сохраняет данные артефакта в формате JSON. Данные должны быть представлены в виде словаря.
5.  **Экспорт в TXT (`_export_as_txt`)**:
    -   Метод `_export_as_txt` сохраняет данные артефакта в виде текста. Данные могут быть представлены как в виде словаря (где извлекается значение ключа `content`), так и в виде строки.
6.  **Экспорт в DOCX (`_export_as_docx`)**:
    -   Метод `_export_as_docx` сохраняет данные артефакта в формате DOCX.
    -   Данные сначала преобразуются в HTML с использованием markdown, а затем конвертируются в DOCX с использованием `pypandoc`.

Пример использования
-------------------------

```python
    from tinytroupe.extraction import ArtifactExporter

    # Инициализация ArtifactExporter
    exporter = ArtifactExporter(base_output_folder="output")

    # Пример данных для экспорта
    artifact_data = {
        "title": "Agent Interaction Summary",
        "content": "# Key Interactions\n- Agent A greeted Agent B.\n- Agent B responded positively."
    }

    # Экспорт артефакта в формате JSON
    exporter.export(
        artifact_name="interaction_summary",
        artifact_data=artifact_data,
        content_type="summary",
        target_format="json"
    )

    # Экспорт артефакта в формате TXT
    exporter.export(
        artifact_name="interaction_summary",
        artifact_data=artifact_data,
        content_type="summary",
        content_format="md",
        target_format="txt"
    )

    # Экспорт артефакта в формате DOCX
    exporter.export(
        artifact_name="interaction_summary",
        artifact_data=artifact_data,
        content_type="summary",
        content_format="md",
        target_format="docx"
    )
```

В этом примере демонстрируется инициализация `ArtifactExporter`, создание данных для экспорта и экспорт артефакта в различных форматах (JSON, TXT, DOCX).
```

```markdown
### Как использовать класс `Normalizer`
=========================================================================================

Описание
-------------------------
Класс `Normalizer` предназначен для нормализации текстовых элементов (пассажей, концепций и т.д.). Он использует OpenAI API для приведения различных элементов к общему, стандартизированному виду.

Шаги выполнения
-------------------------
1.  **Инициализация `Normalizer`**:
    -   Создается экземпляр класса `Normalizer` с указанием списка элементов для нормализации (`elements`) и количества нормализованных элементов, которые необходимо получить на выходе (`n`).
    -   При инициализации происходит обращение к OpenAI API для получения списка нормализованных элементов.
    -   Результаты сохраняются в атрибутах `normalized_elements` (список нормализованных элементов) и `normalizing_map` (словарь, отображающий исходные элементы на нормализованные).
2.  **Нормализация элемента или списка элементов (`normalize`)**:
    -   Вызывается метод `normalize` с указанием элемента или списка элементов для нормализации.
    -   Если элемент уже был нормализован ранее (т.е. присутствует в `normalizing_map`), возвращается его нормализованная форма из кэша.
    -   Если элемент еще не был нормализован, происходит обращение к OpenAI API для получения его нормализованной формы.
    -   Результаты нормализации сохраняются в `normalizing_map` для последующего использования.

Пример использования
-------------------------

```python
    from tinytroupe.extraction import Normalizer

    # Пример списка элементов для нормализации
    elements = ["apple", " apples", "АПЕЛЬСИН", "orange", "ОРАНЖЕВЫЙ"]

    # Инициализация Normalizer
    normalizer = Normalizer(elements=elements, n=2)

    # Нормализация списка элементов
    normalized_elements = normalizer.normalize(elements)
    print(f"Normalized elements: {normalized_elements}")

    # Нормализация отдельного элемента
    normalized_element = normalizer.normalize("apple")
    print(f"Normalized element: {normalized_element}")
```

В этом примере демонстрируется инициализация `Normalizer` с списком элементов, требующих нормализации. Затем вызывается метод `normalize`, чтобы нормализовать список элементов и отдельный элемент.