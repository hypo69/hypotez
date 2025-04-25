# Модуль AllenAI: Провайдер GPT-4 Free для работы с AI2 Playground

## Обзор

Модуль `AllenAI` предоставляет реализацию асинхронного провайдера для генерации текста с использованием API сервиса AI2 Playground. Он реализует интерфейсы `AsyncGeneratorProvider` и `ProviderModelMixin` для работы с асинхронными генераторами и поддержкой различных моделей.

## Детали

### Класс `Conversation`

```python
class Conversation(JsonConversation):
    parent: str = None
    x_anonymous_user_id: str = None

    def __init__(self, model: str):
        super().__init__()  # Ensure parent class is initialized
        self.model = model
        self.messages = []  # Instance-specific list
        if not self.x_anonymous_user_id:
            self.x_anonymous_user_id = str(uuid4())
```

**Описание**: Класс `Conversation` представляет собой контекст для общения с моделью, содержащий историю сообщений, родительский идентификатор и идентификатор анонимного пользователя. Он наследует от `JsonConversation` и дополняет его атрибутами для работы с API AI2 Playground.

**Атрибуты**:

- `parent` (str): Идентификатор родительского сообщения, если оно есть.
- `x_anonymous_user_id` (str): Уникальный идентификатор анонимного пользователя, генерируемый при создании объекта.
- `model` (str): Имя модели, используемой в контексте общения.
- `messages` (list): Список сообщений в контексте общения.


### Класс `AllenAI`

```python
class AllenAI(AsyncGeneratorProvider, ProviderModelMixin):
    label = "Ai2 Playground"
    url = "https://playground.allenai.org"
    login_url = None
    api_endpoint = "https://olmo-api.allen.ai/v4/message/stream"

    working = True
    needs_auth = False
    use_nodriver = False
    supports_stream = True
    supports_system_message = False
    supports_message_history = True

    default_model = 'tulu3-405b'
    models = [
        default_model,
        'OLMo-2-1124-13B-Instruct',
        'tulu-3-1-8b',
        'Llama-3-1-Tulu-3-70B',
        'olmoe-0125'
    ]

    model_aliases = {
        "tulu-3-405b": default_model,
        "olmo-2-13b": "OLMo-2-1124-13B-Instruct",
        "tulu-3-1-8b": "tulu-3-1-8b",
        "tulu-3-70b": "Llama-3-1-Tulu-3-70B",
        "llama-3.1-405b": "tulu3-405b",
        "llama-3.1-8b": "tulu-3-1-8b",
        "llama-3.1-70b": "Llama-3-1-Tulu-3-70B",
    }
```

**Описание**: Класс `AllenAI` реализует асинхронный провайдер для работы с API AI2 Playground, предоставляя возможность взаимодействовать с различными моделями, получать результаты в режиме потоковой передачи, сохранять историю сообщений и др.

**Атрибуты**:

- `label` (str): Название провайдера.
- `url` (str): URL-адрес сервиса AI2 Playground.
- `login_url` (str): URL-адрес для входа, не используется в данном провайдере.
- `api_endpoint` (str): URL-адрес API для потоковой передачи сообщений.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `needs_auth` (bool): Флаг, указывающий на необходимость авторизации.
- `use_nodriver` (bool): Флаг, указывающий на использование Selenium webdriver (не используется).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (не используется).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Имя модели по умолчанию.
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь алиасов для имен моделей.

