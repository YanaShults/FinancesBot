import sqlite3
import datetime
import json
import categories


class Sqlite:
    def __init__(self, db_name):
        self.con = sqlite3.connect(
            database=db_name,
        )
        self.cur = self.con.cursor()

    # создание таблицы categories
    def create_table_categories(self):
        # self.cur.execute('''CREATE TABLE IF NOT EXISTS categories(
        #         cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         date date UNIQUE,
        #         food INTEGER,
        #         clothes INTEGER,
        #         entertainment INTEGER,
        #         dancing INTEGER,
        #         sport INTEGER,
        #         transport INTEGER,
        #         house INTEGER,
        #         cafe INTEGER,
        #         cosmetics INTEGER,
        #         subscriptions INTEGER,
        #         other INTEGER,
        #         total_amount INTEGER);
        # ''')

        self.cur.execute(f'CREATE TABLE IF NOT EXISTS categories('
                         f'cat_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                         f'date date UNIQUE, {categories.str_cat_db}, total_amount INTEGER);')

    # создание таблицы calculation_table
    def create_calculation_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS calculation_table(
                        calc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date date UNIQUE,
                        income INTEGER,
                        remainder INTEGER,
                        accumulation INTEGER,
                        money_spent INTEGER);
                ''')

    # # создание таблицы с описанием
    # def create_description_table(self):
    #     self.cur.execute('''CREATE TABLE IF NOT EXISTS description_table(
    #                             descr_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                             cat_id INTEGER UNIQUE,
    #                             description TEXT
    #                             );
    #                     ''')
    # 
    #
    # #
    #
    # # заполнение таблицы с описанием
    # def add_description(self, text):
    #     cat_id =
    #     self.cur.execute('''
    #                             INSERT INTO description_table(
    #                             cat_id,
    #                             description
    #                             ) VALUES (?,?)
    #                         ''', (cat_id, text))
    #     self.con.commit()

    # базовое заполнение таблицы categories (если еще не было определенной даты)
    def __filling_the_table_categories(self, date):
        text = f'INSERT INTO categories(date,' +\
               f'{categories.str_cat}' +\
               f',total_amount) VALUES (?, ? {",? " * categories.count_cat})'
        print(text)
        data = tuple([date] + [0] * (categories.count_cat+1))
        print(data)
        self.cur.execute(text, data)
        # self.cur.execute('''
        #                 INSERT INTO categories(
        #                 date,
        #                 food,
        #                 clothes,
        #                 entertainment,
        #                 dancing,
        #                 sport,
        #                 transport,
        #                 house,
        #                 cafe,
        #                 cosmetics,
        #                 subscriptions,
        #                 other,
        #                 total_amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        #             ''', (date, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.con.commit()

    # базовое заполнение таблицы calculation_table (если еще не было определенной даты)
    #income -  доход
    # remainder - остаток
    # accumulation - накопление
    def __filling_the_table_calculation_table(self, date):
        self.cur.execute('''
                        INSERT INTO calculation_table(
                        date,
                        income, 
                        remainder,
                        accumulation,
                        money_spent) VALUES (?, ?, ?, ?, ?)
                    ''', (date, 0, 0, 0, 0))
        self.con.commit()

    # пользователь выбирает дату или по умолч. today
    def create_date(self, year=None, month=None, day=None):
        if year == None or month == None or day == None:
            date = datetime.datetime.today()
        else:
            date = datetime.datetime(year, month, day)
        str_date = date.strftime('%Y-%m-%d')
        return str_date

    # добавляем сумму по определенной категории и дате
    def add_expenses(self, cat, value, year=None, month=None, day=None):
        str_date = self.create_date(year, month, day)
        find = self.cur.execute('''
            SELECT * FROM categories WHERE date=?
        ''', (str_date,)).fetchone()
        print(find)
        if find is None:
            self.__filling_the_table_categories(str_date)

        find = self.cur.execute('''
                    SELECT * FROM categories WHERE date=?
                ''', (str_date,)).fetchone()
        id = find[0]
        amount_cat = self.cur.execute(f'SELECT {cat} FROM categories WHERE cat_id=?',
                                      (id,)).fetchone()[0]
        new_amount_cat = amount_cat + value
        total_amount = self.cur.execute(f'SELECT total_amount FROM categories WHERE cat_id=?',
                                        (id,)).fetchone()[0]
        new_total_amount = total_amount + value
        self.cur.execute(f'UPDATE categories SET {cat}={new_amount_cat}, '
                         f'total_amount={new_total_amount}'
                         f' WHERE cat_id={id}')
        self.con.commit()
        self.change_money_spent(str_date, value)
        find = self.cur.execute('''
                    SELECT * FROM categories WHERE date=?
                ''', (str_date,)).fetchone()
        print(find)

    # при изменении суммы расходов меняется поле потраченных денег
    def change_money_spent(self, date, value):
        find = self.cur.execute('''
                            SELECT * FROM calculation_table WHERE date=?
                        ''', (date,)).fetchone()
        if find is None:
            self.__filling_the_table_calculation_table(date)

        find = self.cur.execute('''
                            SELECT * FROM calculation_table WHERE date=?
                        ''', (date,)).fetchone()
        id = find[0]
        money_spent = self.cur.execute(f'SELECT money_spent FROM calculation_table WHERE calc_id=?',
                                       (id,)).fetchone()[0]
        new_money_spent = money_spent + value

        self.cur.execute(f'UPDATE calculation_table SET money_spent={new_money_spent}'
                         f' WHERE calc_id={id}')
        self.con.commit()

    # пополнение дохода
    def add_income(self, value, year=None, month=None, day=None):
        date = self.create_date(year, month, day)

        find = self.cur.execute('''
            SELECT * FROM calculation_table WHERE date=?
        ''', (date,)).fetchone()
        print(find)
        if find is None:
            self.__filling_the_table_calculation_table(date)
        find = self.cur.execute('''
                           SELECT * FROM calculation_table WHERE date=?
                       ''', (date,)).fetchone()
        '''calc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date date UNIQUE,
                        income INTEGER,
                        remainder INTEGER,
                        accumulation INTEGER,
                        money_spent INTEGER)'''
        print('1', find)
        id = find[0]
        income = find[2] + value
        accumulation = income * 0.1
        money_spent = find[5] + accumulation - find[4]
        remainder = income - money_spent
        self.cur.execute(f'UPDATE calculation_table SET income={income}, '
                         f'remainder={remainder}, '
                         f'accumulation={accumulation},'
                         f'money_spent={money_spent}  '
                         f'WHERE calc_id={id}')
        self.con.commit()
        find = self.cur.execute('''
                   SELECT * FROM calculation_table WHERE date=?
               ''', (date,)).fetchone()
        print('2', find)

    def __date_today_year_month(self):
        date = datetime.date.today()
        year = date.year
        month = date.month
        return year, month

    # узнать доход за текущий месяц или за выбранную дату
    def count_month_income(self, start_date=None, end_date=None):
        if start_date is None or end_date is None:
            date = self.__date_today_year_month()
            year = date[0]
            month = date[1]
            start_date = f'{year}-{month:02d}-01'
            end_date = f'{year}-{month:02d}-31'  # Предполагаем, что в месяце не более 31 дня

        query = "SELECT sum(income) FROM calculation_table WHERE date BETWEEN ? AND ?"
        find = self.cur.execute(query, (start_date, end_date)).fetchone()[0]

        return find

    # сколько потрачено в общем за текущий месяц или за выбранную дату
    def count_month_money_spent(self, start_date=None, end_date=None):
        if start_date is None or end_date is None:
            date = self.__date_today_year_month()
            year = date[0]
            month = date[1]
            start_date = f'{year}-{month:02d}-01'
            end_date = f'{year}-{month:02d}-31'  # Предполагаем, что в месяце не более 31 дня

        query = "SELECT sum(total_amount) FROM categories WHERE date BETWEEN ? AND ?"
        find = self.cur.execute(query, (start_date, end_date)).fetchone()[0]

        return find

    # сколько потрачено по конкретной категории за текущий месяц или за выбранную дату
    def count_money_category(self, start_date, end_date, category):

        query = f"SELECT sum({category}) FROM categories WHERE date BETWEEN ? AND ?"
        find = self.cur.execute(query, (start_date, end_date)).fetchone()[0]

        return find

    # информация по каждому дню за выбранный период времени
    def all_info_str(self, start_date, end_date):
        query = f"SELECT {categories.str_cat_db}, date, total_amount  FROM categories WHERE date BETWEEN ? AND ?"
        find = self.cur.execute(query, (start_date, end_date)).fetchall()

        text = f'Выбран период с {start_date} по {end_date}:\n\n'
        for i in range(len(find)):
            text += f'*{find[i][-2]}\n*'  # date
            for j in range(len(find[i][1:-1])):
                if find[i][j] != 0:
                    text += f'\t {categories.cat[j]}\t{find[i][j]}\n'
            text += f'\t*Расход за день:* {find[i][-1]}\n\n'

        text += f'Расходы: {self.count_month_money_spent(start_date, end_date)}\n'
        text += f'Доходы: {self.count_month_income(start_date, end_date)}\n'

        return text


a = 5
name_db = str(a) + 'fin'
obj = Sqlite(name_db)
obj.add_expenses('food', 50)
# a = obj.all_info_str(datetime.date(2023, 6, 1), datetime.date(2023, 6, 30))
# print(a)
# obj.count_month_money_spent()
# obj.count_month(2023, 6)
# obj.add_income(0)
# obj.add_expenses('clothes', 100)
# obj.add_income(50)
# obj.add_expenses('food', 100)
# obj.add_income(2000)
# with open('user.txt', 'r') as file:
#     date = file.readlines()
# for i in date:
#     if a == i:
#         break
# else:
#     with open('user.txt', 'a') as file:
#         print(a, file=file)
#     obj.create_table_categories()
#     obj.create_calculation_table()
#     obj.create_description_table()
