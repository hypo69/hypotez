# FreeGPT WebUI

## Обзор

Этот модуль предоставляет доступ к ChatGPT с вашего компьютера без использования VPN. В настоящее время поддерживаются ChatGPT 3.5 Turbo, веб-доступ для бота и джейлбрейки для расширения возможностей.

## Подробней

Модуль представляет собой WebUI для доступа к бесплатным GPT моделям, таким как ChatGPT 3.5/4. Он включает в себя веб-интерфейс, интеграцию с API G4F (GPT4Free) и предоставляет возможности для использования джейлбрейков.

## Установка

### Windows

1.  Скачайте и установите [git](https://git-scm.com/download/win). Скачайте и установите [Python 3.10.X](https://www.python.org/downloads/). Убедитесь, что Python добавлен в PATH.
    *   Если в процессе установки возникают ошибки, связанные с Visual Studio, скачайте [Visual Studio](https://visualstudio.microsoft.com/ru/downloads/) для компиляции библиотек.
2.  Скачайте репозиторий. Для этого откройте Командную строку (Терминал) в папке, где хотите разместить `freegpt-webui-ru`, и выполните команду:

```bash
git clone https://github.com/Em1tSan/freegpt-webui-ru.git
```

3.  Откройте папку `freegpt-webui-ru` и запустите файл `install.bat`, а затем `start.bat`.

Он создаст виртуальное окружение, установит зависимости и запустит скрипт.

4.  Перейдите в браузере по адресу: `http://127.0.0.1:1338`.

Если у вас возникли трудности с установкой классическим путем, попробуйте портативную версию. В ней предустановлено всё необходимое, поэтому достаточно только распаковать и запустить.

Для других ОС инструкция для установки и запуска будет добавлена позже.

### Портативная версия

Портативная версия не требует установки Python. [Скачать ее можно в релизах](https://github.com/Em1tSan/freegpt-webui-ru/releases).

## Поддержка и вопросы

Если у вас возникли какие-либо вопросы или вы хотите обсудить проект, это можно сделать в Telegram-канале: [https://t.me/neurogen_news](https://t.me/neurogen_news).

## Incorporated Projects

Рекомендуется посетить и поддержать следующие проекты:

*   **WebUI**: Интерфейс приложения был взят из репозитория [chatgpt-clone](https://github.com/xtekky/chatgpt-clone).
*   **API G4F**: Бесплатный GPT-4 API был взят из репозитория [GPT4Free](https://github.com/xtekky/gpt4free).

## Legal Notice

Этот репозиторий **не** связан и не поддерживается провайдерами API, содержащихся в этом репозитории GitHub. Этот проект предназначен **только для образовательных целей**. Это всего лишь небольшой личный проект. Сайты могут связаться с автором для улучшения своей безопасности или запросить удаление их сайта из этого репозитория.

Обратите внимание на следующее:

1.  **Disclaimer**: API, сервисы и торговые марки, упомянутые в этом репозитории, принадлежат их соответствующим владельцам. Этот проект **не** претендует на какие-либо права на них и не связан и не поддерживается ни одним из упомянутых провайдеров.
2.  **Responsibility**: Автор этого репозитория **не** несет ответственности за какие-либо последствия, убытки или ущерб, возникшие в результате использования или неправильного использования этого репозитория или контента, предоставляемого сторонними API. Пользователи несут единоличную ответственность за свои действия и любые последствия, которые могут возникнуть. Настоятельно рекомендуется пользователям соблюдать Условия обслуживания каждого веб-сайта.
3.  **Educational Purposes Only**: Этот репозиторий и его контент предоставляются исключительно для образовательных целей. Используя предоставленную информацию и код, пользователи признают, что они используют API и модели на свой страх и риск, и соглашаются соблюдать любые применимые законы и правила.
4.  **Copyright**: Весь контент в этом репозитории, включая, помимо прочего, код, изображения и документацию, является интеллектуальной собственностью автора репозитория, если не указано иное. Несанкционированное копирование, распространение или использование любого контента в этом репозитории строго запрещено без явного письменного согласия автора репозитория.
5.  **Indemnification**: Пользователи соглашаются возмещать убытки, защищать и ограждать автора этого репозитория от любых претензий, обязательств, убытков, ущерба или расходов, включая гонорары и издержки адвокатов, возникающие из-за или каким-либо образом связанные с их использованием или неправильным использованием этого репозитория, его содержимого или связанных сторонних API.
6.  **Updates and Changes**: Автор оставляет за собой право изменять, обновлять или удалять любой контент, информацию или функции в этом репозитории в любое время без предварительного уведомления. Пользователи несут ответственность за регулярный просмотр контента и любых изменений, внесенных в этот репозиторий.

Используя этот репозиторий или любой связанный с ним код, вы соглашаетесь с этими условиями. Автор не несет ответственности за какие-либо копии, форки или повторные загрузки, сделанные другими пользователями. Это единственная учетная запись и репозиторий автора. Чтобы предотвратить выдачу себя за другого или безответственные действия, вы можете соблюдать лицензию GNU GPL, которую использует этот репозиторий.