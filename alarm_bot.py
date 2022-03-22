import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from data import data_store
from model.AlarmModel import AlarmModel
from service import alarm_service

bot = Bot('5211159874:AAFp5BEJc8pQNW9ZrzXDYJzQi53vinjrXfY')
dispatcher = Dispatcher(bot)

admin_id = 278725762
is_running = False


@dispatcher.message_handler(commands=['init'])
async def init(message: types.Message):
    global is_running
    if message.chat.id == admin_id and is_running is False:
        await message.reply('Бот запущен')
        await __run()
    elif message.chat.id == admin_id and is_running is True:
        await message.reply('Бот уже мониторит')


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await __add_to_monitoring(message)


@dispatcher.message_handler(commands=['stop'])
async def stop(message: types.Message):
    await __remove_from_monitoring(message)


@dispatcher.message_handler(commands=['state'])
async def state(message: types.Message):
    alarm_state = handle_state(alarm_service.get_alarm())
    await message.reply(alarm_state)


async def __add_to_monitoring(message: types.Message):
    if data_store.save_chat(message.chat.id):
        print(f'{str(message.chat.full_name)} https://t.me/{str(message.chat.username)} connected')
        await bot.send_message(message.chat.id, 'Запуск мониторинга')
    else:
        await bot.send_photo(message.chat.id, 'https://prnt.sc/740HpA9Fbsdw', reply_to_message_id=message.message_id)


async def __remove_from_monitoring(message: types.Message):
    if data_store.remove_chat(message.chat.id):
        print(f'{str(message.chat.full_name)} https://t.me/{str(message.chat.username)} removed from monitoring')
        await bot.send_message(message.chat.id, 'Остановка мониторинга')
    else:
        await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEEN3JiNxonIyJEZCfFrjfvFFld63kFZgACPhUAAuE7yEshrvTovPQkDyME', reply_to_message_id=message.message_id)


async def __handle_alarm(alarm: AlarmModel, chat_id: int):
    if alarm.status:
        print(f'Отбой тревоги: {alarm.update_time}, id = {chat_id}')
        await bot.send_message(chat_id, f'🟢 Отбой тревоги: {alarm.update_time}{is_bandertown(chat_id)}')
    else:
        print(f'Тревога: {alarm.update_time}, id = {chat_id}')
        await bot.send_message(chat_id, f'🔴 Тревога: {alarm.update_time}{is_bandertown(chat_id)}')


def handle_state(alarm_state: AlarmModel):
    if alarm_state.status:
        return "По кайфу"
    else:
        return "Ты еще не в коридоре?"


def is_bandertown(group_name: int):
    if group_name == -1001197833902:
        return '\n@SolnechnyjKudesnik\n@TheSkywallker\n@jar_1k\n@KiraBaril\n@DelphinGoth\n@Tymurrrr\n@Studa'
    else:
        return ''


async def __run():
    print('Скрипт запущен')
    global is_running
    is_running = True
    alarm_state = True
    while True:
        await asyncio.sleep(20)
        current_alarm = alarm_service.get_alarm()
        if alarm_state != current_alarm.status:
            chat_list = data_store.get_chat_list()
            print('Обновление информации о состоянии: ' + current_alarm.update_time)
            alarm_state = current_alarm.status
            for chat_id in chat_list:
                await __handle_alarm(current_alarm, chat_id)


executor.start_polling(dispatcher, skip_updates=True)
