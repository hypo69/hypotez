### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Данный код предоставляет реализацию различных типов памяти для агента, включая эпизодическую (EpisodicMemory) и семантическую (SemanticMemory). Эпизодическая память хранит последовательность событий, а семантическая память хранит знания и факты. Код содержит базовый класс TinyMemory и его подклассы, реализующие логику хранения и извлечения данных из памяти.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются классы `TinyMentalFaculty` и `BaseSemanticGroundingConnector`, а также модуль `utils`.
   - Импортируются классы `Document` из `llama_index.core` и `Any` из `typing`.

2. **Создание класса `TinyMemory`**:
   - Определяется абстрактный базовый класс `TinyMemory`, который наследуется от `TinyMentalFaculty`.
   - Реализуется метод `_preprocess_value_for_storage`, который выполняет предварительную обработку значения перед сохранением в память (по умолчанию не выполняет никаких действий).
   - Определяются абстрактные методы `_store`, `retrieve`, `retrieve_recent`, `retrieve_all` и `retrieve_relevant`, которые должны быть реализованы в подклассах.
   - Реализуются методы `store` и `store_all` для сохранения одного или нескольких значений в памяти.

3. **Создание класса `EpisodicMemory`**:
   - Определяется класс `EpisodicMemory`, который наследуется от `TinyMemory`.
   - Инициализируется с параметрами `fixed_prefix_length` и `lookback_length`, определяющими длину фиксированного префикса и окна просмотра для извлечения последних значений.
   - Реализуется метод `_store` для добавления значения в список `memory`.
   - Реализуются методы `retrieve`, `retrieve_recent`, `retrieve_all`, `retrieve_first` и `retrieve_last` для извлечения данных из памяти в различных вариантах.

4. **Создание класса `SemanticMemory`**:
   - Определяется класс `SemanticMemory`, который наследуется от `TinyMemory`.
   - Инициализируется с параметром `memories`, представляющим список сохраненных воспоминаний.
   - Используется декоратор `@utils.post_init` для вызова метода `_post_init` после инициализации объекта.
   - В методе `_post_init` инициализируется `semantic_grounding_connector` типа `BaseSemanticGroundingConnector` и добавляются документы, построенные из воспоминаний.
   - Реализуется метод `_preprocess_value_for_storage` для предварительной обработки значения перед сохранением в память, формируя текстовое представление воспоминания в зависимости от его типа (`action` или `stimulus`).
   - Реализуется метод `_store` для добавления документа, построенного из воспоминания, в `semantic_grounding_connector`.
   - Реализуется метод `retrieve_relevant` для извлечения релевантных значений из памяти с использованием `semantic_grounding_connector`.
   - Реализуются вспомогательные методы `_build_document_from` и `_build_documents_from` для построения документов из воспоминаний.

Пример использования
-------------------------

```python
from tinytroupe.agent.memory import EpisodicMemory, SemanticMemory

# Использование EpisodicMemory
episodic_memory = EpisodicMemory(fixed_prefix_length=5, lookback_length=10)
episodic_memory.store({"role": "user", "content": "Hello, how are you?"})
episodic_memory.store({"role": "assistant", "content": "I'm fine, thank you."})
recent_memory = episodic_memory.retrieve_recent()
print(f"Recent memory: {recent_memory}")

# Использование SemanticMemory
semantic_memory = SemanticMemory()
semantic_memory.store({"type": "action", "simulation_timestamp": "2024-01-01 12:00:00", "content": "I went to the store."})
semantic_memory.store({"type": "stimulus", "simulation_timestamp": "2024-01-01 12:05:00", "content": "I saw a cat."})
relevant_memory = semantic_memory.retrieve_relevant("store")
print(f"Relevant memory: {relevant_memory}")