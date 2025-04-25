# Генерация персон

## Обзор

Этот модуль предназначен для создания разнообразных контекстов для генерации описаний персон. 

Он принимает широкий контекст, содержащий общие сведения о персонажах (например, демографические данные, физические характеристики, поведение, убеждения и т.д.), и генерирует множество более специфичных контекстов, основанных на этом широком контексте. 

Эти специфичные контексты затем могут быть использованы для генерации индивидуальных описаний персон.

## Подробней

Модуль использует  интеллектуальные алгоритмы для создания  множества вариантов контекста из одного широкого контекста.  

Он  анализирует вводные данные, выделяет ключевые характеристики и создает различные вариации, чтобы обеспечить разнообразие  в генерируемых описаниях персонажей.  

Модуль может быть использован для создания описаний персон для различных целей, таких как  генерация  диалогов,  разработка  игровых  персонажей,  создание   контента   для   маркетинга   и   другие   задачи,   связанные   с   моделированием   человеческого   поведения.

## Функции

### `generate_person_contexts`

**Назначение**: Функция принимает широкий контекст, содержащий информацию о демографических данных, физических характеристиках, поведении, убеждениях и других особенностях персон, и генерирует набор специфичных контекстов, которые могут быть использованы для создания индивидуальных описаний персонажей. 

**Параметры**:

- `broad_context` (str): Широкий контекст, описывающий общие характеристики персон.

**Возвращает**:

- list: Массив строк, где каждая строка представляет собой специфичный контекст для генерации персонажей.

**Примеры**:

```python
broad_context = "Generate 3 person(s) description(s) based on the following broad context: Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not"

contexts = generate_person_contexts(broad_context)

print(contexts)

# Вывод:
# ["Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies", "Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.", "Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children."]

```

**Как работает функция**:

Функция использует алгоритмы обработки естественного языка для анализа  входного контекста. Она извлекает ключевые слова и фразы,  связанные с демографическими данными,  физическими характеристиками,  поведением и  убеждениями. 

Затем она генерирует  множество вариантов этих характеристик,   создавая   более   специфичные   контексты.  
Например,  из   широкого   контекста   "Latin  American,  age  between  20  and  40 years old"  могут   быть   сгенерированы   контексты   "Mexican   person,  age  25", "Brazilian   person,   age  32",  "Colombian   person,   age   28"   и   т.д.

**Внутренние функции**:

- `_generate_person_context`:  Эта внутренняя функция  принимает  широкий  контекст  и   генерирует   один   специфичный   контекст.   Она   использует   случайный   выбор   среди   вариантов   характеристик,   чтобы   обеспечить   разнообразие   в   результатах.
- `_expand_context`:  Эта   внутренняя   функция   принимает   контекст   и   расширяет   его,   добавляя   более   детализированную   информацию   о   персонаже,   например,   увлечения,   работу,   личности   и   т.д.

**Примеры**:

-  `_generate_person_context("Latin American, age between 20 and 40 years old")`  может   вернуть   контекст  "Mexican person, age 25".
-  `_expand_context("Mexican person, age 25")`  может   вернуть   контекст  "Mexican person, age 25, lawyer, enjoys sports and movies".

## Примеры

```python
# Широкий контекст:
broad_context = "Generate 3 person(s) description(s) based on the following broad context: Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not"

# Генерация специфичных контекстов:
contexts = generate_person_contexts(broad_context)

# Вывод:
# ["Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies", "Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.", "Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children."]

# Использование специфичного контекста для генерации описания:
# (Пример с использованием библиотеки OpenAI)
import openai

openai.api_key = "YOUR_API_KEY"

context = contexts[0]

response = openai.Completion.create(
  engine="text-davinci-003",
  prompt=context,
  max_tokens=100,
  temperature=0.7
)

print(response.choices[0].text)

# Вывод:
# "This is a description of a Mexican person that has formed as a lawyer but now works in another area, is single, likes sports and movies. They enjoy spending time with friends and family, and are passionate about their hobbies. They are a kind and caring individual who is always willing to help others."
```