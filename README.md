# DialogFlow Bot

Простой бот для Telegram и VK, подключенный к [DialogFlow](https://dialogflow.cloud.google.com). Способен отвечать на вопросы собеседников заранее заготовленными ответами.

## Установка

Для запуска программы должен быть установлен Python 3.

Скачайте код и установите требуемые библиотеки командой

```bash
pip install -r requirements.txt

```

## Переменные окружения

Для запуска ботов понадобится `.env` файл следующего содержимого:

* `TG_BOT_TOKEN` - токен Telegram бота. Получается у [@BotFather](https://telegram.me/BotFather)
* `GOOGLE_APPLICATION_CREDENTIALS` - Путь к JSON-файлу с ключом к Google Cloud.
Получается [таким образом](https://cloud.google.com/dialogflow/es/docs/quick/setup#sa-create)
* `GOOGLE_CLOUD_PROJECT_ID` - ID проекта Google Cloud. Лежит в JSON-файле, полученном выше под ключом 'project_id'
* `VK_API_TOKEN` - получается в настройках группы VK в разделе "Работа с API". Требует право доступа к сообщениям сообщества.
* `TG_CHAT_ID`=1285793181
* `TG_LOG_BOT_TOKEN` - токен запасного Telegram бота. Получается у [@BotFather](https://telegram.me/BotFather)

## Intents

Чтобы боты могли отвечать пользователям, нужно передать DialogFlow Intent-ы c тренировочными фразами и ответами. Для создания intent-ов DialogFlow понадобится JSON-файл следующего содержимого:

```json
{
    "Название Intent-a": {
        "questions": [
        	"Список сообщений пользователя для обучения DialogFlow",
        	"...",
        ],
        "answer": "Ожидаемый ответ на сообщения"
    },
    "Следующий Intent": {
    	"..."
    },
    "..."
}

```

Тестовый JSON-файл с тренировочными фразами можно скачать [здесь](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json)

Процесс обучения DialogFlow запускается командой

```bash
python intents.py intents.py  # аргумент - путь к JSON-файлу

```

Результам обучения доступен [здесь](https://dialogflow.cloud.google.com)

## Запуск ботов

Боты запускаются командами 

```bash
python tgbot.py

```

```bash
python vkbot.py

```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).