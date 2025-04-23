## \file hypotez/src/endpoints/gpt4free/g4f/Provider/hf/models.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль, определяющий модели для использования с провайдером Hugging Face (HF).
=========================================================================

Этот модуль содержит списки и псевдонимы моделей, используемые для работы с различными задачами,
такими как генерация текста и обработка изображений. Он также определяет модели, используемые по умолчанию.

.. module:: src.endpoints.gpt4free.g4f.Provider.hf.models
"""

## Обзор

В этом модуле определены константы, содержащие списки различных моделей, используемых в провайдере HF. Он также содержит псевдонимы моделей, упрощающие их использование.

## Более подробная информация

Модуль содержит списки текстовых и визуальных моделей, псевдонимы моделей и определяет модели, используемые по умолчанию. Этот код используется для настройки и выбора моделей при работе с провайдерами HF.

## Переменные

- `default_model` (str): Модель, используемая по умолчанию для генерации текста.
- `default_image_model` (str): Модель, используемая по умолчанию для обработки изображений.
- `image_models` (List[str]): Список моделей, доступных для обработки изображений.
- `text_models` (List[str]): Список моделей, доступных для генерации текста.
- `fallback_models` (List[str]): Список всех доступных моделей (текстовых и визуальных).
- `model_aliases` (Dict[str, str]): Словарь, содержащий псевдонимы моделей для удобства использования.
- `extra_models` (List[str]): Список дополнительных моделей.
- `default_vision_model` (str): Модель компьютерного зрения, используемая по умолчанию.
- `default_llama_model` (str): Модель Llama, используемая по умолчанию.
- `vision_models` (List[str]): Список моделей компьютерного зрения.

## Таблица содержания

- [Переменные](#Переменные)

### `default_model`

```python
default_model = "Qwen/Qwen2.5-72B-Instruct"
```

- **Описание**: Модель, используемая по умолчанию для генерации текста.
- **Пример**:
  ```python
  print(default_model)
  ```

### `default_image_model`

```python
default_image_model = "black-forest-labs/FLUX.1-dev"
```

- **Описание**: Модель, используемая по умолчанию для обработки изображений.
- **Пример**:
  ```python
  print(default_image_model)
  ```

### `image_models`

```python
image_models = [    
    default_image_model,
    "black-forest-labs/FLUX.1-schnell",
]
```

- **Описание**: Список моделей, доступных для обработки изображений.
- **Пример**:
  ```python
  print(image_models)
  ```

### `text_models`

```python
text_models = [
    default_model,
    'meta-llama/Llama-3.3-70B-Instruct',
    'CohereForAI/c4ai-command-r-plus-08-2024',
    'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
    'Qwen/QwQ-32B',
    'nvidia/Llama-3.1-Nemotron-70B-Instruct-HF',
    'Qwen/Qwen2.5-Coder-32B-Instruct',
    'meta-llama/Llama-3.2-11B-Vision-Instruct',
    'mistralai/Mistral-Nemo-Instruct-2407',
    'microsoft/Phi-3.5-mini-instruct',
]
```

- **Описание**: Список моделей, доступных для генерации текста.
- **Пример**:
  ```python
  print(text_models)
  ```

### `fallback_models`

```python
fallback_models = text_models + image_models
```

- **Описание**: Список всех доступных моделей (текстовых и визуальных).
- **Пример**:
  ```python
  print(fallback_models)
  ```

### `model_aliases`

```python
model_aliases = {
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

- **Описание**: Словарь, содержащий псевдонимы моделей для удобства использования.
- **Пример**:
  ```python
  print(model_aliases)
  ```

### `extra_models`

```python
extra_models = [
    "meta-llama/Llama-3.2-11B-Vision-Instruct",
    "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
    "NousResearch/Hermes-3-Llama-3.1-8B",
]
```

- **Описание**: Список дополнительных моделей.
- **Пример**:
  ```python
  print(extra_models)
  ```

### `default_vision_model`

```python
default_vision_model = "meta-llama/Llama-3.2-11B-Vision-Instruct"
```

- **Описание**: Модель компьютерного зрения, используемая по умолчанию.
- **Пример**:
  ```python
  print(default_vision_model)
  ```

### `default_llama_model`

```python
default_llama_model = "meta-llama/Llama-3.3-70B-Instruct"
```

- **Описание**: Модель Llama, используемая по умолчанию.
- **Пример**:
  ```python
  print(default_llama_model)
  ```

### `vision_models`

```python
vision_models = [default_vision_model, "Qwen/Qwen2-VL-7B-Instruct"]
```

- **Описание**: Список моделей компьютерного зрения.
- **Пример**:
  ```python
  print(vision_models)