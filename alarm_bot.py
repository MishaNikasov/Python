import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from model.AlarmModel import AlarmModel
from service import alarm_service

bot = Bot('5211159874:AAFp5BEJc8pQNW9ZrzXDYJzQi53vinjrXfY')
dispatcher = Dispatcher(bot)

admin_id = 278725762
is_running = False

chat_list = dict({})


@dispatcher.message_handler(commands=['init'])
async def init(message: types.Message):
    global is_running
    if message.chat.id == admin_id and is_running is False:
        is_running = True
        await message.reply('Бот запущен')
        await __monitoring()
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
    if message.chat.id not in chat_list:
        print(str(message.chat.full_name) + ' https://t.me/' + str(message.chat.username) + ' connected')
        chat_list[message.chat.id] = message
        await message.answer('Запуск мониторинга')
    else:
        await bot.send_photo(message.chat.id, 'https://prnt.sc/740HpA9Fbsdw', reply_to_message_id=message.message_id)


async def __remove_from_monitoring(message: types.Message):
    if message.chat.id in chat_list:
        chat_list.pop(message.chat.id)
        print(str(message.chat.full_name) + ' https://t.me/' + str(message.chat.username) + ' removed from monitoring')
        await message.answer('Остановка мониторинга')
    else:
        await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEEN3JiNxonIyJEZCfFrjfvFFld63kFZgACPhUAAuE7yEshrvTovPQkDyME', reply_to_message_id=message.message_id)


async def __handle_alarm(alarm: AlarmModel, message: types.Message):
    if alarm.status:
        print('Отбой тревоги: ' + alarm.update_time + ' = ' + message.chat.full_name)
        await message.answer('🟢 Отбой тревоги: ' + alarm.update_time + is_bandertown(message.chat.full_name))
    else:
        print('Тревога: ' + alarm.update_time + ' = ' + message.chat.full_name)
        await message.answer('🔴 Тревога: ' + alarm.update_time + is_bandertown(message.chat.full_name))


def handle_state(state: AlarmModel):
    if state.status:
        return "По кайфу"
    else:
        return "Ты еще не в коридоре?"


def is_bandertown(group_name: str):
    if group_name == 'Східний Бандертаун':
        return '\n@SolnechnyjKudesnik\n@TheSkywallker\n@jar_1k\n@KiraBaril\n@DelphinGoth\n@Tymurrrr\n@Studa'
    else:
        return ''


async def __monitoring():
    alarm_state = True
    while True:
        await asyncio.sleep(20)
        current_alarm = alarm_service.get_alarm()
        if alarm_state != current_alarm.status:
            print('Обновление информации о состоянии: ' + current_alarm.update_time)
            alarm_state = current_alarm.status
            for key in chat_list:
                await __handle_alarm(current_alarm, chat_list[key])


executor.start_polling(dispatcher, skip_updates=True)
