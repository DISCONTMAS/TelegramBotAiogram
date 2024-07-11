import asyncio
import html
import logging

from aiogram import Bot, Dispatcher, types

from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ParseMode

from datetime import datetime

from aiogram.utils.formatting import Bold, Text, as_list, as_marked_section, as_key_value, HashTag

from config_reader import config

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(),
          default=DefaultBotProperties(
              parse_mode=ParseMode.HTML
          ))
# Диспетчер
dp = Dispatcher()
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    content = Text("Hello, ", Bold(message.from_user.full_name))
    await message.answer(**content.as_kwargs())


@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await message.reply("test1")


async def cmd_test2(message: types.Message):
    await message.reply("test2")


@dp.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice()


@dp.message(Command("add_to_list"))
async def cmd_add_to_list(message: types.Message, my_list: list[int]):
    my_list.append(7)
    await message.answer("Добавлено число 7")


@dp.message(Command("show_list"))
async def cmd_show_list(message: types.Message, my_list: list[int]):
    await message.answer(f"Список имеет следующие значения: {my_list}")


@dp.message(Command("start_datetime"))
async def cmd_start_datetime(message: types.Message, started_at: str):
    await message.answer(f"Момент начала работы бота: {started_at}")


@dp.message(F.text, Command("first_day"))
async def any_message(message: Message):
    await message.answer("Hello, <b>world</b>!")


@dp.message(Command("advanced_example"))
async def cmd_advanced_example(message: Message):
    content = as_list(
        as_marked_section(
            Bold("Success:"),
            "Test 1",
            "Test 3",
            "Test 4",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Failed:"),
            "Test 2",
            marker="❌ ",
        ),
        as_marked_section(
            Bold("Summary:"),
            as_key_value("Total", 4),
            as_key_value("Success", 3),
            as_key_value("Failed", 1),
            marker="  ",
        ),
        HashTag("#test"),
        sep="\n\n",
    )
    await message.answer(**content.as_kwargs())


# @dp.message(F.text)
# async def echo_wish_time(message: Message):
#     moment = datetime.now().strftime("%H:%M")
#     added_text = html.underline(f"Отправлено в {moment}")
#     await message.answer(f"{message.text} \n\n {added_text}")


# @dp.message(F.text)
# async def echo_with_time(message: Message):
#     # Получаем текущее время в часовом поясе ПК
#     time_now = datetime.now().strftime('%H:%M')
#     # Создаём подчёркнутый текст
#     added_text = f"Создано в {time_now}"
#     # Отправляем новое сообщение с добавленным текстом
#     await message.answer(f"{message.html_text}\n\n<u>{added_text}</u>", parse_mode="HTML")


@dp.message(Command("settimer"))
async def cmd_set_timer(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка! аргументы не переданы.")
        return
    try:
        delay_time, text_to_send = command.args.split(" ", maxsplit=1)
    except ValueError:
        await message.answer("Ошибка! Недопустимое количество аргументов.\n "
                             "Пример команды: '/settimer <time> <comment>'.")
        return
    await message.answer(
        "Таймер добавлен.\n"
        f"Время: {delay_time}.\n"
        f"Описание: {text_to_send}."
    )


@dp.message(F.text)
async def extract_data(message: Message):
    data = {
        "url": "",
        "email": "",
        "code": ""
    }
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = item.extract_from(message.text)
    await message.reply(
        "Вот, что я нашла: \n"
        f"Url: {data['url']}\n"
        f"Email: {data['email']}\n"
        f"Code: {data['code']}\n"
    )


# Запуск процесса поллинга новых апдейтов
async def main():
    dp.message.register(cmd_test2, Command("test2"))
    await dp.start_polling(bot, my_list = [1, 2, 3])

if __name__ == "__main__":
    asyncio.run(main())