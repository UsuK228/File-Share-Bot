# Telegram File Bot
Бот для управления файлами через Telegram с возможностью загрузки, скачивания и организации файлов.

# Возможности
📁 Загрузка файлов в облачное хранилище через Telegram

📥 Скачивание файлов по запросу

🔍 Поиск файлов по имени и типу

📂 Организация файлов по категориям

👥 Поддержка многопользовательского режима

🔐 Базовые права доступа (только для авторизованных пользователей)

# Установка и настройка
# Предварительные требования
Python 3.8+
Telegram Bot Token (получить у @BotFather)
Установленный pip

# Установка
Клонируйте репозиторий:
```git clone https://github.com/your-username/telegram-file-bot.git```
```cd telegram-file-bot```
Установите зависимости:

bash
pip install -r requirements.txt
Настройте конфигурацию:

bash
cp config.example.py config.py
Отредактируйте config.py:

python
BOT_TOKEN = "your_bot_token_here"
ADMIN_IDS = [123456789]  # Ваш ID в Telegram
ALLOWED_USER_IDS = []  # Пустой список = все пользователи
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
Запустите бота:

bash
python bot.py
Использование
Основные команды
/start - Начать работу с ботом

/help - Показать справку по командам

/upload - Загрузить файл

/files - Показать список файлов

/download <filename> - Скачать файл

/search <query> - Поиск файлов

# Загрузка файлов
Отправьте боту любой файл или используйте команду /upload и следуйте инструкциям.

Структура проекта
telegram-file-bot/
├── main.py              # Основной файл бота
├── requirements.txt    # Зависимости Python
├── files_data.json/           # База данных с id файлов
├── database/          # База данных пользователей
└── README.md          # Этот файл
Настройка через environment variables
Вы также можете настроить бота через переменные окружения:

# Развертывание
Локальный запуск
bash
python bot.py
Запуск в фоновом режиме (Linux)
bash
nohup python bot.py > bot.log 2>&1 &
Docker (опционально)
bash
docker build -t telegram-file-bot .
docker run -d --name file-bot telegram-file-bot
Безопасность
⚠️ Не публикуйте ваш BOT_TOKEN в открытом доступе

🔒 Настройте ADMIN_IDS для ограничения доступа

📏 Ограничьте MAX_FILE_SIZE для предотвращения перегрузки

💾 Регулярно делайте бэкапы директории storage/

Вклад в проект
Форкните репозиторий

Создайте ветку для фичи (git checkout -b feature/amazing-feature)

Закоммитьте изменения (git commit -m 'Add amazing feature')

Запушьте в ветку (git push origin feature/amazing-feature)

Откройте Pull Request

Лицензия
Этот проект распространяется под лицензией MIT. См. файл LICENSE для подробностей.

Поддержка
Если у вас возникли вопросы или проблемы:

Проверьте Issues

Создайте новое Issue с описанием проблемы

Укажите версию бота и шаги для воспроизведения ошибки

Благодарности
python-telegram-bot - Отличная библиотека для создания Telegram ботов

Telegram API - За прекрасную платформу для ботов

⭐ Если вам понравился этот проект, поставьте звезду на GitHub!
