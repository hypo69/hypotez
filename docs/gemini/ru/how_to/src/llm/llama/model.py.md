## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код демонстрирует использование библиотеки `llama_cpp` для загрузки и использования модели Llama. 

Шаги выполнения
-------------------------
1. **Импорт библиотеки:**  `from llama_cpp import Llama` -  импортирует необходимую библиотеку для работы с Llama.
2. **Загрузка модели:**  `llm = Llama.from_pretrained(...)` - загрузка модели с Hugging Face (в данном случае -  Meta-Llama-3.1-8B-Instruct-GGUF).
    - Параметр `repo_id` -  идентификатор репозитория на Hugging Face.
    - Параметр `filename` - имя файла с моделью.
3. **Генерация текста:** `output = llm(...)` -  генерация текста с помощью модели Llama.
    -  Параметр `...` -  вводный текст для генерации, например: `"Once upon a time,"`.
    - Параметр `max_tokens` - максимальное количество токенов для генерации.
    -  Параметр `echo` - флаг, указывающий, нужно ли возвращать входной текст в качестве части вывода.
4. **Вывод:**  `print(output)` -  печать сгенерированного текста.

Пример использования
-------------------------

```python
from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
    filename="Meta-Llama-3.1-8B-Instruct-IQ4_XS.gguf",
)

output = llm(
    "The quick brown fox jumps over the lazy dog.", 
    max_tokens=10,
    echo=True
)
print(output)
```
В этом примере модель Llama получит предложение "The quick brown fox jumps over the lazy dog." и сгенерирует продолжение.