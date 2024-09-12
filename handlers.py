import random
from aiogram import F, Router
import db
from random import choice
import config
from datetime import datetime
from aiogram.types import Message
from aiogram.filters import Command
from time import sleep
from text import already_reg_list, now_reg_list, finding_pidr_list, finding_nice_list

router = Router()
router.message.filter(F.chat.func(lambda chat: chat.id == int(config.CHAT_ID)))


@router.message(Command("my"))
async def message_handler(msg: Message):
    res = (db.db_request("SELECT * FROM users WHERE id='{}'".format(int(msg.from_user.id))))
    str = "{}, за все время вы были удостоены:\n📝 {} пидоров дня\n🎀 {} красавчиков дня".format(res[0][1], res[0][2],
                                                                                               res[0][3])
    await msg.reply(str)


@router.message(Command("stat"))
async def message_handler(msg: Message):
    month = datetime.today().month
    users = (db.db_request("SELECT id, name FROM users"))

    pidr_logs = (db.db_request(("SELECT pidr FROM logs WHERE EXTRACT (month FROM \"date\") = {}").format(month)))
    pidr_dic = {}
    pidr_logs = [elem[0] for elem in pidr_logs]

    nice_logs = (db.db_request(("SELECT nice FROM logs WHERE EXTRACT (month FROM \"date\") = {}").format(month)))
    nice_dic = {}
    nice_logs = [elem[0] for elem in nice_logs]

    for id in users:
        pidr_dic[id[0]] = pidr_logs.count(id[0])
        nice_dic[id[0]] = nice_logs.count(id[0])

    pidr_list = sorted(pidr_dic.items(), key=lambda x: x[1])
    sort_pidr = dict(pidr_list)
    nice_list = sorted(nice_dic.items(), key=lambda x: x[1])
    sort_nice = dict(nice_list)

    str = "Результаты 🌈ПИДОР Дня\n\n"
    num = 0
    for elem in reversed(sort_pidr):
        num = num + 1
        id = elem
        score = sort_pidr[elem]
        name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(id)))[0][0]
        str = str + (f"{num}) <a href='tg://user?id={id}'>{name}</a> - {score} раз(а)\n")

    await msg.answer(str, "HTML")

    str = "🎉 Результаты Красавчик Дня\n\n"
    num = 0
    for elem in reversed(sort_nice):
        num = num + 1
        id = elem
        score = sort_nice[elem]
        name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(id)))[0][0]
        str = str + (f"{num}) <a href='tg://user?id={id}'>{name}</a> - {score} раз(а)\n")

    await msg.answer(str, "HTML")


@router.message(Command("reg"))
async def message_handler(msg: Message):
    if ((db.db_request(
            "INSERT INTO users VALUES ('{}', '{}') ON CONFLICT DO NOTHING RETURNING *".format(msg.from_user.id,
                                                                                              msg.from_user.first_name))) == []):
        await msg.reply(choice(already_reg_list))
    else:
        await msg.reply(choice(now_reg_list))


async def run(bot, chat_id):
    date = datetime.today().strftime("%Y%m%d")
    id_list = (db.db_request("SELECT id FROM users"))
    nice_id = choice(id_list)[0]
    pidr_id = choice(id_list)[0]
    result = (db.db_request(
        "INSERT INTO logs VALUES ('{}', '{}', '{}') ON CONFLICT DO NOTHING RETURNING *".format(date, pidr_id, nice_id)))

    if result == []:
        nice_id = (db.db_request("SELECT nice FROM logs WHERE date='{}'".format(date)))[0][0]
        pidr_id = (db.db_request("SELECT pidr FROM logs WHERE date='{}'".format(date)))[0][0]
        nice_name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(nice_id)))[0][0]
        pidr_name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(pidr_id)))[0][0]
        await bot.send_message(chat_id, "Я уже все сделал, не мороси")
        sleep(2)
        await bot.send_message(chat_id, "Гейский гей уже был выбран сегодня, вот он:")
        sleep(1)
        await bot.send_message(chat_id, f"<a href='tg://user?id={pidr_id}'>{pidr_name}</a>", parse_mode="HTML")
        sleep(2)
        await bot.send_message(chat_id, "Красивый красавчик дня тоже тут:")
        sleep(1)
        await bot.send_message(chat_id, f"<a href='tg://user?id={nice_id}'>{nice_name}</a>", parse_mode="HTML")
    else:
        nice_name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(nice_id)))[0][0]
        pidr_name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(pidr_id)))[0][0]
        db.db_request("UPDATE users SET pidrs = pidrs + 1 WHERE id='{}' RETURNING *".format(pidr_id))
        db.db_request("UPDATE users SET nices = nices + 1 WHERE id='{}' RETURNING *".format(nice_id))
        await bot.send_message(chat_id, '🎰')
        await bot.send_message(chat_id, "🌈 НАЧНЕМ ПОИСКИ С ПИДОРА ДНЯ 🌈")
        sleep(3)
        await bot.send_message(chat_id, choice(finding_pidr_list))
        sleep(3)
        await bot.send_message(chat_id, choice(finding_pidr_list))
        sleep(3)
        await bot.send_message(chat_id, choice(finding_pidr_list))
        sleep(3)
        await bot.send_message(chat_id, "⚠️ ВНИМАНИЕ, ПИДОР ДНЯ ⚠️")
        sleep(1)
        await bot.send_message(chat_id, f"<a href='tg://user?id={pidr_id}'>{pidr_name}</a>", parse_mode="HTML")
        sleep(5)
        await bot.send_message(chat_id, "🥰 А ТЕПЕРЬ К ПРИЯТНОМУ 🥰")
        sleep(3)
        await bot.send_message(chat_id, choice(finding_nice_list))
        sleep(3)
        await bot.send_message(chat_id, choice(finding_nice_list))
        sleep(3)
        await bot.send_message(chat_id, choice(finding_nice_list))
        sleep(3)
        await bot.send_message(chat_id, "😻 КРАСОТКА ДНЯ В ЧАТЕ 😻")
        sleep(1)
        await bot.send_message(chat_id, f"<a href='tg://user?id={nice_id}'>{nice_name}</a>", parse_mode="HTML")
        sleep(2)
        await bot.send_message(chat_id, "всем спасибо все свободны")


@router.message(Command("run"))
async def message_handler(msg: Message):
    await run(msg.bot, msg.chat.id)


@router.message(Command("hate"))
async def message_handler(msg: Message):
    ser_id = "742474560"
    ser_name = "Sergei"
    leh_id = "837475241"
    leh_name = "Алексей"
    names = (ser_name, leh_name)
    ids = (ser_id, leh_id)
    num = random.randint(0, 1)
    await msg.answer(f"Звание Биг Ган Дон получает: <a href='tg://user?id={ids[num]}'>{names[num]}</a>", "HTML")


@router.message(F.text == 'увы')
async def message_handler(msg: Message):
    await msg.answer_sticker('CAACAgIAAxkBAAEMqwVmwdb4EjjRMe1d9XbHRcZwMmdWtAACqyIAAhfmkEhTcU-1XtA3hTUE')
