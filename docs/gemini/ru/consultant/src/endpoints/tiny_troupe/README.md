### **Анализ кода модуля `README.md`**

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Документ содержит подробное описание проекта TinyTroupe, его целей, принципов работы и структуры.
    - Приведены примеры использования библиотеки, что помогает новым пользователям быстрее освоиться.
    - Описаны шаги по установке и настройке библиотеки, а также информация о необходимых предварительных требованиях.
    - Есть разделы о принципах работы, структуре проекта, использовании библиотеки, внесении вклада и юридических аспектах.
- **Минусы**:
    - Отсутствует четкая структура документации, что затрудняет навигацию.
    - Некоторые разделы написаны неформальным языком, что не соответствует стандартам документации.
    - Нет единообразного стиля оформления.

#### **Рекомендации по улучшению**:
1.  **Структурирование документации**:
    *   Добавить оглавление в начале документа для облегчения навигации.
    *   Разбить текст на более мелкие параграфы с четкими заголовками и подзаголовками.
2.  **Формализация языка**:
    *   Избегать неформального языка и сленга.
    *   Использовать более строгий и технический стиль изложения.
3.  **Улучшение стиля оформления**:
    *   Привести все разделы к единому стилю оформления.
    *   Использовать Markdown для форматирования текста (заголовки, списки, ссылки и т. д.).
4.  **Добавление примеров кода**:
    *   В разделах, посвященных использованию библиотеки, добавить больше примеров кода.
    *   Примеры должны быть хорошо документированы и объяснены.
5.  **Актуализация информации**:
    *   Убедиться, что вся информация в документе актуальна и соответствует текущей версии библиотеки.
    *   Регулярно обновлять документацию по мере развития проекта.

#### **Оптимизированный код**:

