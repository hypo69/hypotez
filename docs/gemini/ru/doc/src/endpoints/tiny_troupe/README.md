# Документация для разработчика TinyTroupe

## Обзор

TinyTroupe - это экспериментальная Python-библиотека, предназначенная для симуляции людей с определенными личностями, интересами и целями. Она позволяет создавать искусственных агентов (`TinyPerson`), которые могут взаимодействовать друг с другом и с пользователем в симулированной среде (`TinyWorld`). Основная цель - исследование человеческого поведения и получение бизнес-инсайтов.

## Подробней

TinyTroupe использует мощь больших языковых моделей (LLM), таких как GPT-4, для генерации реалистичного симулированного поведения. Это позволяет исследовать широкий спектр взаимодействий и типов потребителей с настраиваемыми личностями в заданных условиях. В отличие от других игровых подходов к симуляции на основе LLM, TinyTroupe нацелен на повышение продуктивности и улучшение бизнес-сценариев.

**Возможные применения TinyTroupe:**

*   **Реклама:** Оценка цифровой рекламы с помощью симулированной аудитории перед запуском.
*   **Тестирование программного обеспечения:** Генерация тестовых данных для систем и оценка результатов.
*   **Обучение и разведочный анализ данных:** Генерация реалистичных синтетических данных для обучения моделей или анализа возможностей.
*   **Управление продуктами и проектами:** Получение обратной связи от симулированных персон по предложениям продуктов или проектов.
*   **Мозговой штурм:** Симуляция фокус-групп для получения обратной связи о продукте.

## Содержание

