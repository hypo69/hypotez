### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предназначен для автоматического перевода документа README.md на другой язык с использованием GPT-4. Он разделяет README на части, переводит каждую часть, сохраняя при этом определенные элементы кода без изменений.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**:
   - Импортируются библиотеки `sys`, `pathlib`, `asyncio`, `g4f`.
   - `g4f` используется для взаимодействия с API GPT-4.

2. **Настройка путей и параметров**:
   - Добавляется путь к родительскому каталогу для импорта модуля `g4f`.
   - Включается логирование `g4f.debug.logging = True`.
   - Указывается провайдер `g4f.Provider.OpenaiChat`.
   - Определяются параметры перевода, такие как `iso` (страна), `language` (язык), и `translate_prompt` (начальный промпт для перевода).

3. **Определение списков блокировки и разрешения**:
   - `blocklist`: Список заголовков, которые не нужно переводить целиком.
   - `allowlist`: Список элементов, которые нужно переводить даже в заблокированных частях.

4. **Функция `read_text(text)`**:
   - Извлекает текст из markdown блока кода, находящегося между ```.
   - Определяет начало и конец блока кода.
   - Возвращает текст между этими блоками.

5. **Функция `translate(text)`**:
   - Формирует полный промпт для перевода, добавляя начальный промпт `translate_prompt` к тексту.
   - Если в тексте есть маркер "[!Note]", добавляет инструкцию `keep_note` для его сохранения.
   - Вызывает асинхронную функцию `provider.create_async` для получения перевода от GPT-4.
   - Возвращает переведенный текст.

6. **Функция `translate_part(part, i)`**:
   - Проверяет, содержится ли текущая часть в списке `blocklist`.
   - Если часть заблокирована, переводит только заголовок и элементы из `allowlist`.
   - Если часть не заблокирована, переводит всю часть текста.
   - Выводит сообщение о завершении перевода части.

7. **Функция `translate_readme(readme)`**:
   - Разделяет README на части по заголовку "## ".
   - Асинхронно переводит каждую часть, используя `translate_part`.
   - Объединяет переведенные части обратно в один текст.

8. **Основной блок кода**:
   - Открывает файл "README.md" для чтения.
   - Запускает асинхронный перевод всего README, используя `translate_readme`.
   - Сохраняет переведенный текст в новый файл с именем "README-{iso}.md".

Пример использования
-------------------------

```python
import sys
from pathlib import Path
import asyncio

sys.path.append(str(Path(__file__).parent.parent.parent))

import g4f
g4f.debug.logging = True
from g4f.debug import access_token
provider = g4f.Provider.OpenaiChat

iso = "GE"
language = "german"
translate_prompt = f"""
Translate this markdown document to {language}.
Don\'t translate or change inline code examples.
```md
"""
keep_note = "Keep this: [!Note] as [!Note].\\n"
blocklist = [
    '## ©️ Copyright',
    '## 🚀 Providers and Models',
    '## 🔗 Related GPT4Free Projects'
]
allowlist = [
    "### Other",
    "### Models"
]

def read_text(text):
    start = end = 0
    new = text.strip().split('\n')
    for i, line in enumerate(new):
        if line.startswith('```'):
            if not start:
                start = i + 1
            end = i
    return '\n'.join(new[start:end]).strip()

async def translate(text):
    prompt = translate_prompt + text.strip() + '\n```'
    if "[!Note]" in text:
        prompt = keep_note + prompt
    result = read_text(await provider.create_async(
        model="",
        messages=[{"role": "user", "content": prompt}],
        access_token=access_token
    ))
    if text.endswith("```") and not result.endswith("```"):
        result += "\\n```"
    return result

async def translate_part(part, i):
    blocklisted = False
    for headline in blocklist:
        if headline in part:
            blocklisted = True
    if blocklisted:
        lines = part.split('\n')
        lines[0] = await translate(lines[0])
        part = '\n'.join(lines)
        for trans in allowlist:
            if trans in part:
                part = part.replace(trans, await translate(trans))
    else:
        part = await translate(part)
    print(f"[{i}] translated")
    return part

async def translate_readme(readme) -> str:
    parts = readme.split('\n## ')
    print(f"{len(parts)} parts...")
    parts = await asyncio.gather(
        *[translate_part("## " + part, i) for i, part in enumerate(parts)]
    )
    return "\\n\\n".join(parts)

with open("README.md", "r") as fp:
    readme = fp.read()

print("Translate readme...")
readme = asyncio.run(translate_readme(readme))

file = f"README-{iso}.md"
with open(file, "w") as fp:
    fp.write(readme)
print(f'"{file}" saved')