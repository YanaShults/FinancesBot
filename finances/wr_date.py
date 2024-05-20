import datetime
import json


# diction = {
#     'date': None,
#     'first_date': None,
#     'second_date': None,
#     'option': None
# }
#
#
# with open('date.json', 'w') as file:
#     json.dump(diction, file, indent=4)

#date - для даты, кот. отображ. на календаре
#first_date - для первой выбранной даты (начала отсчета)
#second_date - для второй выбранной даты


def datetime_date(date):
    datetime_object = datetime.datetime.strptime(date, "%Y-%m-%d")
    return datetime_object


def str_date(date):
    return date.strftime('%Y-%m-%d')


def read_file():
    with open('date.json', 'r') as file:
        data = json.load(file)
    return data
# print(read_file())


def read_date():
    return datetime_date(read_file()['date'])
# print(read_date())


def read_first_date():
    return datetime_date(read_file()['first_date'])


def read_second_date():
    return datetime_date(read_file()['second_date'])


def read_option():
    return read_file()['option']


def write_file(data):
    with open('date.json', 'w') as file:
        json.dump(data, file)


def replace_date(date):
    data = read_file()
    data['date'] = str_date(date)
    # print(data)
    write_file(data)
# replace_date(datetime.datetime(2023, 10, 5).strftime('%Y.%d.%m'))
# replace_date(datetime.datetime(2023, 10, 5))


def replace_first_date(date):
    data = read_file()
    data['first_date'] = str_date(date)
    write_file(data)


def replace_second_date(date):
    data = read_file()
    data['second_date'] = str_date(date)
    write_file(data)


def replace_option(option):
    data = read_file()
    data['option'] = option
    write_file(data)


def replace_none():
    data = read_file()
    data['second_date'] = None
    data['first_date'] = None
    data['option'] = None
    write_file(data)


def checking_selected_dates(day):
    cur_year_month = read_date()
    year = cur_year_month.year
    month = cur_year_month.month
    date = datetime.datetime(year, month, day)
    if read_file()['first_date'] is None:
        replace_first_date(date)
        return False
    elif read_file()['second_date'] is None:
        replace_second_date(date)
        return True

