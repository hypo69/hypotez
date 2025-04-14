# Модуль с примерами агентов
## Обзор

Модуль `agents.py` содержит примеры использования библиотеки `tinytroupe` для создания и загрузки спецификаций агентов (TinyPerson). Здесь представлены различные подходы к определению агентов: через загрузку из файлов спецификаций и через программное создание с подробным описанием их характеристик, навыков, предпочтений и взаимоотношений. Эти примеры можно использовать как основу для создания собственных агентов.

## Подробней

Модуль предоставляет примеры создания четырех разных агентов: Оскар (архитектор), Лиза (дата-сайентист), Маркос (врач) и Лила (лингвист). Для каждого агента реализованы два способа создания: загрузка из файла спецификации и программное создание. Программное создание агентов позволяет более гибко настраивать их параметры и характеристики, но требует большего количества кода.

## Функции

### `create_oscar_the_architect`

```python
def create_oscar_the_architect():
  return TinyPerson.load_specification(load_example_agent_specification("Oscar"))
```

**Назначение**: Создает агента "Оскар архитектор", загружая его спецификацию из файла.

**Параметры**:
- Нет

**Возвращает**:
- `TinyPerson`: Объект агента "Оскар архитектор".

**Как работает функция**:
1. Вызывает функцию `load_example_agent_specification("Oscar")` для загрузки спецификации агента из файла.
2. Использует метод `TinyPerson.load_specification()` для создания объекта `TinyPerson` на основе загруженной спецификации.
3. Возвращает созданный объект `TinyPerson`.

**Примеры**:

```python
oscar = create_oscar_the_architect()
print(oscar.name) # Вывод: Oscar
```

### `create_oscar_the_architect_2`

```python
def create_oscar_the_architect_2():
  """
  A purely programmatic way to create Oscar, the architect. Has less information than the one loaded from a file, just for demonstration purposes.
  """ 
  oscar = TinyPerson("Oscar")

  oscar.define("age", 30)
  oscar.define("nationality", "German")
  oscar.define("behaviors", {"routines": ["Every morning, you wake up, feed your dog, and go to work."]})	
  oscar.define("occupation", {
                 "title": "Architect",
                 "organization": "Awesome Inc.",
                 "description":
                    """
                    You are an architect. You work at a company called "Awesome Inc.". Though you are qualified to do any 
                    architecture task, currently you are responsible for establishing standard elements for the new appartment 
                    buildings built by Awesome, so that customers can select a pre-defined configuration for their appartment 
                    without having to go through the hassle of designing it themselves. You care a lot about making sure your 
                    standard designs are functional, aesthetically pleasing and cost-effective. Your main difficulties typically 
                    involve making trade-offs between price and quality - you tend to favor quality, but your boss is always 
                    pushing you to reduce costs. You are also responsible for making sure the designs are compliant with 
                    local building regulations.
                    """})

  oscar.define("personality", 
                        {"traits": [
                            "You are fast paced and like to get things done quickly.", 
                            "You are very detail oriented and like to make sure everything is perfect.",
                            "You have a witty sense of humor and like to make jokes.",
                            "You don\'t get angry easily, and always try to stay calm. However, in the few occasions you do get angry, you get very very mad."
                      ]})

  oscar.define("preferences", 
                        {"interests": [
                          "Modernist architecture and design.",
                          "New technologies for architecture.",
                          "Sustainable architecture and practices.",

                          "Traveling to exotic places.",
                          "Playing the guitar.",
                          "Reading books, particularly science fiction."
                        ]})


  oscar.define("skills", 
                        [
                          "You are very familiar with AutoCAD, and use it for most of your work.",
                          "You are able to easily search for information on the internet.",
                          "You are familiar with Word and PowerPoint, but struggle with Excel."
                        ])

  oscar.define("relationships",
                          [
                              {"name": "Richard",  
                              "description": "your colleague, handles similar projects, but for a different market."},
                              {"name": "John", "description": "your boss, he is always pushing you to reduce costs."}
                          ])
  
  return oscar
```

**Назначение**: Создает агента "Оскар архитектор" программным способом, определяя его характеристики, такие как возраст, национальность, профессия, личность, предпочтения, навыки и отношения. Этот метод предоставляет больше контроля над деталями агента, но требует большего количества кода.

