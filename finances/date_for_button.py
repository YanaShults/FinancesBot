import datetime
import calendar
import wr_date
from dateutil.relativedelta import relativedelta

# def read_date():
#     with open('date.txt', 'r') as file:
#         data = file.read()
#     year = int(data[0:4])
#     month = int(data[5:7])
#     return date(year=year, month=month)
#
#
# def write_date(date):
#     with open('date.txt', 'w') as file:
#         print(date, file=file)


def date(year=datetime.datetime.now().year, month=datetime.datetime.now().month):
    date = datetime.datetime(year, month, 1)
    wr_date.replace_date(date)
    return date


def next_month():
    today = wr_date.read_date()
    # print(today)
    # days = calendar.monthrange(today.year, today.month)[1]
    # next_month_date = today + datetime.timedelta(days=days)
    next_month_date = today + relativedelta(months=1)
    next_year = next_month_date.year
    next_month = next_month_date.month
    return date(year=next_year, month=next_month)


def prev_month():
    today = wr_date.read_date()
    print(today)
    # days = calendar.monthrange(today.year, today.month)[1]
    # prev_month_date = today - datetime.timedelta(days=days)
    prev_month_date = today - relativedelta(months=1)
    prev_year = prev_month_date.year
    prev_month = prev_month_date.month
    return date(year=prev_year, month=prev_month)

