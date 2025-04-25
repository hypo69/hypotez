### **Как использовать этот блок кода**
=========================================================================================

**Описание**
-------------------------
Этот блок кода генерирует документацию для модуля `src.endpoints.bots` в формате `reStructuredText` (reST). 

**Шаги выполнения**
-------------------------
1. **Создание заголовка модуля:**  Вставляется строка `.. module:: src.endpoints.bots`  
2. **Создание ссылки на корневой README:** Вставляется строка `[Root ↑](https://github.com/hypo69/hypotez/blob/master/REDAME.MD)` 
3. **Создание ссылки на README модуля src:** Вставляется строка `[src](https://github.com/hypo69/hypotez/blob/master/src/bots/REDAME.MD)` 
4. **Создание ссылки на README модуля на русском:** Вставляется строка `[Русский](https://github.com/hypo69/hypotez/blob/master/src/bots/readme.ru.md)`

**Пример использования**
-------------------------

```python
                ```rst
.. module:: src.endpoints.bots
```

[Root ↑](https://github.com/hypo69/hypotez/blob/master/REDAME.MD)

[src](https://github.com/hypo69/hypotez/blob/master/src/bots/REDAME.MD) 

[Русский](https://github.com/hypo69/hypotez/blob/master/src/bots/readme.ru.md)