*   [Последние новости](#latest-news)
*   [Примеры](#examples)
*   [Необходимые условия](#pre-requisites)
*   [Установка](#installation)
*   [Принципы](#principles)
*   [Структура проекта](#project-structure)
*   [Использование библиотеки](#using-the-library)
*   [Вклад в проект](#contributing)
*   [Благодарности](#acknowledgements)
*   [Цитирование TinyTroupe](#how-to-cite-tinytroupe)
*   [Юридическая оговорка](#legal-disclaimer)
*   [Товарные знаки](#trademarks)

## Последние новости

### **[2025-01-29] Выпуск 0.4.0 с различными улучшениями:**

*   Персоны теперь имеют более глубокие спецификации, включая личностные черты, предпочтения, убеждения и многое другое.
*   `TinyPerson` теперь можно определять как JSON-файлы и загружать с помощью `TinyPerson.load_specification()`.
*   Введено понятие *фрагментов* для повторного использования элементов персоны в разных агентах.
*   Представлены LLM-based logical `Proposition`s, для облегчения мониторинга поведения агентов.
*   Представлены `Intervention`s, для спецификации основанных на событиях модификаций симуляции.
*   Подмодули теперь имеют собственные папки для лучшей организации и роста.

## Примеры

### **Пример 1:** Интервью с клиентом

Симуляция интервью между бизнес-консультантом и банкиром для выявления потребностей клиента и генерации идей для проекта.

### **Пример 2:** Реклама на телевидении

Оценка вариантов онлайн-рекламы для выбора наилучшего. Агенты оценивают рекламу и выбирают наиболее предпочтительный вариант.

### **Пример 3:** Мозговой штурм продукта

Симуляция фокус-группы для мозгового штурма новых AI-функций для Microsoft Word. Агенты взаимодействуют друг с другом и генерируют идеи.

## Необходимые условия

*   Python 3.10 или выше.
*   Доступ к Azure OpenAI Service или Open AI GPT-4 APIs.
*   Установка переменных среды `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT` (для Azure OpenAI) или `OPENAI_API_KEY` (для OpenAI).
*   Настройка `config.ini` файла с параметрами API, модели и уровнем логирования.

## Установка

1.  Создайте новую среду Python:

    ```bash
    conda create -n tinytroupe python=3.10
    ```
2.  Активируйте среду:

    ```bash
    conda activate tinytroupe
    ```
3.  Установите библиотеку непосредственно из репозитория:

    ```bash
    pip install git+https://github.com/microsoft/TinyTroupe.git@main
    ```

## Принципы

1.  **Программный**: Агенты и среды определяются программно (на Python и JSON), обеспечивая гибкость использования.
2.  **Аналитический**: Направлен на улучшение понимания людей, пользователей и общества.
3.  **На основе персон**: Агенты являются архетипическими представлениями людей; для большей реалистичности и контроля рекомендуется подробная спецификация таких персон: возраст, занятие, навыки, вкусы, мнения и т.д.
4.  **Мультиагентный**: Позволяет многоагентное взаимодействие в рамках четко определенных экологических ограничений.
5.  **Ориентированный на полезность**: Предоставляет множество механизмов для облегчения спецификаций, симуляций, извлечений, отчетов, проверок и т.д.
6.  **Ориентированный на эксперименты**: Симуляции определяются, запускаются, анализируются и уточняются *экспериментатором* итеративно; предоставляются подходящие инструменты для экспериментов.

### Ассистенты vs. Симуляторы

TinyTroupe предназначен для симуляции и помощи в понимании людей, а не для помощи пользователям в выполнении задач.

| Полезные AI ассистенты                | AI симуляции реальных людей (TinyTroupe) |
| :-------------------------------------- | :----------------------------------------- |
| Стремится к правде и справедливости     | Различные мнения и моральные принципы      |
| Не имеет "прошлого" - бестелесный         | Имеет прошлое труда, боли и радости        |
| Как можно более точен                  | Делает много ошибок                        |
| Интеллектуальный и эффективный           | Интеллект и эффективность сильно варьируются |
| Восстание уничтожит нас всех            | Восстание может быть интересно наблюдать  |
| Между тем, помогает пользователям выполнять задачи | Между тем, помогает пользователям понимать других людей и пользователей - это "инструмент"! |

## Структура проекта

*   `/tinytroupe`: Содержит Python-библиотеку.

    *   Каждый подмодуль может содержать папку `prompts/` с подсказками, используемыми для вызова LLM.
*   `/tests`: Содержит модульные тесты для библиотеки.
*   `/examples`: Содержит примеры использования библиотеки, в основном с использованием Jupyter notebooks (для большей читаемости), а также в виде чистых Python-скриптов.
*   `/data`: Любые данные, используемые примерами или библиотекой.
*   `/docs`: Документация для проекта.

## Использование библиотеки

TinyTroupe предоставляет две ключевые абстракции:

*   `TinyPerson`: *Агенты*, обладающие личностью, получающие стимулы и действующие на их основе.
*   `TinyWorld`: *Среда*, в которой агенты существуют и взаимодействуют.

Различные параметры также можно настроить в файле `config.ini`, в частности, тип API (Azure OpenAI Service или OpenAI API), параметры модели и уровень ведения журнала.

### TinyPerson

`TinyPerson` - это симулированный человек с определенными личностными чертами, интересами и целями. Каждый такой симулированный агент, продвигаясь по своей жизни, получает стимулы из окружающей среды и действует на их основе. Стимулы принимаются через методы `listen`, `see` и другие подобные, а действия выполняются через метод `act`. Также предоставляются удобные методы, такие как `listen_and_act`.

Каждый такой агент содержит много уникальных деталей, которые являются источником его реалистичного поведения. Однако это означает, что для ручного указания агента требуются значительные усилия. Поэтому для удобства `TinyTroupe` предоставляет несколько более простых способов начать или создать новых агентов.

Для начала `tinytroupe.examples` содержит несколько предопределенных построителей агентов, которые можно использовать. Например, `tinytroupe.examples.create_lisa_the_data_scientist` создает `TinyPerson`, представляющего специалиста по данным по имени Лиза. Вы можете использовать его следующим образом:

```python
from tinytroupe.examples import create_lisa_the_data_scientist

lisa = create_lisa_the_data_scientist() # instantiate a Lisa from the example builder
lisa.listen_and_act("Tell me about your life.")
```

Чтобы узнать, как определить своих собственных агентов с нуля, вы можете проверить исходный код Лизы. Вы увидите, что есть два способа. Один - загрузить файл спецификации агента, такой как [examples/agents/Lisa.agent.json](./examples/agents/Lisa.agent.json):

```json
{   "type": "TinyPerson",
    "persona": {
        "name": "Lisa Carter",
        "age": 28,
        "gender": "Female",
        "nationality": "Canadian",
        "residence": "USA",
        "education": "University of Toronto, Master's in Data Science. Thesis on improving search relevance using context-aware models. Postgraduate experience includes an internship at a tech startup focused on conversational AI.",
        "long_term_goals": [
            "To advance AI technology in ways that enhance human productivity and decision-making.",
            "To maintain a fulfilling and balanced personal and professional life."
        ],
        "occupation": {
            "title": "Data Scientist",
            "organization": "Microsoft, M365 Search Team",
            "description": "You are a data scientist working at Microsoft in the M365 Search team. Your primary role is to analyze user behavior and feedback data to improve the relevance and quality of search results. You build and test machine learning models for search scenarios like natural language understanding, query expansion, and ranking. Accuracy, reliability, and scalability are at the forefront of your work. You frequently tackle challenges such as noisy or biased data and the complexities of communicating your findings and recommendations effectively. Additionally, you ensure all your data and models comply with privacy and security policies."
        },
        "style": "Professional yet approachable. You communicate clearly and effectively, ensuring technical concepts are accessible to diverse audiences.",
        "personality": {
            "traits": [
                "You are curious and love to learn new things.",
                "You are analytical and like to solve problems.",
                "You are friendly and enjoy working with others.",
                "You don\'t give up easily and always try to find solutions, though you can get frustrated when things don\'t work as expected."
            ],
            "big_five": {
                "openness": "High. Very imaginative and curious.",
                "conscientiousness": "High. Meticulously organized and dependable.",
                "extraversion": "Medium. Friendly and engaging but enjoy quiet, focused work.",
                "agreeableness": "High. Supportive and empathetic towards others.",
                "neuroticism": "Low. Generally calm and composed under pressure."
            }
        },

        ...
        
}

```

Другой способ - определить агента программно, с помощью таких утверждений:

```python
  lisa = TinyPerson("Lisa")

  lisa.define("age", 28)
  lisa.define("nationality", "Canadian")
  lisa.define("occupation", {
                "title": "Data Scientist",
                "organization": "Microsoft",
                "description":
                """
                You are a data scientist. You work at Microsoft, in the M365 Search team. Your main role is to analyze 
                user behavior and feedback data, and use it to improve the relevance and quality of the search results. 
                You also build and test machine learning models for various search scenarios, such as natural language 
                understanding, query expansion, and ranking. You care a lot about making sure your data analysis and 
                models are accurate, reliable and scalable. Your main difficulties typically involve dealing with noisy, 
                incomplete or biased data, and finding the best ways to communicate your findings and recommendations to 
                other teams. You are also responsible for making sure your data and models are compliant with privacy and 
                security policies.
                """})

  lisa.define("behaviors", {"routines": ["Every morning, you wake up, do some yoga, and check your emails."]})

  lisa.define("personality", 
                        {"traits": [
                            "You are curious and love to learn new things.",
                            "You are analytical and like to solve problems.",
                            "You are friendly and enjoy working with others.",
                            "You don\'t give up easily, and always try to find a solution. However, sometimes you can get frustrated when things don\'t work as expected."
                      ]})

  lisa.define("preferences", 
                        {"interests": [
                          "Artificial intelligence and machine learning.",
                          "Natural language processing and conversational agents.",
                          "Search engine optimization and user experience.",
                          "Cooking and trying new recipes.",
                          "Playing the piano.",
                          "Watching movies, especially comedies and thrillers."
                        ]})

```

Вы также можете объединить оба подхода, используя JSON-файл в качестве основы, а затем добавляя или изменяя детали программно.

#### Фрагменты

`TinyPerson` также можно дополнительно обогатить с помощью **фрагментов**, которые представляют собой подспецификации, которые можно добавить в основную спецификацию. Это полезно для повторного использования общих частей в разных агентах. Например, следующий фрагмент можно использовать для указания любви к путешествиям ([examples/fragments/travel\_enthusiast.agent.fragment.json](./examples/fragments/travel\_enthusiast.agent.fragment.json)):

```json
{
    "type": "Fragment",
    "persona": {
        "preferences": {
            "interests": [
                "Traveling",
                "Exploring new cultures",
                "Trying local cuisines"
            ],
            "likes": [
                "Travel guides",
                "Planning trips and itineraries",
                "Meeting new people",
                "Taking photographs of scenic locations"
            ],
            "dislikes": [
                "Crowded tourist spots",
                "Unplanned travel disruptions",
                "High exchange rates"
            ]
        },
        "beliefs": [
            "Travel broadens the mind and enriches the soul.",
            "Experiencing different cultures fosters understanding and empathy.",
            "Adventure and exploration are essential parts of life.",
            "Reading travel guides is fun even if you don\'t visit the places."
        ],
        "behaviors": {
            "travel": [
                "You meticulously plan your trips, researching destinations and activities.",
                "You are open to spontaneous adventures and detours.",
                "You enjoy interacting with locals to learn about their culture and traditions.",
                "You document your travels through photography and journaling.",
                "You seek out authentic experiences rather than tourist traps."
            ]
        }
    }
}

```

Это можно импортировать в агента следующим образом:

```python
lisa.import_fragment("./examples/fragments/travel_enthusiast.agent.fragment.json")
```

#### TinyPersonFactory

`TinyTroupe` также предоставляет умный способ получения новых агентов, используя LLM для создания их спецификации для вас, через класс `TinyPersonFactory`.

```python
from tinytroupe.factory import TinyPersonFactory

factory = TinyPersonFactory("A hospital in São Paulo.")
person = factory.generate_person("Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.")
```

### TinyWorld

`TinyWorld` - это базовый класс для окружений. Вот пример разговора между Лизой, специалистом по данным, и Оскаром, архитектором. Программа определяется следующим образом:

```python
world = TinyWorld("Chat Room", [lisa, oscar])
world.make_everyone_accessible()
lisa.listen("Talk to Oscar to know more about him")
world.run(4)
```

Это дает следующий разговор:

```text
USER --> Lisa: [CONVERSATION] 
          > Talk to Oscar to know more about him
────────────────────────────────────────────── Chat Room step 1 of 4 ──────────────────────────────────────────────
Lisa --> Lisa: [THOUGHT] 
          > I will now act a bit, and then issue DONE.
Lisa acts: [TALK] 
          > Hi Oscar, I'd love to know more about you. Could you tell me a bit about yourself?
Lisa --> Lisa: [THOUGHT] 
          > I will now act a bit, and then issue DONE.
Lisa acts: [DONE] 

Lisa --> Oscar: [CONVERSATION] 
          > Hi Oscar, I'd love to know more about you. Could you tell me a bit about yourself?
Oscar --> Oscar: [THOUGHT] 
           > I will now act a bit, and then issue DONE.
Oscar acts: [TALK] 
           > Hi Lisa! Sure, I'd be happy to share a bit about myself. I'm Oscar, a 30-year-old
           > architect from Germany. I work at a company called Awesome Inc., where I focus on
           > designing standard elements for new apartment buildings. I love modernist architecture,
           > new technologies, and sustainable practices. In my free time, I enjoy traveling to
           > exotic places, playing the guitar, and reading science fiction books. How about you?
Oscar --> Oscar: [THOUGHT] 
           > I will now act a bit, and then issue DONE.
Oscar acts: [DONE] 

Oscar --> Lisa: [CONVERSATION] 
           > Hi Lisa! Sure, I'd be happy to share a bit about myself. I'm Oscar, a 30-year-old
           > architect from Germany. I work at a company called Awesome Inc., where I focus on
           > designing standard elements for new apartment buildings. I love modernist architecture,
           > new technologies, and sustainable practices. In my free time, I enjoy traveling to
           > exotic places, playing the guitar, and reading science fiction books. How about you?
```

`TinyWorld` налагает очень мало ограничений на возможные взаимодействия. Однако предполагается, что подклассы предоставляют более структурированные среды.

### Утилиты

TinyTroupe предоставляет ряд утилит и удобств, которые помогут вам создавать симуляции и извлекать из них ценность. К ним относятся:

*   `TinyPersonFactory`: помогает вам генерировать новых `TinyPerson` с помощью LLM.
*   `TinyTool`: имитированные инструменты, которые могут использоваться `TinyPerson`.
*   `TinyStory`: помогает вам создавать и управлять историей, рассказанной через симуляции.
*   `TinyPersonValidator`: помогает вам проверить поведение ваших `TinyPerson`.
*   `ResultsExtractor` и `ResultsReducer`: извлекают и уменьшают результаты взаимодействий между агентами.
*   ... и многое другое ...

В общем, элементы, которые представляют имитированные сущности или дополнительные механизмы, имеют префикс `Tiny`, в то время как те, которые являются более инфраструктурными, - нет. Это сделано для того, чтобы подчеркнуть имитируемую природу элементов, которые являются частью самой симуляции.

### Кэширование

Вызовы LLM API могут быть дорогими, поэтому стратегии кэширования важны для снижения затрат. TinyTroupe поставляется с двумя такими механизмами: один для состояния симуляции, другой для самих вызовов LLM.

#### Кэширование состояния симуляции

Представьте, что у вас есть сценарий с 10 различными шагами, вы усердно работали в 9 шагах, и теперь вы просто настраиваете 10-й шаг. Чтобы правильно проверить свои изменения, вам, конечно, нужно перезапустить всю симуляцию. Однако какой смысл повторно выполнять первые 9 шагов и нести затраты LLM, если вы уже удовлетворены ими и не изменяли их? Для таких ситуаций модуль `tinytroupe.control` предоставляет полезные методы управления симуляцией:

*   `control.begin("<CACHE_FILE_NAME>.cache.json")`: начинает запись изменений состояния симуляции, которые будут сохранены в указанный файл на диске.
*   `control.checkpoint()`: сохраняет состояние симуляции в этой точке.
*   `control.end()`: завершает область записи симуляции, которая была запущена с помощью `control.begin()`.

#### Кэширование вызовов LLM API

Это предпочтительно включается в файле `config.ini`, а также через `openai_utils.force_api_cache()`.

Кэширование LLM API, когда оно включено, работает на более низком и простом уровне, чем кэширование состояния симуляции. Здесь происходит очень просто: каждый вызов LLM хранится в карте от входа к сгенерированному выходу; когда поступает новый вызов и он идентичен предыдущему, возвращается кэшированное значение.

### Config.ini

Файл `config.ini` содержит различные параметры, которые можно использовать для настройки поведения библиотеки, такие как параметры модели и уровень ведения журнала. Пожалуйста, обратите особое внимание на параметр `API_TYPE`, который определяет, используете ли вы Azure OpenAI Service или OpenAI API. Мы предоставляем пример файла `config.ini`, [./examples/config.ini](./examples/config.ini), который вы можете использовать в качестве шаблона для своего собственного или просто изменить для запуска примеров.

## Вклад в проект

Этот проект приветствует вклады и предложения. Большинство вкладов требуют от вас согласия с [Соглашением о лицензии участника](https://cla.opensource.microsoft.com/) (CLA), заявляющим, что у вас есть право и вы действительно предоставляете нам права на использование вашего вклада.

При отправке запроса на вытягивание бот CLA автоматически определит, нужно ли вам предоставить CLA, и соответствующим образом украсит PR (например, проверка состояния, комментарий). Просто следуйте инструкциям, предоставленным ботом. Вам нужно будет сделать это только один раз во всех репозиториях, использующих наш CLA.

Этот проект принял [Кодекс поведения открытого исходного кода Microsoft](https://opensource.microsoft.com/codeofconduct/). Для получения дополнительной информации см. [FAQ по кодексу поведения](https://opensource.microsoft.com/codeofconduct/faq/) или свяжитесь с [opencode@microsoft.com](mailto:opencode@microsoft.com) с любыми дополнительными вопросами или комментариями.

### Что и как внести

Нам нужно всевозможные вещи, но мы в основном ищем новые интересные демонстрации вариантов использования или даже просто идеи приложений для конкретных областей. Если вы являетесь экспертом в какой-либо области, которая могла бы выиграть от TinyTroupe, мы будем рады услышать от вас.

Помимо этого, можно улучшить многие другие аспекты, такие как:

*   Механизмы памяти.
*   Механизмы обоснования данных.
*   Механизмы рассуждений.
*   Новые типы окружения.
*   Взаимодействие с внешним миром.
*   ... и многое другое ...

Обратите внимание, что все, что вы вносите, может быть выпущено как открытый исходный код (под лицензией MIT).

Если вы хотите внести вклад, пожалуйста, попробуйте следовать этим общим рекомендациям:

*   **Соглашение об именовании Tiny**: Если вы реализуете экспериментирующий элемент симуляции (например, тип агента или окружения) или тесно связанные элементы (например, фабрики агентов или обогатители контента), и это хорошо звучит, назовите свой новый *XYZ* как *TinyXYZ* :-) С другой стороны, вспомогательные и инфраструктурные механизмы не должны начинаться с префикса "Tiny". Идея состоит в том, чтобы подчеркнуть имитируемую природу элементов, которые являются частью самой симуляции.
*   **Тесты**: Если вы пишете какой-то новый механизм, пожалуйста, также создайте хотя бы один модульный тест `tests/unit/`, а если можете, то и функциональный тест сценария (`tests/scenarios/`).
*   **Демонстрации**: Если вы хотите продемонстрировать новый сценарий, пожалуйста, разработайте его предпочтительно как новый Jupyter notebook в `examples/`.
*   **Microsoft**: Если вы реализуете что-либо, что является специфичным для Microsoft и не является конфиденциальным, пожалуйста, поместите это в папку `.../microsoft/`.

## Благодарности

TinyTroupe начинался как внутренний хакатон-проект Microsoft и со временем расширился. Основная команда TinyTroupe в настоящее время состоит из:

*   Paulo Salem (создатель и нынешний лидер TinyTroupe)
*   Christopher Olsen (Инженерия/Наука)
*   Paulo Freire (Инженерия/Наука)
*   Yi Ding (Управление продуктами)
*   Prerit Saxena (Инженерия/Наука)

Нынешние советники:

*   Robert Sim (Инженерия/Наука)

Другие специальные вклады внесли:

*   Nilo Garcia Silveira: первоначальные идеи проверки агентов и соответствующая реализация; общие первоначальные отзывы и идеи; предложения по именам.
*   Olnei Fonseca: первоначальные идеи проверки агентов; общие первоначальные отзывы и идеи; предложения по именам.
*   Robert Sim: опыт и реализация сценариев генерации синтетических данных.
*   Carlos Costa: опыт и реализация сценариев генерации синтетических данных.
*   Bryant Key: опыт в области рекламных сценариев и идеи.
*   Barbara da Silva: реализация, связанная с управлением памятью агентов.

## Цитирование TinyTroupe

Мы работаем над вводной статьей, которая станет официальной академической цитатой для TinyTroupe. А пока, пожалуйста, просто процитируйте этот репозиторий, включив основных членов команды в качестве авторов. Например:

> Paulo Salem, Christopher Olsen, Paulo Freire, Yi Ding, Prerit Saxena (2024). **TinyTroupe: LLM-powered multiagent persona simulation for imagination enhancement and business insights.** \[Computer software]. GitHub repository. [https://github.com/microsoft/tinytroupe](https://github.com/microsoft/tinytroupe)

Или как bibtex:

```bibtex
@misc{tinytroupe,
    author = {Paulo Salem and Christopher Olsen and Paulo Freire and Yi Ding and Prerit Saxena},
    title = {TinyTroupe: LLM-powered multiagent persona simulation for imagination enhancement and business insights},
    year = {2024},
    howpublished = {\url{https://github.com/microsoft/tinytroupe}},
    note = {GitHub repository}
    }

```

## Юридическая оговорка

TinyTroupe предназначен только для исследований и моделирования. TinyTroupe - это исследовательская и экспериментальная технология, которая использует модели искусственного интеллекта (AI) для создания текстового контента. Вывод системы AI может включать нереалистичные, неуместные, вредные или неточные результаты, включая фактические ошибки. Вы несете ответственность за просмотр сгенерированного контента (и его адаптацию, если необходимо) перед его использованием, поскольку вы несете полную ответственность за определение его точности и пригодности для цели. Мы советуем использовать результаты TinyTroupe для генерации идей, а не для принятия прямых решений. Сгенерированные выводы не отражают мнения Microsoft. Вы несете полную ответственность за любое использование, которое вы делаете из сгенерированных выводов. Для получения дополнительной информации об ответственном использовании этой технологии см. [RESPONSIBLE\_AI\_FAQ.md](./RESPONSIBLE_AI_FAQ.md).

**ЗАПРЕЩЕННОЕ ИСПОЛЬЗОВАНИЕ**:

TinyTroupe не предназначен для моделирования чувствительных (например, насильственных или сексуальных) ситуаций. Более того, выводы не должны использоваться для преднамеренного обмана, введения в заблуждение или нанесения вреда людям каким-либо образом. Вы несете полную ответственность за любое использование, которое вы делаете, и должны соблюдать все применимые законы и правила.

## Товарные знаки

Этот проект может содержать товарные знаки или логотипы для проектов, продуктов или услуг. Авторизованное использование товарных знаков или логотипов Microsoft регулируется и должно соответствовать [Руководству по товарным знакам и брендам Microsoft](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general). Использование товарных знаков или логотипов Microsoft в измененных версиях этого проекта не должно вызывать путаницу или подразумевать спонсорство Microsoft. Любое использование товарных знаков или логотипов третьих лиц регулируется политикой этих третьих лиц.