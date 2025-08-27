# 19.07.2025 пока что слишком для меня тяжело
# 26.07.2025 я это запилил!
# 28.07.2025 допилил до конфэтки

import asyncio
import logging
import json
import random
import string
import os

from collections import defaultdict
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

API_TOKEN = "TOKEN"
FILES_DATA = "files_data.json" # бд с id файлов
USERS_DATA = "users_data.json" # бд с юзерами
ADMINS = ["useridhere1", "useridhere2"] # юзер айдишники админов
# админ команды: /admin и /filedel для всех файлов даже если админ не овнер файла

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Настройки антифлуда
FLOOD_LIMIT = 2  # Максимальное количество сообщений
TIME_LIMIT = 5  # В секундах, за которое нельзя превышать лимит
BAN_TIME = 30  # В секундах, на сколько банить флудера

user_messages = defaultdict(list)
banned_users = {}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

async def check_flood(message):
    user_id = message.from_user.id

    if user_id in banned_users:
        if datetime.now() < banned_users[user_id]:
            return True
        else:
            message.reply("КД на сообщения прошло!")
            del banned_users[user_id]

    user_messages[user_id].append(datetime.now())

    user_messages[user_id] = [
        msg_time for msg_time in user_messages[user_id]
        if datetime.now() - msg_time < timedelta(seconds=TIME_LIMIT)
    ]

    if len(user_messages[user_id]) > FLOOD_LIMIT:
        banned_users[user_id] = datetime.now() + timedelta(seconds=BAN_TIME)
        logger.warning(f"User {user_id} (@{message.from_user.username}) banned for flooding for {BAN_TIME} seconds")
        message.reply("Не флудите!")
        return True

    return False

@dp.message(Command("start"))
async def send_start(message: Message):
    if await check_flood(message):
        return

    logger.info(f"User send /start command | User: {message.from_user.id} | Username: @{message.from_user.username} | Chat: {message.chat.id} ({message.chat.type})")

    with open(USERS_DATA, "r") as rf:
        users = json.load(rf)
    try:
        users[str(message.from_user.id)] = {"UserName": message.from_user.username, "ChatID": message.chat.id, "Uploads": users[str(message.from_user.id)]["Uploads"], "Downloads": users[str(message.from_user.id)]["Downloads"]}
    except KeyError:
        users[str(message.from_user.id)] = {}
        users[str(message.from_user.id)]["UserName"] = message.from_user.username
        users[str(message.from_user.id)]["ChatID"] = message.chat.id
        users[str(message.from_user.id)]["Uploads"] = 0
        users[str(message.from_user.id)]["Downloads"] = 0
    with open(USERS_DATA, "w") as wf:
        json.dump(users, wf)

    await message.reply(f"""
Здравствуйте, {message.from_user.full_name},
Вас приветствует файловый бот!
Просто отправьте мне любой файл и вы получите для него код!
(ВАЖНО: Отправляйте по одному файлу или архивируйте их!)
Вы можете отправить файлы следующих типов:
    `Фото`
    `Видео`
    `Кружочки`
    `Войс`
    `Аудио`
    `Стикер`
    `Документы`
    `Архивы`
    `И прочее`
Чтобы получить файл, введите команду
`/file [код]`
Чтобы удалить файл (может только загрузчик файла или админ), введите команду
`/filedel [код]`
Чтобы посмотреть вашу статистику, введите команду
`/stats`
__Дискорд создателя-начинающего кодера:__
__usuk228__""", parse_mode="Markdown") # заменишь автора = пидорас

