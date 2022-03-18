import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from model.AlarmModel import AlarmModel
from service import alarm_service

bot = Bot('5211159874:AAFp5BEJc8pQNW9ZrzXDYJzQi53vinjrXfY')
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    print(str(message.chat.full_name) + ' https://t.me/' + str(message.chat.username) + ' connected')
    await message.answer('Запуск мониторинга')
    await __monitoring(message)


@dispatcher.message_handler(commands=['state'])
async def get_state(message: types.Message):
    state = alarm_service.get_alarm()
    await message.answer(state)


async def __monitoring(message: types.Message):
    alarm_state = True
    while True:
        await asyncio.sleep(20)
        current_alarm = alarm_service.get_alarm()
        if alarm_state != current_alarm.status:
            print('Обновление информации о состоянии: ' + current_alarm.update_time)
            alarm_state = current_alarm.status
            await __handle_alarm(current_alarm, message)


async def __handle_alarm(alarm: AlarmModel, message: types.Message):
    if alarm.status:
        print('Отбой тревоги')
        await message.answer('🟢 Отбой тревоги: ' + alarm.update_time)
    else:
        print('Тревога')
        await message.answer('🔴 Тревога: ' + alarm.update_time)


def handle_state(state: AlarmModel):
    if state:
        return "По кайфу"
    else:
        return "Ты еще не в коридоре?"


executor.start_polling(dispatcher, skip_updates=True)