### Метод `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        host: str = "inferd",
        private: bool = True,
        top_p: float = None,
        temperature: float = None,
        conversation: Conversation = None,
        return_conversation: bool = False,
        **kwargs
    ) -> AsyncResult:
        prompt = format_prompt(messages) if conversation is None else get_last_user_message(messages)
        # Initialize or update conversation
        if conversation is None:
            conversation = Conversation(model)

        # Generate new boundary for each request
        boundary = f"----WebKitFormBoundary{uuid4().hex}"

        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": f"multipart/form-data; boundary={boundary}",
            "origin": cls.url,
            "referer": f"{cls.url}/",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "x-anonymous-user-id": conversation.x_anonymous_user_id,
        }

        # Build multipart form data
        form_data = [
            f'--{boundary}\\r\\n'
            f'Content-Disposition: form-data; name="model"\\r\\n\\r\\n{cls.get_model(model)}\\r\\n',

            f'--{boundary}\\r\\n'
            f'Content-Disposition: form-data; name="host"\\r\\n\\r\\n{host}\\r\\n',

            f'--{boundary}\\r\\n'
            f'Content-Disposition: form-data; name="content"\\r\\n\\r\\n{prompt}\\r\\n',

            f'--{boundary}\\r\\n'
            f'Content-Disposition: form-data; name="private"\\r\\n\\r\\n{str(private).lower()}\\r\\n'
        ]

        # Add parent if exists in conversation
        if conversation.parent:
            form_data.append(
                f'--{boundary}\\r\\n'
                f'Content-Disposition: form-data; name="parent"\\r\\n\\r\\n{conversation.parent}\\r\\n'
            )

        # Add optional parameters
        if temperature is not None:
            form_data.append(
                f'--{boundary}\\r\\n'
                f'Content-Disposition: form-data; name="temperature"\\r\\n\\r\\n{temperature}\\r\\n'
            )

        if top_p is not None:
            form_data.append(
                f'--{boundary}\\r\\n'
                f'Content-Disposition: form-data; name="top_p"\\r\\n\\r\\n{top_p}\\r\\n'
            )

        form_data.append(f'--{boundary}--\\r\\n')
        data = "".join(form_data).encode()

        async with ClientSession(headers=headers) as session:
            async with session.post(
                cls.api_endpoint,
                data=data,
                proxy=proxy,
            ) as response:
                await raise_for_status(response)
                current_parent = None

                async for chunk in response.content:
                    if not chunk:
                        continue
                    decoded = chunk.decode(errors="ignore")
                    for line in decoded.splitlines():
                        line = line.strip()
                        if not line:
                            continue

                        try:
                            data = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        if isinstance(data, dict):
                            # Update the parental ID
                            if data.get("children"):
                                for child in data["children"]:
                                    if child.get("role") == "assistant":
                                        current_parent = child.get("id")
                                        break

                            # We process content only from the assistant
                            if "message" in data and data.get("content"):
                                content = data["content"]
                                # Skip empty content blocks
                                if content.strip():
                                    yield content

                            # Processing the final response
                            if data.get("final") or data.get("finish_reason") == "stop":
                                if current_parent:
                                    conversation.parent = current_parent

                                # Add a message to the story
                                conversation.messages.extend([
                                    {"role": "user", "content": prompt},
                                    {"role": "assistant", "content": content}
                                ])

                                if return_conversation:
                                    yield conversation

                                yield FinishReason("stop")
                                return

```

**Описание**: Метод `create_async_generator` создает асинхронный генератор для потоковой передачи ответов от модели AI2 Playground. Он принимает параметры, такие как модель, сообщения, прокси-сервер, флаги приватности, параметры регулировки температуры и top_p, а также параметры контекста общения.

**Параметры**:

- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений для отправки модели.
- `proxy` (str): URL-адрес прокси-сервера.
- `host` (str): Имя хоста (используется для отправки данных на API AI2 Playground).
- `private` (bool): Флаг, указывающий на режим приватности запроса.
- `top_p` (float): Параметр регулировки вероятности отбора слов.
- `temperature` (float): Параметр регулировки температуры генерации.
- `conversation` (Conversation): Объект контекста общения.
- `return_conversation` (bool): Флаг, указывающий на необходимость возврата обновленного контекста общения в качестве результата генератора.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, который выдает частичные ответы модели в режиме потоковой передачи.

**Как работает**:

- Метод формирует HTTP-запрос к API AI2 Playground с использованием multipart/form-data.
- В запросе передаются параметры, такие как модель, сообщения, прокси-сервер, флаги приватности, параметры регулировки температуры и top_p, а также параметры контекста общения.
- После получения ответа от API, метод обрабатывает его в режиме потоковой передачи, выдавая частичные ответы модели по мере их поступления.
- В конце генерации, метод возвращает обновленный контекст общения (если параметр `return_conversation` установлен в `True`) и флаг `FinishReason("stop")`, сигнализирующий о завершении генерации.