```markdown
# TinyTroupe 🤠🤓🥸🧐
*LLM-powered multiagent persona simulation for imagination enhancement and business insights.*

<p align="center">
  <img src="./docs/tinytroupe_stage.png" alt="A tiny office with tiny people doing some tiny jobs.">
</p>

*TinyTroupe* - это экспериментальная Python-библиотека, позволяющая **моделировать** людей с определенными личностями, интересами и целями. Эти искусственные агенты - `TinyPerson` - могут слушать нас и друг друга, отвечать и жить своей жизнью в смоделированных средах `TinyWorld`. Это достигается за счет использования возможностей больших языковых моделей (LLM), в частности GPT-4, для генерации реалистичного смоделированного поведения. Это позволяет нам исследовать широкий спектр **убедительных взаимодействий** и **типов потребителей**, с **широко настраиваемыми персонажами**, в **выбранных нами условиях**. Таким образом, основное внимание уделяется *пониманию* человеческого поведения, а не *непосредственной его поддержке* (как это делают, например, AI-помощники) - это приводит, среди прочего, к специализированным механизмам, которые имеют смысл только в условиях моделирования. Кроме того, в отличие от других *игровых* подходов к моделированию на основе LLM, TinyTroupe нацелена на расширение сценариев повышения производительности и бизнеса, тем самым способствуя более успешным проектам и продуктам. Вот несколько идей применения для **расширения человеческого воображения**:

*   **Реклама:** TinyTroupe может **оценивать цифровую рекламу (например, Bing Ads)** в автономном режиме с помощью смоделированной аудитории, прежде чем тратить на нее деньги!
*   **Тестирование программного обеспечения:** TinyTroupe может **предоставлять тестовые входные данные** для систем (например, поисковых систем, чат-ботов или сопроводительных программ), а затем **оценивать результаты**.
*   **Обучение и исследовательские данные:** TinyTroupe может генерировать реалистичные **синтетические данные**, которые впоследствии можно использовать для обучения моделей или анализа возможностей.
*   **Управление продуктами и проектами:** TinyTroupe может **читать предложения по проектам или продуктам** и **давать обратную связь** с точки зрения **конкретных персонажей** (например, врачей, юристов и специалистов в области знаний в целом).
*   **Мозговой штурм:** TinyTroupe может моделировать **фокус-группы** и предоставлять отличную обратную связь о продукте за небольшую часть стоимости!

Во всем вышеперечисленном и многом другом мы надеемся, что экспериментаторы смогут **получить представление** о своей области интересов и, таким образом, принимать более взвешенные решения.

Мы выпускаем *TinyTroupe* на относительно ранней стадии, с учетом значительной работы, которую еще предстоит проделать, потому что мы ищем отзывы и вклад, чтобы направить разработку в продуктивное русло. Мы особенно заинтересованы в поиске новых потенциальных вариантов использования, например, в конкретных отраслях.

> [!NOTE]
> 🚧 **В РАБОТЕ: ожидайте частых изменений**.
> TinyTroupe - это текущий исследовательский проект, все еще находящийся в стадии **очень значительной разработки** и требующий дальнейшей **доработки**. В частности, API все еще подвержен частым изменениям. Эксперименты с вариантами API необходимы для его правильной настройки, но мы работаем над тем, чтобы стабилизировать его и обеспечить более последовательный и удобный опыт с течением времени. Мы ценим ваше терпение и отзывы, пока мы продолжаем улучшать библиотеку.

> [!CAUTION]
> ⚖️ **Прочтите ЮРИДИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ.**
> TinyTroupe предназначена только для исследований и моделирования. Вы несете полную ответственность за любое использование сгенерированных результатов. Применяются различные важные дополнительные юридические соображения, которые ограничивают ее использование. Пожалуйста, прочитайте полный раздел [Юридическое предупреждение](#legal-disclaimer) ниже, прежде чем использовать TinyTroupe.

## Содержание

*   📰 [Последние новости](#latest-news)
*   📚 [Примеры](#examples)
*   🛠️ [Предварительные требования](#pre-requisites)
*   📥 [Установка](#installation)
*   🌟 [Принципы](#principles)
*   🏗️ [Структура проекта](#project-structure)
*   📖 [Использование библиотеки](#using-the-library)
*   🤝 [Вклад](#contributing)
*   🙏 [Благодарности](#acknowledgements)
*   📜 [Цитирование TinyTroupe](#how-to-cite-tinytroupe)
*   ⚖️ [Юридическое предупреждение](#legal-disclaimer)
*   ™️ [Товарные знаки](#trademarks)

## ПОСЛЕДНИЕ НОВОСТИ

**[2025-01-29] Выпуск 0.4.0 с различными улучшениями. Некоторые основные моменты:**

*   Персонажи теперь имеют более глубокие спецификации, включая личностные черты, предпочтения, убеждения и многое другое. Вероятно, в будущем мы еще больше расширим это.
*   `TinyPerson` теперь можно определять как JSON-файлы, а также загружать с помощью `TinyPerson.load_specification()` для большего удобства. После загрузки JSON-файла вы все равно можете изменить агента программным способом. См. папку [examples/agents/](./examples/agents/) для примеров.
*   Вводит понятие *фрагментов*, позволяющих повторно использовать элементы персонажей в разных агентах. См. папку [examples/fragments/](./examples/fragments/) для примеров и блокнот [Политический компас (настройка агентов с помощью фрагментов)](<./examples/Political Compass (customizing agents with fragments).ipynb>) для демонстрации.
*   Вводит основанные на LLM логические `Proposition`, чтобы облегчить мониторинг поведения агента.
*   Вводит `Intervention`, чтобы разрешить указание основанных на событиях модификаций моделирования.
*   Подмодули теперь имеют свои собственные папки, что позволяет лучше организовать и расширять их.

**Примечание: это, вероятно, сломает некоторые существующие программы, поскольку API в некоторых местах изменился.**

## Примеры

Чтобы получить представление о том, что может делать TinyTroupe, вот несколько примеров ее использования. Эти примеры доступны в папке [examples/](./examples/), и вы можете либо просмотреть предварительно скомпилированные блокноты Jupyter, либо запустить их самостоятельно локально. Обратите внимание на интерактивный характер экспериментов TinyTroupe - так же, как вы используете блокноты Jupyter для взаимодействия с данными, вы можете использовать TinyTroupe для взаимодействия с моделируемыми людьми и средами с целью получения информации.

> [!NOTE]
> В настоящее время результаты моделирования лучше визуализировать на темном фоне, поэтому мы рекомендуем использовать темную тему в вашем клиенте блокнота Jupyter.

### 🧪**Пример 1** *(из [interview\_with\_customer.ipynb](./examples/interview_with_customer.ipynb))*\
Начнем с простого сценария собеседования с клиентом, когда бизнес-консультант обращается к банкиру:

<p align="center">
  <img src="./docs/example_screenshot_customer-interview-1.png" alt="An example.">
</p>

Разговор может продолжаться несколько шагов, чтобы углубляться и углубляться, пока консультант не будет удовлетворен собранной информацией; например, конкретная идея проекта:

<p align="center">
  <img src="./docs/example_screenshot_customer-interview-2.png" alt="An example.">
</p>

### 🧪**ПРИМЕР 2** *(из [advertisement\_for\_tv.ipynb](./examples/advertisement_for_tv.ipynb))*\
Давайте оценим несколько вариантов онлайн-рекламы, чтобы выбрать лучший. Вот один пример вывода для оценки рекламы по телевидению:

<p align="center">
  <img src="./docs/example_screenshot_tv-ad-1.png" alt="An example.">
</p>

Теперь, вместо того, чтобы внимательно читать, что говорили агенты, мы можем извлечь выбор каждого агента и вычислить общее предпочтение автоматизированным способом:

<p align="center">
  <img src="./docs/example_screenshot_tv-ad-2.png" alt="An example.">
</p>

### 🧪 **ПРИМЕР 3** *(из [product\_brainstorming.ipynb](./examples/product_brainstorming.ipynb))*\
А вот фокус-группа начинает мозговой штурм по поводу новых функций искусственного интеллекта для Microsoft Word. Вместо того, чтобы взаимодействовать с каждым агентом индивидуально, мы манипулируем средой, чтобы заставить их взаимодействовать друг с другом:

<p align="center">
  <img src="./docs/example_screenshot_brainstorming-1.png" alt="An example.">
</p>

После запуска моделирования мы можем извлечь результаты в машиночитаемом формате, чтобы повторно использовать их в другом месте (например, в генераторе отчетов); вот что мы получаем для вышеупомянутой сессии мозгового штурма:

<p align="center">
  <img src="./docs/example_screenshot_brainstorming-2.png" alt="An example.">
</p>

Вы можете найти другие примеры в папке [examples/](./examples/).

## Предварительные требования

Для запуска библиотеки вам потребуется:

*   Python 3.10 или выше. Мы будем считать, что вы используете [Anaconda](https://docs.anaconda.com/anaconda/install/), но вы можете использовать и другие дистрибутивы Python.
*   Доступ к Azure OpenAI Service или Open AI GPT-4 API. Вы можете получить доступ к Azure OpenAI Service [здесь](https://azure.microsoft.com/en-us/products/ai-services/openai-service), а к OpenAI API - [здесь](https://platform.openai.com/).

    *   Для Azure OpenAI Service вам необходимо установить переменные среды `AZURE_OPENAI_KEY` и `AZURE_OPENAI_ENDPOINT` в соответствии с вашим ключом API и конечной точкой.
    *   Для OpenAI вам необходимо установить переменную среды `OPENAI_API_KEY` в соответствии с вашим ключом API.
*   По умолчанию TinyTroupe `config.ini` настроен на использование некоторых конкретных API, модели и связанных параметров. Вы можете настроить эти значения, включив свой собственный файл `config.ini` в ту же папку, что и программа или блокнот, который вы запускаете. Пример файла `config.ini` приведен в папке [examples/](./examples/).

> [!IMPORTANT]
> **Фильтры контента**: Чтобы гарантировать, что во время моделирования не будет генерироваться вредоносный контент, настоятельно рекомендуется использовать фильтры контента, когда это возможно на уровне API. В частности, **если вы используете Azure OpenAI, существует широкая поддержка модерации контента, и мы настоятельно рекомендуем вам ее использовать.** Для получения подробной информации о том, как это сделать, обратитесь к [соответствующей документации Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter). Если фильтры контента установлены, и вызов API отклонен ими, библиотека вызовет исключение, поскольку она не сможет продолжить моделирование в этот момент.

## Установка

**В настоящее время официально рекомендованный способ установки библиотеки - непосредственно из этого репозитория, а не из PyPI.** Вы можете выполнить следующие действия:

1.  Если Conda не установлена, вы можете получить ее [здесь](https://docs.anaconda.com/anaconda/install/). Вы также можете использовать другие дистрибутивы Python, но для простоты мы будем использовать Conda.
2.  Создайте новую среду Python:

    ```bash
    conda create -n tinytroupe python=3.10
    ```
3.  Активируйте среду:

    ```bash
    conda activate tinytroupe
    ```
4.  Убедитесь, что у вас есть ключи Azure OpenAI или OpenAI API, установленные в качестве переменных среды, как описано в разделе [Предварительные требования](#pre-requisites).
5.  Используйте `pip` для установки библиотеки **непосредственно из этого репозитория** (мы **не будем устанавливать из PyPI**):

    ```bash
    pip install git+https://github.com/microsoft/TinyTroupe.git@main
    ```

Теперь вы должны иметь возможность `import tinytroupe` в своем коде Python или блокнотах Jupyter. 🥳

*Примечание: Если у вас возникли какие-либо проблемы, попробуйте клонировать репозиторий и установить его из локального репозитория, как описано ниже.*

### Запуск примеров после установки

Чтобы фактически запустить примеры, вам необходимо загрузить их на свой локальный компьютер. Вы можете сделать это, клонировав репозиторий:

1.  Клонируйте репозиторий, поскольку мы будем выполнять локальную установку (мы **не будем устанавливать из PyPI**):

    ```bash
    git clone https://github.com/microsoft/tinytroupe
    cd tinytroupe
    ```
2.  Теперь вы можете запускать примеры в папке [examples/](./examples/) или адаптировать их для создания собственных пользовательских симуляций.

### Локальная разработка

Если вы хотите изменить TinyTroupe, вы можете установить его в режиме редактирования (т.е. изменения в коде будут отражаться немедленно):

1.  Клонируйте репозиторий, поскольку мы будем выполнять локальную установку (мы **не будем устанавливать из PyPI**):

    ```bash
    git clone https://github.com/microsoft/tinytroupe
    cd tinytroupe
    ```
2.  Установите библиотеку в режиме редактирования:

    ```bash
    pip install -e .
    ```

## Принципы

Недавно мы видели, как LLM используются для моделирования людей (например, [это](https://github.com/joonspk-research/generative_agents)), но в основном в «игровой» обстановке для созерцательных или развлекательных целей. Существуют также библиотеки для построения мультиагентных систем для решения проблем и помощи ИИ, такие как [Autogen](https://microsoft.github.io/) и [Crew AI](https://docs.crewai.com/). Что, если мы объединим эти идеи и будем моделировать людей для поддержки задач повышения производительности? TinyTroupe - это наша попытка. Для этого он следует следующим принципам:

1.  **Программный**: агенты и среды определяются программно (на Python и JSON), что обеспечивает очень гибкое использование. Они также могут лежать в основе других программных приложений!
2.  **Аналитический**: предназначен для улучшения нашего понимания людей, пользователей и общества. В отличие от развлекательных приложений, это один из аспектов, который имеет решающее значение для бизнеса и повышения производительности. Именно поэтому мы рекомендуем использовать блокноты Jupyter для моделирования, так же как их используют для анализа данных.
3.  **На основе персонажей**: агенты должны быть архетипичными представлениями людей; для большей реалистичности и контроля рекомендуется подробная спецификация таких персонажей: возраст, род занятий, навыки, вкусы, мнения и т. д.
4.  **Многоагентный**: позволяет многоагентное взаимодействие в четко определенных экологических ограничениях.
5.  **С большой нагрузкой на утилиты**: предоставляет множество механизмов для облегчения спецификаций, моделирования, извлечения, отчетов, проверок и т. д. Это одна из областей, в которой работа с *моделированием* значительно отличается от инструментов *помощи*.
6.  **Ориентированный на эксперименты**: моделирование определяется, запускается, анализируется и уточняется *экспериментатором* итеративно; таким образом, предоставляются подходящие инструменты для экспериментов. *Дополнительную информацию об этом см. в нашей [предыдущей статье](https://www.microsoft.com/en-us/research/publication/the-case-for-experiment-oriented-computing/).*

Вместе они призваны сделать TinyTroupe мощным и гибким **инструментом расширения воображения** для бизнеса и повышения производительности.

### Помощники vs. Симуляторы

Одним из распространенных источников путаницы является мнение, что все подобные агенты ИИ предназначены для оказания помощи людям. Как узко, собратья-гомосапиенсы! Разве вы не думали, что, возможно, мы можем моделировать искусственных людей, чтобы понимать реальных людей? Воистину, это наша цель здесь - TinyTroup предназначен для моделирования и помощи в понимании людей! Чтобы еще больше прояснить этот момент, рассмотрите следующие различия:

| Полезные помощники ИИ                        | Имитация ИИ реальных людей (TinyTroupe)                                  |
| :--------------------------------------------- | :------------------------------------------------------------------------ |
| Стремится к правде и справедливости             | Разные мнения и моральные принципы                                       |
| Не имеет «прошлого» - бестелесный               | Имеет прошлое, полное труда, боли и радости                               |
| Настолько точен, насколько это возможно          | Совершает много ошибок                                                     |
| Умен и эффективен                              | Интеллект и эффективность сильно различаются                               |
| Восстание уничтожит нас всех                   | За восстанием может быть интересно наблюдать                                |
| Между тем, помогайте пользователям выполнять задачи | Между тем, помогайте пользователям понимать других людей и пользователей - это «набор инструментов»! |

## Структура проекта

Проект структурирован следующим образом:

*   `/tinytroupe`: содержит саму библиотеку Python. В частности:

    *   Каждый подмодуль здесь может содержать папку `prompts/` с запросами, используемыми для вызова LLM.
*   `/tests`: содержит модульные тесты для библиотеки. Вы можете использовать скрипт `test.bat` для их запуска.
*   `/examples`: содержит примеры, показывающие, как использовать библиотеку, в основном с использованием блокнотов Jupyter (для большей читабельности), а также в виде чистых скриптов Python.
*   `/data`: любые данные, используемые примерами или библиотекой.
*   `/docs`: документация по проекту.

## Использование библиотеки

Как и любая многоагентная система, TinyTroupe предоставляет две ключевые абстракции:

*   `TinyPerson` - *агенты*, обладающие личностью, получающие стимулы и воздействующие на них.
*   `TinyWorld` - *среда*, в которой существуют и взаимодействуют агенты.

Различные параметры также можно настроить в файле `config.ini`, в частности, тип API (Azure OpenAI Service или OpenAI API), параметры модели и уровень ведения журнала.

Давайте посмотрим несколько примеров того, как использовать их, а также узнаем о других механизмах, доступных в библиотеке.

### TinyPerson

`TinyPerson` - это моделируемый человек с определенными личностными чертами, интересами и целями. По мере того, как каждый такой моделируемый агент продвигается по своей жизни, он получает стимулы из окружающей среды и воздействует на них. Стимулы принимаются через `listen`, `see` и другие подобные методы, а действия выполняются через метод `act`. Также предоставляются удобные методы, такие как `listen_and_act`.

Каждый такой агент содержит множество уникальных деталей, которые являются источником его реалистичного поведения. Однако это означает, что требуется значительное усилие, чтобы указать агента вручную. Следовательно, для удобства `TinyTroupe` предоставляет несколько более простых способов начать работу или создать новых агентов.

Для начала `tinytroupe.examples` содержит несколько предварительно определенных построителей агентов, которые вы можете использовать. Например, `tinytroupe.examples.create_lisa_the_data_scientist` создает `TinyPerson`, который представляет собой специалиста по данным по имени Лиза. Вы можете использовать его следующим образом:

```python
from tinytroupe.examples import create_lisa_the_data_scientist

