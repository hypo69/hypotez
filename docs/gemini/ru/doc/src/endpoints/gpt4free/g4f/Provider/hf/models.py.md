# Модуль `models.py`

## Обзор

Этот модуль определяет модели, которые будут использоваться для работы с GPT4Free через HuggingFace. Он предоставляет список моделей по умолчанию для текста, изображений, а также альтернативные модели, а также определения псевдонимов для удобства работы с ними.


## Модели

### `default_model` 

**Описание**: Модель по умолчанию для обработки текстовых запросов. 
**Значение**: `Qwen/Qwen2.5-72B-Instruct`
**Примеры**:

```python
# Использование default_model в коде
model = default_model 
```

### `default_image_model` 

**Описание**: Модель по умолчанию для обработки изображений. 
**Значение**: `black-forest-labs/FLUX.1-dev`
**Примеры**:

```python
# Использование default_image_model в коде
image_model = default_image_model
```

### `image_models` 

**Описание**: Список моделей для обработки изображений.
**Значение**:  `[default_image_model, "black-forest-labs/FLUX.1-schnell",]`
**Примеры**:

```python
# Использование image_models в коде
for model in image_models:
    # Действия с моделью
    pass
```

### `text_models` 

**Описание**: Список моделей для обработки текста.
**Значение**: `[default_model, 'meta-llama/Llama-3.3-70B-Instruct', 'CohereForAI/c4ai-command-r-plus-08-2024', 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B', 'Qwen/QwQ-32B', 'nvidia/Llama-3.1-Nemotron-70B-Instruct-HF', 'Qwen/Qwen2.5-Coder-32B-Instruct', 'meta-llama/Llama-3.2-11B-Vision-Instruct', 'mistralai/Mistral-Nemo-Instruct-2407', 'microsoft/Phi-3.5-mini-instruct',]`
**Примеры**:

```python
# Использование text_models в коде
for model in text_models:
    # Действия с моделью
    pass
```

### `fallback_models` 

**Описание**: Список моделей для обрабтки текста или изображений в качестве резерва.
**Значение**:  `text_models + image_models`
**Примеры**:

```python
# Использование fallback_models в коде
for model in fallback_models:
    # Действия с моделью
    pass
```

### `model_aliases` 

**Описание**: Словарь псевдонимов для моделей, упрощающий работу с ними. 
**Значение**: 
```python
{
    ### Chat ###
    "qwen-2.5-72b": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "llama-3": "meta-llama/Llama-3.3-70B-Instruct",
    "llama-3.3-70b": "meta-llama/Llama-3.3-70B-Instruct",
    "command-r-plus": "CohereForAI/c4ai-command-r-plus-08-2024",
    "deepseek-r1": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "qwq-32b": "Qwen/QwQ-32B",
    "nemotron-70b": "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
    "qwen-2.5-coder-32b": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "llama-3.2-11b": "meta-llama/Llama-3.2-11B-Vision-Instruct",
    "mistral-nemo": "mistralai/Mistral-Nemo-Instruct-2407",
    "phi-3.5-mini": "microsoft/Phi-3.5-mini-instruct",
    ### Image ###
    "flux": "black-forest-labs/FLUX.1-dev",
    "flux-dev": "black-forest-labs/FLUX.1-dev",
    "flux-schnell": "black-forest-labs/FLUX.1-schnell",
    ### Used in other providers ###
    "qwen-2-vl-7b": "Qwen/Qwen2-VL-7B-Instruct",
    "gemma-2-27b": "google/gemma-2-27b-it",
    "qwen-2-72b": "Qwen/Qwen2-72B-Instruct",
    "qvq-72b": "Qwen/QVQ-72B-Preview",
    "sd-3.5": "stabilityai/stable-diffusion-3.5-large",
}
```
**Примеры**:

```python
# Использование псевдонима для модели
model = model_aliases["qwen-2.5-72b"] 
```

### `extra_models` 

**Описание**: Дополнительные модели, которые могут использоваться для различных задач.
**Значение**: `["meta-llama/Llama-3.2-11B-Vision-Instruct", "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF", "NousResearch/Hermes-3-Llama-3.1-8B",]`
**Примеры**:

```python
# Использование extra_models в коде
for model in extra_models:
    # Действия с моделью
    pass
```

### `default_vision_model` 

**Описание**: Модель по умолчанию для обработки изображений с текстовыми подписями. 
**Значение**: `meta-llama/Llama-3.2-11B-Vision-Instruct`
**Примеры**:

```python
# Использование default_vision_model в коде
vision_model = default_vision_model
```

### `default_llama_model` 

**Описание**: Модель по умолчанию для обработки текстовых запросов (Llama). 
**Значение**: `meta-llama/Llama-3.3-70B-Instruct`
**Примеры**:

```python
# Использование default_llama_model в коде
model = default_llama_model
```

### `vision_models` 

**Описание**: Список моделей для обработки изображений с текстовыми подписями. 
**Значение**:  `[default_vision_model, "Qwen/Qwen2-VL-7B-Instruct"]`
**Примеры**:

```python
# Использование vision_models в коде
for model in vision_models:
    # Действия с моделью
    pass
```


## Назначение модуля

Этот модуль предоставляет набор моделей, которые используются для обработки различных типов запросов с помощью API GPT4Free. 
Он позволяет выбирать модели по умолчанию, использовать псевдонимы для удобства и определяет дополнительные модели для расширения возможностей. 

## Примеры использования

```python
# Получение модели по умолчанию
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.models import default_model
model = default_model

# Получение модели по псевдониму
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.models import model_aliases
model = model_aliases["llama-3.3-70b"]

# Использование модели из списка
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.models import text_models
for model in text_models:
    # Обработка модели
    pass