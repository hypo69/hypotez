# FreeGPT WebUI: Доступ к ChatGPT с вашего ПК без VPN

## Обзор

FreeGPT WebUI - это проект, предоставляющий простой доступ к ChatGPT 3.5/4 с вашего ПК без необходимости использования VPN. Проект основан на проекте `chatgpt-clone` и предоставляет удобный веб-интерфейс для взаимодействия с ChatGPT. 

## Установка

### Windows

1. **Установите Git:** Скачайте и установите [Git](https://git-scm.com/download/win).
2. **Установите Python:** Скачайте и установите [Python 3.10.X](https://www.python.org/downloads/). Убедитесь, что опция добавления Python в PATH включена во время установки.
   - Если во время установки возникают ошибки, связанные с Visual Studio, скачайте [Visual Studio](https://visualstudio.microsoft.com/ru/downloads/) для компиляции библиотек.
3. **Скачайте репозиторий:** Откройте командную строку (терминал) в папке, где вы хотите разместить `freegpt-webui-ru`, и введите команду:
   ```bash
   git clone https://github.com/Em1tSan/freegpt-webui-ru.git
   ```
4. **Запустите установку:** Откройте папку `freegpt-webui-ru` и запустите файл `install.bat`, а затем `start.bat`. Это создаст виртуальную среду, установит зависимости и запустит сервер.
5. **Доступ к веб-интерфейсу:** Откройте браузер и перейдите по адресу: `http://127.0.0.1:1338`.

### Портативная версия

Портативная версия не требует установки Python. Ее можно скачать в [релизах](https://github.com/Em1tSan/freegpt-webui-ru/releases). 

## Поддержка и вопросы

Если у вас возникли вопросы или вы хотите обсудить проект, вы можете сделать это в моем телеграм канале: https://t.me/neurogen_news

## Включенные проекты

Проект FreeGPT WebUI использует компоненты из других репозиториев:

### WebUI

Веб-интерфейс проекта основан на репозитории [chatgpt-clone](https://github.com/xtekky/chatgpt-clone).

### API G4F

Бесплатный API GPT-4 был интегрирован из репозитория [GPT4Free](https://github.com/xtekky/gpt4free).

## Юридическая информация

Данный репозиторий не связан с поставщиками API, которые в нем используются, и не одобряется ими. Проект предназначен **только для образовательных целей**. Это всего лишь небольшой личный проект. 

**Обратите внимание на следующее:**

1. **Отказ от ответственности**: API, сервисы и торговые марки, упомянутые в этом репозитории, принадлежат их законным владельцам. Этот проект не претендует на какие-либо права на них и не связан с упомянутыми поставщиками.
2. **Ответственность**: Автор этого репозитория не несет ответственности за любые последствия, ущерб или убытки, возникшие в результате использования или неправильного использования этого репозитория или контента, предоставляемого сторонними API. Пользователи несут полную ответственность за свои действия и любые последствия, которые могут последовать. Мы настоятельно рекомендуем пользователям следовать Условиям использования каждого сайта.
3. **Только для образовательных целей**: Этот репозиторий и его содержимое предоставляются исключительно для образовательных целей. Используя предоставленную информацию и код, пользователи подтверждают, что они используют API и модели на свой страх и риск и соглашаются соблюдать все применимые законы и правила.
4. **Авторские права**: Все содержимое этого репозитория, включая, но не ограничиваясь, код, изображения и документацию, является интеллектуальной собственностью автора репозитория, если не указано иное. Несанкционированное копирование, распространение или использование любого контента в этом репозитории строго запрещено без письменного разрешения автора репозитория.
5. **Возмещение ущерба**: Пользователи соглашаются возместить убытки, защитить и оградить от ответственности автора этого репозитория от и против любых и всех претензий, обязательств, убытков, ущерба или расходов, включая юридические сборы и расходы, возникшие в связи с или каким-либо образом связанными с их использованием или неправильным использованием этого репозитория, его контента или связанных с ним сторонних API.
6. **Обновления и изменения**: Автор оставляет за собой право изменять, обновлять или удалять любое содержимое, информацию или функции в этом репозитории в любое время без предварительного уведомления. Пользователи несут ответственность за регулярный просмотр контента и любых изменений, внесенных в этот репозиторий.

Используя этот репозиторий или любой код, связанный с ним, вы соглашаетесь с этими условиями. Автор не несет ответственности за любые копии, форки или повторные загрузки, сделанные другими пользователями. Это единственный аккаунт и репозиторий автора. Чтобы предотвратить подделку личности или безответственные действия, вы можете соблюдать лицензию GNU GPL, используемую этим репозиторием.