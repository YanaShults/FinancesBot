from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from categories import cat
import datetime
from calendar import monthrange
import date_for_button


start = types.ReplyKeyboardMarkup(resize_keyboard=True)

expenses = types.KeyboardButton('Добавить расходы')
sum_expenses = types.KeyboardButton('Расходы за месяц')
income = types.KeyboardButton('Добавить доходы')
sum_income = types.KeyboardButton('Доход за месяц')
info = types.KeyboardButton('Информация')
statis = types.KeyboardButton('Статистика')

start.add(expenses, sum_expenses)
start.add(income, sum_income)
start.add(info, statis)

stat = InlineKeyboardMarkup()
for i in cat:
    stat.add(InlineKeyboardButton(f'{i}', callback_data=f'cat_{i}'))


def empty_button():
    return InlineKeyboardButton('   ', callback_data='pass')


def date_button(date):
    # date = date_for_button.date()
    # date = datetime.datetime(year=2023, month=5, day=1)
    str_date = date.strftime('%Y.%m')
    date_button = InlineKeyboardMarkup(row_width=7)
    date_button.row(InlineKeyboardButton(f'<--', callback_data='previous'),
                    InlineKeyboardButton(f'{str_date}', callback_data='pass'),
                    InlineKeyboardButton(f'-->', callback_data='next'))
    date_button.row(InlineKeyboardButton(f'Mo', callback_data='pass'),
                    InlineKeyboardButton(f'Tu', callback_data='pass'),
                    InlineKeyboardButton(f'We', callback_data='pass'),
                    InlineKeyboardButton(f'Th', callback_data='pass'),
                    InlineKeyboardButton(f'Fr', callback_data='pass'),
                    InlineKeyboardButton(f'Sa', callback_data='pass'),
                    InlineKeyboardButton(f'Su', callback_data='pass'))
    sp = []
    count = 0
    # date_button.row(*sp)
    week_count = monthrange(date.year, date.month)
    first_weekday = week_count[0] # первый день недели месяца
    count_days = week_count[1] # кол-во дней в месяце
    count_d = 0
    start_empty_button = True

    while True:
        if start_empty_button:
            for i in range(first_weekday):
                sp.append(empty_button())
                count += 1
            days_left = 7 - count
            for i in range(1, days_left+1):
                count_d += 1
                # count += 1
                sp.append(InlineKeyboardButton(f'{i}', callback_data=f'date_{i}'))
            date_button.row(*sp)
            sp = []
            count = 0
            start_empty_button = False
        elif count_d < count_days:
            count_d += 1
            count += 1
            sp.append(InlineKeyboardButton(f'{count_d}', callback_data=f'date_{count_d}'))
            if count == 7:
                date_button.row(*sp)
                # if count_d == count_days:
                #     break
                sp = []
                count = 0

        elif count_d >= count_days:
            count += 1
            sp.append(empty_button())
            if count == 7:
                date_button.row(*sp)
                # sp = []
                # count = 0
                break

    return date, date_button


def choose_option():
    option = InlineKeyboardMarkup()
    option.add(InlineKeyboardButton(f'Расходы', callback_data=f'total_amount'))
    option.add(InlineKeyboardButton(f'Доходы', callback_data=f'income'))
    option.add(InlineKeyboardButton(f'Выбрать категорию', callback_data=f'select_cat'))
    return option