@dp.message(Command("stats"))
async def send_stats(message: Message):
    if await check_flood(message):
        return

    logger.info(f"User send /stats command | User: {message.from_user.id} | Username: @{message.from_user.username} | Chat: {message.chat.id} ({message.chat.type})")

    with open(FILES_DATA, "r") as ff:
        files = json.load(ff)
    with open(USERS_DATA, "r") as uf:
        users = json.load(uf)

    allfiles = []

    for file in files:
        if files[file]["UserID"] == message.from_user.id:
            allfiles.append(file)

    await message.reply(f"""
Ваша статистика:
    Кол-во загруженных файлов в бота:
    `{users[str(message.from_user.id)]["Uploads"]}`
    Кол-во просмотров загруженных вами файлов:
    `{users[str(message.from_user.id)]["Downloads"]}`
    ID всех загруженных файлов:
    `{"`, `".join(str(fileuniq2) for fileuniq2 in allfiles) if allfiles != [] else "Ни одной загрузки"}`""", parse_mode="Markdown")

@dp.message(Command("file"))
async def send_file(message: Message):
    if await check_flood(message):
        return
    try:
        fileuniq = message.text.split(maxsplit=1)[1]
        logger.info(f"User send /file {fileuniq} command | User: {message.from_user.id} | Username: @{message.from_user.username} | Chat: {message.chat.id} ({message.chat.type})")
        with open(FILES_DATA, "r") as f:
            filedata = json.load(f)
        if "video" in filedata[fileuniq]["FileType"]:
            await message.reply_video(filedata[fileuniq]["FileID"], caption=f"Отправитель: {filedata[fileuniq]["UserNick"]} (@{filedata[fileuniq]["UserName"]})")
        elif "image" in filedata[fileuniq]["FileType"]:
            await message.reply_photo(filedata[fileuniq]["FileID"], caption=f"Отправитель: {filedata[fileuniq]["UserNick"]} (@{filedata[fileuniq]["UserName"]})")
        elif "audio" in filedata[fileuniq]["FileType"]:
            if "voice" in filedata[fileuniq]["FileType"]:
                await message.reply_voice(filedata[fileuniq]["FileID"], caption=f"Отправитель: {filedata[fileuniq]["UserNick"]} (@{filedata[fileuniq]["UserName"]})")
            else:
                await message.reply_audio(filedata[fileuniq]["FileID"], caption=f"Отправитель: {filedata[fileuniq]["UserNick"]} (@{filedata[fileuniq]["UserName"]})")
        elif "sticker" in filedata[fileuniq]["FileType"]:
            await message.reply_sticker(filedata[fileuniq]["FileID"], caption=f"Отправитель: {filedata[fileuniq]["UserNick"]} (@{filedata[fileuniq]["UserName"]})")
        elif "video_note" in filedata[fileuniq]["FileType"]:
            await message.reply_video_note(filedata[fileuniq]["FileID"], caption=f"Отправитель: {filedata[fileuniq]["UserNick"]} (@{filedata[fileuniq]["UserName"]})")
        else:
            await message.reply_document(filedata[fileuniq]["FileID"], caption=f"Отправитель: {filedata[fileuniq]["UserNick"]} (@{filedata[fileuniq]["UserName"]})")
        with open(USERS_DATA, "r") as rf:
            users = json.load(rf)
        users[str(filedata[fileuniq]["UserID"])]["Downloads"] += 1
        with open(USERS_DATA, "w") as wf:
            json.dump(users, wf)
    except IndexError:
        await message.reply("Ошибка: Укажите какой либо ID")
    except KeyError:
        await message.reply("Ошибка: ID не найден или указан не верно")
    except Exception as err:
        await message.reply(f"Ошибка: {err}")

@dp.message(Command("filedel"))
async def send_filedel(message: Message):
    if await check_flood(message):
        return
    try:
        fileuniq = message.text.split(maxsplit=1)[1]
        logger.info(f"User send /filedel {fileuniq} command | User: {message.from_user.id} | Username: @{message.from_user.username} | Chat: {message.chat.id} ({message.chat.type})")
        with open(FILES_DATA, "r") as rf:
            filedata = json.load(rf)
        if filedata[fileuniq]["UserID"] == message.from_user.id or filedata[fileuniq]["UserID"] in ADMINS:
            await message.reply(f"Файл с ID `{fileuniq}` был удален!", parse_mode="Markdown")
            del filedata[fileuniq]
            with open(FILES_DATA, "w") as wf:
                json.dump(filedata, wf)
        else:
            await message.reply("Ошибка: Вы не владелец или не админ!")
    except IndexError:
        await message.reply("Ошибка: Укажите какой либо ID")
    except KeyError:
        await message.reply("Ошибка: ID не найден или указан не верно")
    except Exception as err:
        await message.reply(f"Ошибка: {err}")