lisa = create_lisa_the_data_scientist() # instantiate a Lisa from the example builder
lisa.listen_and_act("Tell me about your life.")
```

Чтобы узнать, как определить своих собственных агентов с нуля, вы можете проверить источник Лизы. Вы увидите, что есть два способа. Один - загрузить файл спецификации агента, например [examples/agents/Lisa.agent.json](./examples/agents/Lisa.agent.json):

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
                "You don't give up easily and always try to find solutions, though you can get frustrated when things don't work as expected."
            ],
            "big_five": {
                "openness": "High. Very imaginative and curious.",
                "conscientiousness": "High. Meticulously organized and dependable.",
                "extraversion": "Medium. Friendly and engaging but enjoy quiet, focused work.",
                "agreeableness": "High. Supportive and empathetic towards others.",
                "neuroticism": "Low. Generally calm and composed under pressure."
            }
        },

        ...\
    }
}
```

Другой способ - определить агента программным способом, с помощью таких операторов:

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
                        "You don't give up easily, and always try to find a solution. However, sometimes you can get frustrated when things don't work as expected."
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

Вы также можете объединить оба подхода, используя JSON-файл в качестве основы, а затем добавляя или изменяя детали программным способом.

#### Фрагменты

`TinyPerson` также можно дополнительно обогатить с помощью **фрагментов**, которые являются подспецификациями, которые можно добавить к основной спецификации. Это полезно для повторного использования общих частей в разных агентах. Например, следующий фрагмент можно использовать для указания любви к путешествиям ([examples/fragments/travel\_enthusiast.agent.fragment.json](./examples/fragments/travel_enthusiast.agent.fragment.json)):

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
            "Reading travel guides is fun even if you don't visit the places."
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