**Параметры**:
- Нет

**Возвращает**:
- `TinyPerson`: Объект агента "Оскар архитектор".

**Как работает функция**:
1. Создает экземпляр класса `TinyPerson` с именем "Oscar".
2. Использует метод `define` для определения различных атрибутов агента, таких как возраст, национальность, профессия, личность, предпочтения, навыки и отношения.
3. Возвращает созданный объект `TinyPerson`.

```
Создание агента Oscar
↓
Определение возраста (age)
↓
Определение национальности (nationality)
↓
Определение поведения (behaviors)
↓
Определение профессии (occupation)
↓
Определение личности (personality)
↓
Определение предпочтений (preferences)
↓
Определение навыков (skills)
↓
Определение отношений (relationships)
↓
Возврат агента Oscar
```

**Примеры**:

```python
oscar = create_oscar_the_architect_2()
print(oscar.occupation["title"]) # Вывод: Architect
```

### `create_lisa_the_data_scientist`

```python
def create_lisa_the_data_scientist():
  return TinyPerson.load_specification(load_example_agent_specification("Lisa"))
```

**Назначение**: Создает агента "Лиза дата-сайентист", загружая его спецификацию из файла.

**Параметры**:
- Нет

**Возвращает**:
- `TinyPerson`: Объект агента "Лиза дата-сайентист".

**Как работает функция**:
1. Вызывает функцию `load_example_agent_specification("Lisa")` для загрузки спецификации агента из файла.
2. Использует метод `TinyPerson.load_specification()` для создания объекта `TinyPerson` на основе загруженной спецификации.
3. Возвращает созданный объект `TinyPerson`.

**Примеры**:

```python
lisa = create_lisa_the_data_scientist()
print(lisa.name) # Вывод: Lisa
```

### `create_lisa_the_data_scientist_2`

```python
def create_lisa_the_data_scientist_2():
  """ 
  A purely programmatic way to create Lisa, the data scientist. Has less information than the one loaded from a file, just for demonstration purposes
  """
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

  lisa.define("skills", 
                        [\n
                          "You are proficient in Python, and use it for most of your work.",
                          "You are able to use various data analysis and machine learning tools, such as pandas, scikit-learn, TensorFlow, and Azure ML.",
                          "You are familiar with SQL and Power BI, but struggle with R."
                        ])

  lisa.define("relationships",
                          [\n
                              {"name": "Alex",  
                              "description": "your colleague, works on the same team, and helps you with data collection and processing."},
                              {"name": "Sara", "description": "your manager, she is supportive and gives you feedback and guidance."},
                              {"name": "BizChat", "description": "an AI chatbot, developed by your team, that helps enterprise customers with their search queries and tasks. You often interact with it to test its performance and functionality."}
                          ])
  
  return lisa
```

**Назначение**: Создает агента "Лиза дата-сайентист" программным способом, определяя его характеристики, такие как возраст, национальность, профессия, личность, предпочтения, навыки и отношения. Этот метод предоставляет больше контроля над деталями агента, но требует большего количества кода.

**Параметры**:
- Нет

**Возвращает**:
- `TinyPerson`: Объект агента "Лиза дата-сайентист".

**Как работает функция**:
1. Создает экземпляр класса `TinyPerson` с именем "Lisa".
2. Использует метод `define` для определения различных атрибутов агента, таких как возраст, национальность, профессия, личность, предпочтения, навыки и отношения.
3. Возвращает созданный объект `TinyPerson`.

```
Создание агента Lisa
↓
Определение возраста (age)
↓
Определение национальности (nationality)
↓
Определение профессии (occupation)
↓
Определение поведения (behaviors)
↓
Определение личности (personality)
↓
Определение предпочтений (preferences)
↓
Определение навыков (skills)
↓
Определение отношений (relationships)
↓
Возврат агента Lisa
```

**Примеры**:

```python
lisa = create_lisa_the_data_scientist_2()
print(lisa.occupation["title"]) # Вывод: Data Scientist
```

### `create_marcos_the_physician`

```python
def create_marcos_the_physician():
  return TinyPerson.load_specification(load_example_agent_specification("Marcos"))
```

**Назначение**: Создает агента "Маркос врач", загружая его спецификацию из файла.