@dp.message(F.photo)
async def photo_check(message: Message):
    if await check_flood(message):
        return

    with open(FILES_DATA, "r") as f:
        data = json.load(f)
    crypting = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(3)) + message.photo[-1].file_unique_id
    fileuniq = "".join(random.sample(crypting, len(crypting)))

    logger.info(f"Photo info: {message.photo[-1].file_id} | Uniq: {fileuniq} |User: {message.from_user.id} | Username: @{message.from_user.username}")

    data[fileuniq] = {"FileID": message.photo[-1].file_id, "FileType": "image/photo",
                      "UserNick": message.from_user.full_name, "UserName": message.from_user.username,
                      "UserID": message.from_user.id}
    with open(FILES_DATA, "w") as f:
        json.dump(data, f)

    with open(USERS_DATA, "r") as rf:
        users = json.load(rf)
    users[str(data[fileuniq]["UserID"])]["Uploads"] += 1
    with open(USERS_DATA, "w") as wf:
        json.dump(users, wf)

    await message.reply(f"""
Изображение было обработано!
ID: `{fileuniq}`
Команда для получения:
`/file {fileuniq}`
Команда для удаления:
`/filedel {fileuniq}`""", parse_mode="Markdown")

@dp.message(F.sticker)
async def sticker_check(message: Message):
    if await check_flood(message):
        return

    print(message.sticker)

    with open(FILES_DATA, "r") as f:
        data = json.load(f)
    crypting = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(3)) + message.sticker.file_unique_id
    fileuniq = "".join(random.sample(crypting, len(crypting)))

    logger.info(f"Sticker info: {message.sticker.file_id} | Uniq: {fileuniq} | User: {message.from_user.id} | Username: @{message.from_user.username}")

    data[fileuniq] = {"FileID": message.sticker.file_id, "FileType": "sticker",
                      "UserNick": message.from_user.full_name, "UserName": message.from_user.username,
                      "UserID": message.from_user.id}
    with open(FILES_DATA, "w") as f:
        json.dump(data, f)

    with open(USERS_DATA, "r") as rf:
        users = json.load(rf)
    users[str(data[fileuniq]["UserID"])]["Uploads"] += 1
    with open(USERS_DATA, "w") as wf:
        json.dump(users, wf)

    await message.reply(f"""
Стикер был обработан!
ID: `{fileuniq}`
Команда для получения:
`/file {fileuniq}`
Команда для удаления:
`/filedel {fileuniq}`""", parse_mode="Markdown")

@dp.message(F.video_note)
async def video_note_check(message: Message):
    if await check_flood(message):
        return

    print(message.video_note)

    with open(FILES_DATA, "r") as f:
        data = json.load(f)
    crypting = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(3)) + message.video_note.file_unique_id
    fileuniq = "".join(random.sample(crypting, len(crypting)))

    logger.info(f"Video note info: {message.video_note.file_id} | Uniq: {fileuniq} | User: {message.from_user.id} | Username: @{message.from_user.username}")

    data[fileuniq] = {"FileID": message.video_note.file_id, "FileType": "video_note",
                      "UserNick": message.from_user.full_name, "UserName": message.from_user.username,
                      "UserID": message.from_user.id}
    with open(FILES_DATA, "w") as f:
        json.dump(data, f)

    with open(USERS_DATA, "r") as rf:
        users = json.load(rf)
    users[str(data[fileuniq]["UserID"])]["Uploads"] += 1
    with open(USERS_DATA, "w") as wf:
        json.dump(users, wf)

    await message.reply(f"""
Кружочек был обработан!
ID: `{fileuniq}`
Команда для получения:
`/file {fileuniq}`
Команда для удаления:
`/filedel {fileuniq}`""", parse_mode="Markdown")