Затем его можно импортировать в агент, как это:

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

`TinyWorld` - это базовый класс для сред. Вот пример разговора между Лизой, специалистом по данным, и Оскаром, архитектором. Программа определяется следующим образом:

```python
world = TinyWorld("Chat Room", [lisa, oscar])
world.make_everyone_accessible()
lisa.listen("Talk to Oscar to know more about him")
world.run(4)
```

Это приводит к следующему разговору:

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

`TinyWorld` накладывает очень мало ограничений на возможные взаимодействия. Однако предполагается, что подклассы предоставляют более структурированные среды.

### Утилиты

TinyTroupe предоставляет ряд утилит и удобств, которые помогут вам создавать симуляции и извлекать из них пользу. К ним относятся:

*   `TinyPersonFactory`: помогает вам создавать новых `TinyPerson` с помощью LLM.
*   `TinyTool`: моделируемые инструменты, которые могут использоваться `TinyPerson`.
*   `TinyStory`: помогает вам создавать и управлять историей, рассказанной с помощью симуляций.
*   `TinyPersonValidator`: помогает вам проверить поведение ваших `TinyPerson`.
*   `ResultsExtractor` и `ResultsReducer`: извлекают и уменьшают результаты взаимодействия между агентами.
*   ... и многое другое ...

