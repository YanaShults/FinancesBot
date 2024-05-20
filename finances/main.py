import datetime
from dotenv import load_dotenv
import os

from aiogram import Bot, types
from aiogram.utils import executor
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup,\
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

import config
import keyboard
from db import Sqlite
from categories import cat
import date_for_button
import wr_date

load_dotenv()
token = os.getenv('TOKEN')

storage = MemoryStorage()
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


class info(StatesGroup):
    category = State()
    income = State()
    option = State()


@dp.message_handler(Command('start'), state=None)
async def welcome(message):
    global obj
    with open('user.txt', 'r') as file:
        data_in_file = file.readlines()

    name_db = str(message.chat.id) + 'fin'


    if not str(message.chat.id)+'\n' in data_in_file:
        with open('user.txt', 'a') as file:
            print(str(message.chat.id), file=file)

        obj = Sqlite(name_db)
        obj.create_calculation_table()
        obj.create_table_categories()
        obj.create_description_table()

    obj = Sqlite(name_db)

    await bot.send_message(message.chat.id, f'Привет, "{message.from_user.first_name}",'
                                            f' Бот Работает',
                           reply_markup=keyboard.start,
                           parse_mode='Markdown')


@dp.message_handler(content_types=['text'])
async def get_message(message):
    global current_date
    if message.text == 'Добавить расходы':
        await bot.send_message(message.chat.id, text=f'Выберите категорию',
                                   reply_markup=keyboard.stat,
                                   parse_mode='Markdown')
    elif message.text == 'Добавить доходы':
        await bot.send_message(message.chat.id, text=f'Введите сумму!',
                               parse_mode='Markdown')
        await info.income.set()
    elif message.text == 'Статистика':
        current_date = date_for_button.date()
        # await bot.send_message(message.chat.id, text=f'Button',
        #                        reply_markup=keyboard.date_button(current_date)[-1],
        #                        parse_mode='Markdown')
        await bot.send_message(message.chat.id, text=f'Выберите категорию',
                               reply_markup=keyboard.choose_option(),
                               parse_mode='Markdown')
    elif message.text == 'Расходы за месяц':
        data = obj.count_month_money_spent()
        await bot.send_message(message.chat.id, text=f'Ваши расходы за месяц составляют *{data}*',
                               parse_mode='Markdown')
    elif message.text == 'Доход за месяц':
        data = obj.count_month_income()
        await bot.send_message(message.chat.id, text=f'Ваш доход за месяц составляет *{data}*',
                               parse_mode='Markdown')
    elif message.text == 'Информация':
        answer = 'info'
        wr_date.replace_option(answer)
        current_date = date_for_button.date()
        await bot.send_message(message.chat.id,
                               text=f'Выберите дату начала: ',
                               reply_markup=keyboard.date_button(current_date)[-1],
                               parse_mode='Markdown')


# здесь может быть ляп с lambda
# когда выбрали категорию запускается состояние category lambda i: True
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("cat_"))
async def join(call: types.CallbackQuery):
    global category
    category = call.data[4:]
    if wr_date.read_option() is None:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'Введите сумму!',
                                    parse_mode='Markdown')
        await info.category.set()
    else:
        wr_date.replace_option(category)
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'Выберите дату начала: ',
                                    reply_markup=keyboard.date_button(current_date)[-1],
                                    parse_mode='Markdown')


#обработка состояния category, сохраняет сумму по определ. категории
@dp.message_handler(state=info.category)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    # category = info.category
    await state.update_data(answer1=answer)
    data = await state.get_data()
    answer = data.get('answer1')
    obj.add_expenses(category, int(answer))
    await message.answer(f'Ваша категория {category}\n'
                         f'Ваша сумма: {answer}')
    await state.finish()



#обработка состояния income, добавляем введенную сумму
@dp.message_handler(state=info.income)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    data = await state.get_data()
    answer = data.get('answer1')
    obj.add_income(int(answer))
    await message.answer(f'Ваша сумма: *{answer}*', parse_mode='Markdown')
    await state.finish()


@dp.callback_query_handler(text_contains='previous')
async def join(call: types.CallbackQuery):
    date = date_for_button.prev_month()
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard.date_button(date)[-1])


@dp.callback_query_handler(text_contains='next')
async def join(call: types.CallbackQuery):
    date = date_for_button.next_month()
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard.date_button(date)[-1])


@dp.callback_query_handler(text_contains='total_amount')
async def spend_money(call: types.CallbackQuery):
    answer = call.data
    wr_date.replace_option(answer)
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=f'Выберите дату начала: ',
                                reply_markup=keyboard.date_button(current_date)[-1],
                                parse_mode='Markdown')


@dp.callback_query_handler(text_contains='income')
async def spend_money(call: types.CallbackQuery):
    answer = call.data
    wr_date.replace_option(answer)
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=f'Выберите дату начала: ',
                                reply_markup=keyboard.date_button(current_date)[-1],
                                parse_mode='Markdown')


@dp.callback_query_handler(text_contains='select_cat')
async def spend_money(call: types.CallbackQuery):
    answer = call.data
    wr_date.replace_option(answer)
    # await bot.send_message(call.message.chat.id, text=f'Выберите категорию',
    #                        reply_markup=keyboard.stat,
    #                        parse_mode='Markdown')
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=f'Выберите категорию: ',
                                reply_markup=keyboard.stat,
                                parse_mode='Markdown')


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("date_"))
async def spend_money(call: types.CallbackQuery):
    answer = int(call.data[5:])
    res = wr_date.checking_selected_dates(answer)

    if res:
        first_date = wr_date.read_first_date().date()
        second_date = wr_date.read_second_date().date()
        option = wr_date.read_option()
        wr_date.replace_none()
        if option == 'info':
            text = obj.all_info_str(first_date, second_date)
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text=text,
                                        parse_mode='Markdown')
        else:
            if option == 'total_amount':
                data = obj.count_month_money_spent(first_date, second_date)
            elif option == 'income':
                data = obj.count_month_income(first_date, second_date)
            else:
                data = obj.count_money_category(first_date, second_date, option)

            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text=f'Полученные данные: *{data}*\n'
                                             f'За период с *{first_date} по {second_date}*',
                                        parse_mode='Markdown')



if __name__ == '__main__':
    print('Good!')
executor.start_polling(dp)
