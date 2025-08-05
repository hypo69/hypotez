## Как использовать класс `neural_networks`
=========================================================================================

Описание
-------------------------
Класс `neural_networks` предоставляет доступ к различным нейронным сетям для выполнения задач, таких как генерация изображений и текста. Он содержит защищенные методы, которые взаимодействуют с API различных сервисов нейронных сетей, таких как Hugging Face, Mistral и Azure AI.

Шаги выполнения
-------------------------
1. **Инициализация класса**: Создайте экземпляр класса `neural_networks`.
2. **Выбор метода**: Выберите нужный защищенный метод, соответствующий API сервиса, с которым вы хотите взаимодействовать. 
3. **Передача параметров**:  Передайте необходимые параметры в выбранный метод, такие как:
    -  `prompt`: Текстовая подсказка для генерации изображения или текста.
    -  `size`: Размеры изображения (ширина, высота).
    -  `seed`: Значение начальной точки для генерации изображений.
    -  `num_inference_steps`: Количество шагов для генерации изображения.
4. **Получение результата**: Метод возвращает результат: изображение (в формате `PIL.Image`), текст (в формате `str`) или кортеж (текст, количество токенов запроса, количество токенов ответа). 

Пример использования
-------------------------

```python
from ToolBox.ToolBox_n_networks import neural_networks

# Инициализация класса
nn = neural_networks()

# Генерация изображения с помощью FLUX.1-schnell (Hugging Face)
image = nn._FLUX_schnell(prompt="A cat sitting on a chair", size=[512, 512], seed=42, num_inference_steps=50)

# Генерация текста с помощью Mistral (Mistral AI)
prompt = [
    {"role": "user", "content": "What is the meaning of life?"},
]
text, prompt_tokens, completion_tokens = nn.__mistral_large_2407(prompt)

# Генерация текста с помощью GPT-4o-mini (Azure AI)
prompt = [
    {"role": "user", "content": "Write a short story about a robot who dreams."},
]
text, prompt_tokens, completion_tokens = nn._free_gpt_4o_mini(prompt)

# Вывод результатов
if image:
    image.show()
print(f"Text: {text}")
print(f"Prompt tokens: {prompt_tokens}")
print(f"Completion tokens: {completion_tokens}")
```