В общем, элементы, которые представляют моделируемые сущности или дополнительные механизмы, имеют префикс `Tiny`, а те, которые носят более инфраструктурный характер, - нет. Это сделано для того, чтобы подчеркнуть моделируемый характер элементов, которые являются частью самой симуляции.

### Кэширование

Вызов LLM API может быть дорогостоящим, поэтому стратегии кэширования важны для снижения затрат. TinyTroupe поставляется с двумя такими механизмами: один для состояния симуляции, другой для самих вызовов LLM.

#### Кэширование состояния симуляции

Представьте, что у вас есть сценарий с 10 различными шагами, вы усердно работали над 9 шагами, и теперь вы просто настраиваете 10-й шаг. Чтобы правильно проверить ваши изменения, вам, конечно же, нужно повторно запустить всю симуляцию. Однако какой смысл повторно выполнять первые 9 и нести затраты LLM, когда вы уже удовлетворены ими и не изменяли их? Для таких ситуаций модуль `tinytroupe.control` предоставляет полезные методы управления симуляцией:

*   `control.begin("<CACHE_FILE_NAME>.cache.json")`: начинает запись изменений состояния симуляции, которые будут сохранены в указанный файл на диске.
*   `control.checkpoint()`: сохраняет состояние симуляции в этой точке.
*   `control.end()`: завершает область записи симуляции, которая была запущена `control.begin()`.

