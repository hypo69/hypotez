## Как использовать Normalizer
=========================================================================================

Описание
-------------------------
`Normalizer` - это класс, который нормализует текстовые элементы, такие как отрывки текста, концепции и другие. Он использует модель LLM (Large Language Model) для определения наиболее репрезентативной формы каждого элемента.

Шаги выполнения
-------------------------
1. **Инициализация**:
   -  Создается экземпляр класса `Normalizer` с предоставленными элементами для нормализации, количеством элементов для вывода и флагом verbose (для отладки).
   -  Элементы делаются уникальными.
   -  Инициализируется структура данных `normalized_elements` (словарь, где ключом является нормализованный элемент, а значением - список исходных элементов, объединенных в него), а также `normalizing_map` (словарь, где ключом является исходный элемент, а значением - его нормализованный вариант, используется для кэширования).
   -  Составляется начальный набор сообщений для LLM, используя шаблоны "normalizer.system.mustache" и "normalizer.user.mustache". 
   -  Отправляется сообщение в LLM (через `openai_utils.client().send_message`) с температурой 0.1 (низкая температура для более предсказуемых ответов).
   -  Полученный результат LLM обрабатывается и сохраняется в `normalized_elements`.

2. **Нормализация**:
   -  Метод `normalize()` принимает на вход либо один элемент, либо список элементов.
   -  Проверяется наличие кэша для каждого элемента. Если элемент уже нормализован, берется из кэша.
   -  Если элемент не кэширован, составляются сообщения для LLM, используя шаблоны "normalizer.applier.system.mustache" и "normalizer.applier.user.mustache".
   -  Отправляется сообщение в LLM, результат LLM обрабатывается и сохраняется в кэше.
   -  Возвращается нормализованный элемент (или список элементов) в том же порядке, что и во входных данных.

Пример использования
-------------------------

```python
from tinytroupe.extraction.normalizer import Normalizer

# Создание списка элементов для нормализации
elements = ["apple", "Apple", "APPLE", "fruit", "fruits"]

# Инициализация Normalizer
normalizer = Normalizer(elements, n=2, verbose=True)

# Нормализация элемента
normalized_element = normalizer.normalize("apple")
print(f"Normalized element: {normalized_element}") 

# Нормализация списка элементов
normalized_elements = normalizer.normalize(["apple", "fruit"])
print(f"Normalized elements: {normalized_elements}") 
```

**Output:**
```
Normalization result message: {'id': 'msg_...', 'object': 'chat.completion', 'created': ..., 'model': 'gpt-3.5-turbo', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': '{"fruit": ["apple", "Apple", "APPLE", "fruit"], "fruits": ["fruits"]}'}, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': ..., 'completion_tokens': ..., 'total_tokens': ...}}
{'fruit': ['apple', 'Apple', 'APPLE', 'fruit'], 'fruits': ['fruits']}
Normalized element: ['apple', 'Apple', 'APPLE', 'fruit']
Normalization result message: {'id': 'msg_...', 'object': 'chat.completion', 'created': ..., 'model': 'gpt-3.5-turbo', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': '["fruit", "fruit"]'}, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': ..., 'completion_tokens': ..., 'total_tokens': ...}}
['fruit', 'fruit']
Normalized elements: ['fruit', 'fruit']
```