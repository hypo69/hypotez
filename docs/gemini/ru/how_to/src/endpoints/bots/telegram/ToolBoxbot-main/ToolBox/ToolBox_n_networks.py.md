### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `neural_networks`, который предоставляет методы для взаимодействия с различными нейронными сетями. В частности, он включает методы для генерации изображений на основе текстовых запросов и для получения текстовых ответов от моделей чат-ботов.

Шаги выполнения
-------------------------
1. **Импорт библиотек**: Импортируются необходимые библиотеки, такие как `requests` для выполнения HTTP-запросов, `json` для работы с данными в формате JSON, `os` для доступа к переменным окружения, `io` для работы с потоками ввода-вывода, `randint` для генерации случайных чисел и `Image` из библиотеки `PIL` для работы с изображениями.
2. **Определение класса `neural_networks`**: Создается класс `neural_networks`, который будет содержать методы для работы с различными нейронными сетями.
3. **Метод `_FLUX_schnell`**:
   - Функция принимает текстовый запрос `prompt`, размер изображения `size` (ширина и высота), случайное число `seed` и количество шагов `num_inference_steps`.
   - Формируется полезная нагрузка (payload) с параметрами для запроса к API.
   - Выполняются POST-запросы к API "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell" с использованием токенов авторизации из переменных окружения `HF_TOKEN{i}` (где `i` от 1 до 7).
   - Если запрос успешен (код состояния 200), изображение открывается из полученного содержимого и возвращается.
4. **Метод `__mistral_large_2407`**:
    - Функция принимает список словарей `prompt`, содержащий текстовые запросы для модели.
    - Формируются данные для запроса к API Mistral.
    - Выполняется POST-запрос к API "https://api.mistral.ai/v1/chat/completions" с использованием токена авторизации из переменной окружения `MISTRAL_TOKEN`.
    - Функция возвращает текстовый ответ модели, количество токенов в запросе и количество токенов в ответе.
5. **Метод `_free_gpt_4o_mini`**:
   - Функция принимает список словарей `prompt`, содержащий текстовые запросы для модели.
   - Формируются данные для запроса к API.
   - Выполняются POST-запросы к API "https://models.inference.ai.azure.com/chat/completions" с использованием токенов авторизации из переменных окружения `GIT_TOKEN{i}` (где `i` от 1 до 7).
   - Если запрос успешен (код состояния 200), функция возвращает текстовый ответ модели, количество токенов в запросе и количество токенов в ответе.
   - Если ни один из запросов не успешен, вызывается метод `__mistral_large_2407` для получения ответа от другой модели.

Пример использования
-------------------------

```python
from src.endpoints.bots.telegram.ToolBoxbot-main.ToolBox.ToolBox_n_networks import neural_networks
import os

# Создание экземпляра класса neural_networks
nn = neural_networks()

# Пример использования метода _FLUX_schnell
# Установите переменные окружения HF_TOKEN1, HF_TOKEN2, ..., HF_TOKEN7
os.environ["HF_TOKEN1"] = "your_huggingface_token_1"
os.environ["HF_TOKEN2"] = "your_huggingface_token_2"
os.environ["HF_TOKEN3"] = "your_huggingface_token_3"
os.environ["HF_TOKEN4"] = "your_huggingface_token_4"
os.environ["HF_TOKEN5"] = "your_huggingface_token_5"
os.environ["HF_TOKEN6"] = "your_huggingface_token_6"
# prompt = "A futuristic cityscape"
# size = [512, 512]
# seed = 42
# num_inference_steps = 30
# image = nn._FLUX_schnell(prompt, size, seed, num_inference_steps)
# if image:
#     image.save("futuristic_cityscape.png")
#     print("Изображение успешно сгенерировано и сохранено.")
# else:
#     print("Не удалось сгенерировать изображение.")

# Пример использования метода _free_gpt_4o_mini
# Установите переменные окружения GIT_TOKEN1, GIT_TOKEN2, ..., GIT_TOKEN7 и MISTRAL_TOKEN
os.environ["GIT_TOKEN1"] = "your_git_token_1"
os.environ["GIT_TOKEN2"] = "your_git_token_2"
os.environ["GIT_TOKEN3"] = "your_git_token_3"
os.environ["GIT_TOKEN4"] = "your_git_token_4"
os.environ["GIT_TOKEN5"] = "your_git_token_5"
os.environ["GIT_TOKEN6"] = "your_git_token_6"
os.environ["MISTRAL_TOKEN"] = "your_mistral_token"
# prompt = [{"role": "user", "content": "Напиши короткий рассказ о космическом путешествии."}]
# response, prompt_tokens, completion_tokens = nn._free_gpt_4o_mini(prompt)
# print(f"Ответ: {response}")
# print(f"Токены в запросе: {prompt_tokens}")
# print(f"Токены в ответе: {completion_tokens}")