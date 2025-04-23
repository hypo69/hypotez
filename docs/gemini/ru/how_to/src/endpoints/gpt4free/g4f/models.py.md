### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет набор классов и объектов, которые представляют различные модели машинного обучения и способы доступа к ним через различных провайдеров. Он включает в себя модели для текста, аудио и изображений, а также утилиты для сопоставления строковых идентификаторов с экземплярами моделей.

Шаги выполнения
-------------------------
1. **Определение классов моделей**:
   - Класс `Model` определяет основные атрибуты модели, такие как имя, базовый провайдер и лучший провайдер (с логикой повторных попыток).
   - Классы `ImageModel`, `AudioModel` и `VisionModel` наследуются от `Model` и представляют специфические типы моделей.

2. **Создание экземпляров моделей**:
   - Создаются экземпляры моделей для различных провайдеров, таких как OpenAI, Meta, Google и других.
   - Для каждой модели указывается имя, базовый провайдер и лучший провайдер, который может быть как конкретным провайдером, так и списком провайдеров с логикой перебора.

3. **Использование класса `ModelUtils`**:
   - Класс `ModelUtils` содержит словарь `convert`, который сопоставляет строковые идентификаторы моделей с их экземплярами.
   - Этот словарь используется для удобного доступа к моделям по их именам.

4. **Создание списка всех моделей**:
   - Создается словарь `__models__`, который содержит все модели и их доступных провайдеров.
   - Из этого словаря извлекается список всех имен моделей `_all_models`.

Пример использования
-------------------------

```python
    from .Provider import AllenAI, Blackbox, ChatGLM, ChatGptEs, Cloudflare
    from .Provider import DDG, DeepInfraChat, Dynaspark, Free2GPT, FreeGpt
    from .Provider import HuggingSpace, G4F, Grok, DeepseekAI_JanusPro7b, Glider
    from .Provider import Goabror, ImageLabs, Jmuz, LambdaChat, Liaobots, OIVSCode
    from .Provider import PerplexityLabs, Pi, PollinationsAI, PollinationsImage
    from .Provider import TypeGPT, TeachAnything, Websim, Yqcloud
    from .Provider import BingCreateImages, CopilotAccount, Gemini, GeminiPro, GigaChat
    from .Provider import HailuoAI, HuggingChat, HuggingFace, HuggingFaceAPI, MetaAI
    from .Provider import MicrosoftDesigner, OpenaiAccount, OpenaiChat, Reka

    @dataclass(unsafe_hash=True)
    class Model:
        """
        Представляет конфигурацию модели машинного обучения.

        Attributes:
            name (str): Имя модели.
            base_provider (str): Базовый провайдер для модели.
            best_provider (ProviderType): Предпочтительный провайдер для модели, обычно с логикой повторных попыток.
        """
        name: str
        base_provider: str
        best_provider: ProviderType = None

    gpt_3_5_turbo = Model(
        name          = 'gpt-3.5-turbo',
        base_provider = 'OpenAI'
    )

    gpt_4 = Model(
        name          = 'gpt-4',
        base_provider = 'OpenAI',
        best_provider = IterListProvider([DDG, Jmuz, ChatGptEs, PollinationsAI, Yqcloud, Goabror, Copilot, OpenaiChat, Liaobots])
    )

    class ModelUtils:
        """
        Утилитный класс для сопоставления строковых идентификаторов с экземплярами моделей.

        Attributes:
            convert (dict[str, Model]): Словарь, сопоставляющий строковые идентификаторы моделей с экземплярами моделей.
        """
        convert: dict[str, Model] = { 
            gpt_3_5_turbo.name: gpt_3_5_turbo,
            gpt_4.name: gpt_4,
        }

    __models__  = {
        model.name: (model, providers)
            for model, providers in [(model, [provider for provider in model.best_provider.providers if provider.working]
                    if isinstance(model.best_provider, IterListProvider)
                    else [model.best_provider]
                    if model.best_provider is not None and model.best_provider.working
                    else [])
                for model in ModelUtils.convert.values()]
            if providers
        }
    _all_models = list(__models__.keys())