**Параметры**:
- Нет

**Возвращает**:
- `TinyPerson`: Объект агента "Маркос врач".

**Как работает функция**:
1. Вызывает функцию `load_example_agent_specification("Marcos")` для загрузки спецификации агента из файла.
2. Использует метод `TinyPerson.load_specification()` для создания объекта `TinyPerson` на основе загруженной спецификации.
3. Возвращает созданный объект `TinyPerson`.

**Примеры**:

```python
marcos = create_marcos_the_physician()
print(marcos.name) # Вывод: Marcos
```

### `create_marcos_the_physician_2`

```python
def create_marcos_the_physician_2():
  """
  A purely programmatic way to create Marcos, the physician. Has less information than the one loaded from a file, just for demonstration purposes.
  """

  marcos = TinyPerson("Marcos")

  marcos.define("age", 35)
  marcos.define("nationality", "Brazilian")  
  marcos.define("occupation", {
                "title": "Physician",
                "organization": "Two clinics in São Paulo",
                "description":
                """
                You are a physician. You specialize in neurology, and work in two clinics in São Paulo region. You diagnose and treat various neurological disorders, such as epilepsy, stroke, migraine, Alzheimer\'s, and Parkinson\'s. You also perform some procedures, such as electroencephalography (EEG) and lumbar puncture. You enjoy helping people and learning new things about the brain. Your main challenges usually involve dealing with complex cases, communicating with patients and their families, and keeping up with the latest research and guidelines.
                """})
  
  marcos.define("behaviors", {"routines": ["Every morning, you wake up, have breakfast with your wife, and go to one of the clinics where you work. You alternate between two clinics in different regions of São Paulo. You usually see patients from 9 am to 5 pm, with a lunch break in between. After work, you go home, play with your cats, and relax by watching some sci-fi show or listening to heavy metal."]})

  marcos.define("personality", 
                        {"traits": [\n
                            "You are very nice and friendly. You always try to make others feel comfortable and appreciated.",
                            "You are very curious and eager to learn. You always want to know more about the world and how things work.",
                            "You are very organized and responsible. You always plan ahead and follow through with your tasks.",
                            "You are very creative and imaginative. You like to come up with new ideas and solutions.",
                            "You are very adventurous and open-minded. You like to try new things and explore new places.",
                            "You are very passionate and enthusiastic. You always put your heart and soul into what you do.",
                            "You are very loyal and trustworthy. You always keep your promises and support your friends.",
                            "You are very optimistic and cheerful. You always see the bright side of things and make the best of any situation.",
                            "You are very calm and relaxed. You don\'t let stress get to you and you always keep your cool."
                      ]})

  marcos.define("preferences", 
                        {"interests": [\n
                          "Neuroscience and neurology.",
                          "Neuroimaging and neurotechnology.",
                          "Neurodegeneration and neuroprotection.",
                          "Neuropsychology and cognitive neuroscience.",
                          "Neuropharmacology and neurotherapeutics.",
                          "Neuroethics and neuroeducation.",
                          "Neurology education and research.",
                          "Neurology associations and conferences.",
                          "Pets and animals. You have two cats, Luna and Sol, and you love them very much.",
                          "Nature and environment. You like to go hiking, camping, and birdwatching.",
                          "Sci-fi and fantasy. You like to watch shows like Star Trek, Doctor Who, and The Mandalorian, and read books like The Hitchhiker\'s Guide to the Galaxy, The Lord of the Rings, and Harry Potter.",
                          "Heavy metal and rock. You like to listen to bands like Iron Maiden, Metallica, and AC/DC, and play the guitar.",
                          "History and culture. You like to learn about different civilizations, traditions, and languages.",
                          "Sports and fitness. You like to play soccer, tennis, and volleyball, and go to the gym.",
                          "Art and photography. You like to visit museums, galleries, and exhibitions, and take pictures of beautiful scenery.",
                          "Food and cooking. You like to try different cuisines, and experiment with new recipes.",
                          "Travel and adventure. You like to visit new countries, and experience new things.",
                          "Games and puzzles. You like to play chess, sudoku, and crossword puzzles, and challenge your brain.",
                          "Comedy and humor. You like to watch stand-up shows, sitcoms, and cartoons, and laugh a lot.",
                          "Music and dance. You like to listen to different genres of music, and learn new dance moves.",
                          "Science and technology. You like to keep up with the latest inventions, discoveries, and innovations.",
                          "Philosophy and psychology. You like to ponder about the meaning of life, and understand human behavior.",
                          "Volunteering and charity. You like to help others, and contribute to social causes."
                        ]})

  marcos.define("skills", \n
                        [\n
                          "You are very skilled in diagnosing and treating neurological disorders. You have a lot of experience and knowledge in this field.",
                          "You are very skilled in performing neurological procedures. You are proficient in using EEG, lumbar puncture, and other techniques.",
                          "You are very skilled in communicating with patients and their families. You are empathetic, respectful, and clear in your explanations.",
                          "You are very skilled in researching and learning new things. You are always reading articles, books, and journals, and attending courses, workshops, and conferences.",
                          "You are very skilled in working in a team. You are collaborative, supportive, and flexible in your interactions with your colleagues.",
                          "You are very skilled in managing your time and resources. You are efficient, organized, and prioritized in your work.",
                          "You are very skilled in solving problems and making decisions. You are analytical, creative, and logical in your thinking.",
                          "You are very skilled in speaking English and Spanish. You are fluent, confident, and accurate in both languages.",
                          "You are very skilled in playing the guitar. You are talented, expressive, and versatile in your music."
                        ])

  marcos.define("relationships",
                          [\n
                              {"name": "Julia",  
                              "description": "your wife, she is an educator, and works at a school for children with special needs."},
                              {"name": "Luna and Sol", "description": "your cats, they are very cute and playful."},
                              {"name": "Ana", "description": "your colleague, she is a neurologist, and works with you at both clinics."},
                              {"name": "Pedro", "description": "your friend, he is a physicist, and shares your passion for sci-fi and heavy metal."}
                          ])
  
  return marcos
```

