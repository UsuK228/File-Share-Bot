# Telegram File Bot
## Бот для управления файлами через Telegram с возможностью загрузки, скачивания и организации файлов.

# Возможности
📁 Загрузка файлов в облачное хранилище через Telegram

📥 Скачивание файлов по запросу

👥 Поддержка многопользовательского режима

# Установка и настройка
## Предварительные требования
Python 3.8+
Telegram Bot Token (получить у @BotFather)
Установленный pip

# Установка
Клонируйте репозиторий:
`git clone https://github.com/UsuK228/File-Share-Bot.git`
`cd File-Share-Bot`

# Установите зависимости:
`pip install -r requirements.txt`

# Отредактируйте main.py:
`API_TOKEN = "your_bot_token_here"`
`ADMINS = ["12345", "54321"]` - Ваш (Ваши) ID

№ Запустите бота:
`python main.py`

# Основные команды
`/start` - Начать работу с ботом и справка по командам

`/stats` - Показать справку по командам

`/file <fileid>` - Показать список файлов

`/filedel <fileid>` - Удалить файл

`/admin` - Посмотреть все ID файлов в базе данных (Только для админов!)

# Загрузка файлов
Отправьте боту любой файл и получите ID файла в боте.

# Структура проекта
File-Share-Bot/

├── main.py            # Основной файл бота

├── requirements.txt   # Зависимости Python

├── files_data.json/   # База данных с id файлов

├── database/          # База данных пользователей

├── README.md          # Этот файл

└── LICENSE            # Файл лицензии

# Развертывание
## Локальный запуск
`python bot.py`
## Запуск в фоновом режиме (Linux)
`nohup python bot.py > bot.log 2>&1 &`
## Docker (опционально)
`docker build -t telegram-file-bot .`
`docker run -d --name file-bot telegram-file-bot`

# Лицензия
Этот проект распространяется под лицензией MIT. См. файл LICENSE для подробностей.

⭐ Если вам понравился этот проект, поставьте звезду на GitHub!