@dp.message(F.voice)
async def voice_check(message: Message):
    if await check_flood(message):
        return

    with open(FILES_DATA, "r") as f:
        data = json.load(f)
    crypting = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(3)) + message.voice.file_unique_id
    fileuniq = "".join(random.sample(crypting, len(crypting)))

    logger.info(f"Voice info: {message.voice.file_id} | Uniq: {fileuniq} | User: {message.from_user.id} | Username: @{message.from_user.username}")

    data[fileuniq] = {"FileID": message.voice.file_id, "FileType": f"{message.voice.mime_type}/voice",
                      "UserNick": message.from_user.full_name, "UserName": message.from_user.username,
                      "UserID": message.from_user.id}
    with open(FILES_DATA, "w") as f:
        json.dump(data, f)

    with open(USERS_DATA, "r") as rf:
        users = json.load(rf)
    users[str(data[fileuniq]["UserID"])]["Uploads"] += 1
    with open(USERS_DATA, "w") as wf:
        json.dump(users, wf)

    await message.reply(f"""
Голосовуха была обработана!
ID: `{fileuniq}`
Команда для получения:
`/file {fileuniq}`
Команда для удаления:
`/filedel {fileuniq}`""", parse_mode="Markdown")

@dp.message(F.video)
async def video_check(message: Message):
    if await check_flood(message):
        return

    with open(FILES_DATA, "r") as f:
        data = json.load(f)
    crypting = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(3)) + message.video.file_unique_id
    fileuniq = "".join(random.sample(crypting, len(crypting)))

    logger.info(f"Video info: {message.video.file_name}, {message.video.mime_type} | Uniq: {fileuniq} | User: {message.from_user.id} | Username: @{message.from_user.username}")

    data[fileuniq] = {"FileID": message.video.file_id, "FileType": message.video.mime_type,
                      "UserNick": message.from_user.full_name, "UserName": message.from_user.username,
                      "UserID": message.from_user.id}
    with open(FILES_DATA, "w") as f:
        json.dump(data, f)

    with open(USERS_DATA, "r") as rf:
        users = json.load(rf)
    users[str(data[fileuniq]["UserID"])]["Uploads"] += 1
    with open(USERS_DATA, "w") as wf:
        json.dump(users, wf)

    await message.reply(f"""
Видео было обработано!
ID: `{fileuniq}`
Команда для получения:
`/file {fileuniq}`
Команда для удаления:
`/filedel {fileuniq}`""", parse_mode="Markdown")

@dp.message(F.document)
async def document_check(message: Message):
    if await check_flood(message):
        return

    with open(FILES_DATA, "r") as f:
        data = json.load(f)
    crypting = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(3)) + message.document.file_unique_id
    fileuniq = "".join(random.sample(crypting, len(crypting)))

    logger.info(f"Document info: {message.document.file_name}, {message.document.mime_type} | Uniq: {fileuniq} | User: {message.from_user.id} | Username: @{message.from_user.username}")

    data[fileuniq] = {"FileID": message.document.file_id, "FileType": message.document.mime_type,
                      "UserNick": message.from_user.full_name, "UserName": message.from_user.username,
                      "UserID": message.from_user.id}
    with open(FILES_DATA, "w") as f:
        json.dump(data, f)

    with open(USERS_DATA, "r") as rf:
        users = json.load(rf)
    users[str(data[fileuniq]["UserID"])]["Uploads"] += 1
    with open(USERS_DATA, "w") as wf:
        json.dump(users, wf)

    await message.reply(f"""
Файл был обработан!
ID: `{fileuniq}`
Команда для получения:
`/file {fileuniq}`
Команда для удаления:
`/filedel {fileuniq}`""", parse_mode="Markdown")

async def main():
    if not os.path.exists(FILES_DATA):
        open(FILES_DATA, "w").write("{}")
    if not os.path.exists(USERS_DATA):
        open(USERS_DATA, "w").write("{}")
    logger.info("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())