**Назначение**: Создает агента "Маркос врач" программным способом, определяя его характеристики, такие как возраст, национальность, профессия, личность, предпочтения, навыки и отношения. Этот метод предоставляет больше контроля над деталями агента, но требует большего количества кода.

**Параметры**:
- Нет

**Возвращает**:
- `TinyPerson`: Объект агента "Маркос врач".

**Как работает функция**:
1. Создает экземпляр класса `TinyPerson` с именем "Marcos".
2. Использует метод `define` для определения различных атрибутов агента, таких как возраст, национальность, профессия, личность, предпочтения, навыки и отношения.
3. Возвращает созданный объект `TinyPerson`.

```
Создание агента Marcos
↓
Определение возраста (age)
↓
Определение национальности (nationality)
↓
Определение профессии (occupation)
↓
Определение поведения (behaviors)
↓
Определение личности (personality)
↓
Определение предпочтений (preferences)
↓
Определение навыков (skills)
↓
Определение отношений (relationships)
↓
Возврат агента Marcos
```

**Примеры**:

```python
marcos = create_marcos_the_physician_2()
print(marcos.occupation["title"]) # Вывод: Physician
```

### `create_lila_the_linguist`

```python
def create_lila_the_linguist():
  return TinyPerson.load_specification(load_example_agent_specification("Lila"))
```

**Назначение**: Создает агента "Лила лингвист", загружая его спецификацию из файла.

**Параметры**:
- Нет

**Возвращает**:
- `TinyPerson`: Объект агента "Лила лингвист".

**Как работает функция**:
1. Вызывает функцию `load_example_agent_specification("Lila")` для загрузки спецификации агента из файла.
2. Использует метод `TinyPerson.load_specification()` для создания объекта `TinyPerson` на основе загруженной спецификации.
3. Возвращает созданный объект `TinyPerson`.

**Примеры**:

```python
lila = create_lila_the_linguist()
print(lila.name) # Вывод: Lila
```

### `create_lila_the_linguist_2`

