import config
import db
from text import already_reg_list, now_reg_list, finding_loser_list, finding_nice_list
from random import choice
from datetime import datetime
from time import sleep
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()
router.message.filter(F.chat.func(lambda chat: chat.id == int(config.CHAT_ID)))


@router.message(Command("my"))
async def message_handler(msg: Message):
    res = (db.db_request("SELECT * FROM users WHERE id='{}'".format(int(msg.from_user.id))))
    str = "{}, за все время вы были удостоены:\n📝 {} лузеров дня\n🎀 {} красавчиков дня".format(res[0][1], res[0][2],
                                                                                               res[0][3])
    await msg.reply(str)


@router.message(Command("stat"))
async def message_handler(msg: Message):
    month = datetime.today().month
    users = (db.db_request("SELECT id, name FROM users"))

    loser_logs = (db.db_request("SELECT loser FROM logs WHERE EXTRACT (month FROM \"date\") = {}".format(month)))
    loser_dic = {}
    loser_logs = [elem[0] for elem in loser_logs]

    nice_logs = (db.db_request("SELECT nice FROM logs WHERE EXTRACT (month FROM \"date\") = {}".format(month)))
    nice_dic = {}
    nice_logs = [elem[0] for elem in nice_logs]

    for id in users:
        loser_dic[id[0]] = loser_logs.count(id[0])
        nice_dic[id[0]] = nice_logs.count(id[0])

    loser_list = sorted(loser_dic.items(), key=lambda x: x[1])
    sort_loser = dict(loser_list)
    nice_list = sorted(nice_dic.items(), key=lambda x: x[1])
    sort_nice = dict(nice_list)

    str = "Результаты 🌈ЛУЗЕР Дня\n\n"
    num = 0
    for elem in reversed(sort_loser):
        num = num + 1
        id = elem
        score = sort_loser[elem]
        name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(id)))[0][0]
        str = str + f"{num}) <a href='tg://user?id={id}'>{name}</a> - {score} раз(а)\n"

    await msg.answer(str, "HTML")

    str = "🎉 Результаты Красавчик Дня\n\n"
    num = 0
    for elem in reversed(sort_nice):
        num = num + 1
        id = elem
        score = sort_nice[elem]
        name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(id)))[0][0]
        str = str + f"{num}) <a href='tg://user?id={id}'>{name}</a> - {score} раз(а)\n"

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
    loser_id = choice(id_list)[0]
    result = (db.db_request(
        "INSERT INTO logs VALUES ('{}', '{}', '{}') ON CONFLICT DO NOTHING RETURNING *".format(date, loser_id, nice_id)))

    if result == []:
        nice_id = (db.db_request("SELECT nice FROM logs WHERE date='{}'".format(date)))[0][0]
        loser_id = (db.db_request("SELECT loser FROM logs WHERE date='{}'".format(date)))[0][0]
        nice_name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(nice_id)))[0][0]
        loser_name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(loser_id)))[0][0]
        await bot.send_message(chat_id, "Герои дня уже были выбраны!")
        sleep(1)
        await bot.send_message(chat_id, "Главный лузер:")
        sleep(1)
        await bot.send_message(chat_id, f"<a href='tg://user?id={loser_id}'>{loser_name}</a>", parse_mode="HTML")
        sleep(1)
        await bot.send_message(chat_id, "Сегодняшний красивый красавчик:")
        sleep(1)
        await bot.send_message(chat_id, f"<a href='tg://user?id={nice_id}'>{nice_name}</a>", parse_mode="HTML")
    else:
        nice_name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(nice_id)))[0][0]
        loser_name = (db.db_request("SELECT name FROM users WHERE id='{}'".format(loser_id)))[0][0]
        db.db_request("UPDATE users SET losers = losers + 1 WHERE id='{}' RETURNING *".format(loser_id))
        db.db_request("UPDATE users SET nices = nices + 1 WHERE id='{}' RETURNING *".format(nice_id))
        await bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEM1fZm7WpMpXi8l0GfxlC8H73167uDbgACw0MAAuM34Uhcw6sgtc9enzYE')
        await bot.send_message(chat_id, "🌈 НАЧНЕМ ПОИСКИ С ЛУЗЕРА ДНЯ 🌈")
        sleep(3)
        await bot.send_message(chat_id, choice(finding_loser_list))
        sleep(3)
        await bot.send_message(chat_id, choice(finding_loser_list))
        sleep(3)
        await bot.send_message(chat_id, choice(finding_loser_list))
        sleep(3)
        await bot.send_message(chat_id, "⚠️ ВНИМАНИЕ, ЛУЗЕР ДНЯ ⚠️")
        sleep(1)
        await bot.send_message(chat_id, f"<a href='tg://user?id={loser_id}'>{loser_name}</a>", parse_mode="HTML")
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


@router.message(F.text.lower() == 'увы')
async def message_handler(msg: Message):
    await msg.answer_sticker('CAACAgIAAxkBAAEMqwVmwdb4EjjRMe1d9XbHRcZwMmdWtAACqyIAAhfmkEhTcU-1XtA3hTUE')
    