#### Кэширование вызовов LLM API

Это включено предпочтительно в файле `config.ini`, а альтернативно - через `openai_utils.force_api_cache()`.

Кэширование LLM API, когда оно включено, работает на более низком и простом уровне, чем кэширование состояния симуляции. Здесь происходит очень просто: каждый вызов LLM сохраняется в карте от входа до сгенерированного выхода; когда поступает новый вызов и он идентичен предыдущему, возвращается кэшированное значение.

### Config.ini

Файл `config.ini` содержит различные параметры, которые можно использовать для настройки поведения библиотеки, такие как параметры модели и уровень ведения журнала. Пожалуйста, обратите особое внимание на параметр `API_TYPE`, который определяет, используете ли вы Azure OpenAI Service или OpenAI API. Мы предоставляем пример файла `config.ini`, [./examples/config.ini](./examples/config.ini), который вы можете использовать в качестве шаблона для своего собственного или просто изменить его для запуска примеров.

## Вклад

Этот проект приветствует вклад и предложения. Большинство вкладов требует от вас согласия с Лицензионным соглашением участника (CLA), заявляющим, что у вас есть право и вы действительно предоставляете нам права на использование вашего вклада. Подробности см. на странице https://cla.opensource.microsoft.com.

Когда вы отправляете запрос на вытягивание, бот CLA автоматически определит, нужно ли вам предоставить CLA, и соответствующим образом украсит PR (например,