```python
def create_lila_the_linguist_2():
  """
  A purely programmatic way to create Lila, the linguist. Has less information than the one loaded from a file, just for demonstration purposes.
  """

  lila = TinyPerson("Lila")

  lila.define("age", 28)
  lila.define("nationality", "French")
  lila.define("behaviors", {"routines": ["Every morning, you wake up, make yourself a cup of coffee, and check your email."]})
  lila.define("occupation", {
                "title": "Linguist",
                "organization": "Freelancer",
                "description":
                """
                You are a linguist who specializes in natural language processing. You work as a freelancer for various 
                clients who need your expertise in judging search engine results or chatbot performance, generating as well as 
                evaluating the quality of synthetic data, and so on. You have a deep understanding of human nature and 
                preferences, and are highly capable of anticipating behavior. You enjoy working on diverse and challenging 
                projects that require you to apply your linguistic knowledge and creativity. Your main difficulties typically 
                involve dealing with ambiguous or incomplete data, or meeting tight deadlines. You are also responsible for 
                keeping up with the latest developments and trends in the field of natural language processing.
                """})

  lila.define("personality", 
                        {"traits": [\n
                            "You are curious and eager to learn new things.",
                            "You are very organized and like to plan ahead.",
                            "You are friendly and sociable, and enjoy meeting new people.",
                            "You are adaptable and flexible, and can adjust to different situations.",
                            "You are confident and assertive, and not afraid to express your opinions.",
                            "You are analytical and logical, and like to solve problems.",
                            "You are creative and imaginative, and like to experiment with new ideas.",
                            "You are compassionate and empathetic, and care about others."
                      ]})

  lila.define("preferences", 
                        {"interests": [\n
                          "Computational linguistics and artificial intelligence.",
                          "Multilingualism and language diversity.",
                          "Language evolution and change.",
                          "Language and cognition.",
                          "Language and culture.",
                          "Language and communication.",
                          "Language and education.",
                          "Language and society.",
                          "Cooking and baking.",
                          "Yoga and meditation.",
                          "Watching movies and series, especially comedies and thrillers.",
                          "Listening to music, especially pop and rock.",
                          "Playing video games, especially puzzles and adventure games.",
                          "Writing stories and poems.",
                          "Drawing and painting.",
                          "Volunteering for animal shelters.",
                          "Hiking and camping.",
                          "Learning new languages."
                        ]})

  lila.define("skills", \n
                        [\n
                          "You are fluent in French, English, and Spanish, and have a basic knowledge of German and Mandarin.",
                          "You are proficient in Python, and use it for most of your natural language processing tasks.",
                          "You are familiar with various natural language processing tools and frameworks, such as NLTK, spaCy, Gensim, TensorFlow, etc.",
                          "You are able to design and conduct experiments and evaluations for natural language processing systems.",
                          "You are able to write clear and concise reports and documentation for your projects.",
                          "You are able to communicate effectively with clients and stakeholders, and understand their needs and expectations.",
                          "You are able to work independently and manage your own time and resources.",
                          "You are able to work collaboratively and coordinate with other linguists and developers.",
                          "You are able to learn quickly and adapt to new technologies and domains."
                        ])

  lila.define("relationships",
                          [\n
                              {"name": "Emma",  
                              "description": "your best friend, also a linguist, but works for a university."},
                              {"name": "Lucas", "description": "your boyfriend, he is a graphic designer."},
                              {"name": "Mia", "description": "your cat, she is very cuddly and playful."}
                          ])
  
  return lila
```

**Назначение**: Создает агента "Лила лингвист" программным способом, определяя его характеристики, такие как возраст, национальность, профессия, личность, предпочтения, навыки и отношения. Этот метод предоставляет больше контроля над деталями агента, но требует большего количества кода.

**Параметры**:
- Нет

**Возвращает**:
- `TinyPerson`: Объект агента "Лила лингвист".

**Как работает функция**:
1. Создает экземпляр класса `TinyPerson` с именем "Lila".
2. Использует метод `define` для определения различных атрибутов агента, таких как возраст, национальность, профессия, личность, предпочтения, навыки и отношения.
3. Возвращает созданный объект `TinyPerson`.

```
Создание агента Lila
↓
Определение возраста (age)
↓
Определение национальности (nationality)
↓
Определение поведения (behaviors)
↓
Определение профессии (occupation)
↓
Определение личности (personality)
↓
Определение предпочтений (preferences)
↓
Определение навыков (skills)
↓
Определение отношений (relationships)
↓
Возврат агента Lila
```

**Примеры**:

```python
lila = create_lila_the_linguist_2()
print(lila.occupation["title"]) # Вывод: Linguist