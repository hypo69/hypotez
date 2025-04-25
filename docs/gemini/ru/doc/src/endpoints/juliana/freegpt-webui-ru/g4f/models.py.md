# Модуль `models.py`

## Обзор

Модуль `models.py` содержит классы и функции, отвечающие за определение и преобразование моделей AI.  
Он используется для работы с различными AI-моделями, такими как:

- GPT-3.5-turbo 
- GPT-4
- Claude 
- Alpaca
- StableLM
- BLOOM
- FLAN-T5
- GPT-NeoX
- Oasst-SFT
- Santacoder
- Command
- Code Cushman
- Code Davinci
- Text Ada
- Text Babbage
- Text Curie
- Text Davinci
- Palm
- Falcon
- Llama

## Классы

### `Model`

**Описание**: Класс `Model`  используется для определения характеристик каждой модели AI. 

**Атрибуты**:

- `name` (str): Название модели.
- `base_provider` (str): Основной провайдер модели. 
- `best_provider` (`Provider.Provider`): Лучший провайдер для модели.  
- `best_providers` (list): Список лучших провайдеров для модели.  

**Примеры**:

```python
from g4f import Provider
from g4f.models import Model

model = Model.gpt_35_turbo  # Получение модели gpt-3.5-turbo
print(model.name)          # Вывод: gpt-3.5-turbo
print(model.best_provider) # Вывод: Provider.Mishalsgpt 
```

### `ModelUtils`

**Описание**: Класс `ModelUtils`  используется для преобразования названий моделей в соответствующие объекты `Model`.  

**Атрибуты**:

- `convert` (dict): Словарь, где ключ - название модели, а значение - соответствующий объект `Model`.

**Примеры**:

```python
from g4f.models import ModelUtils

model_utils = ModelUtils()
model = model_utils.convert['gpt-3.5-turbo']  # Получение модели gpt-3.5-turbo 
print(model.name)                            # Вывод: gpt-3.5-turbo
```

## Функции

### `Model.convert_model_name`

**Назначение**: Преобразует название модели в объект `Model`. 

**Параметры**:

- `model_name` (str): Название модели AI.

**Возвращает**:

- `Model`: Объект модели AI.

**Примеры**:

```python
from g4f.models import Model

model = Model.convert_model_name('gpt-3.5-turbo')
print(model.name)  # Вывод: gpt-3.5-turbo
```

### `Model.get_provider_by_model_name`

**Назначение**: Определяет лучший провайдер для заданной модели.

**Параметры**:

- `model_name` (str): Название модели.

**Возвращает**:

- `Provider.Provider`: Объект лучшего провайдера.

**Примеры**:

```python
from g4f.models import Model

provider = Model.get_provider_by_model_name('gpt-4')
print(provider) # Вывод: Provider.ChatgptAi
```

### `Model.get_providers_by_model_name`

**Назначение**: Определяет список лучших провайдеров для заданной модели.

**Параметры**:

- `model_name` (str): Название модели.

**Возвращает**:

- `list`: Список объектов лучших провайдеров.

**Примеры**:

```python
from g4f.models import Model

providers = Model.get_providers_by_model_name('gpt-4')
for provider in providers:
    print(provider) # Вывод: Provider.Bing, Provider.Lockchat
```