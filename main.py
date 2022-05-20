import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # условная конструкция тяжело читается,
        # лучше отформатировать в соотвествии с логикой, например,
        # действие-если-правильно
        # if условие
        # else действие-если-неправильно
        # или вообще переписать через or

        # не нашла в задании какой тип передается в функцию, возможно,
        # преобразование вообще не нужно
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # имя переменной лучше писать с маленькой буквы
        for Record in self.records:
            # вынести dt.datetime.now().date() в отдельную переменную
            if Record.date == dt.datetime.now().date():
                # можно переписать через +=
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # (today - record.date).days вынести в отдельную переменную и
            # переписать условие через min <= x <= max
            if ((today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий к функции не требуется, т.к. он дублирует название функции
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # что такое x? Неинформативное название переменной
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Зачем оборачивать строку в скобки?
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Из названия переменной понятно что в ней, комментарий не нужен
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Переменные USD_RATE и EURO_RATE не надо передавать в метод,
    # это переменные класса
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # я бы переписала часть с получением текущего баланса в указанной валюте.
        # можно определить словарь, который будет содержать в себе название
        # валюты, которое надо указать после цифры, и сам курс, что такое:
        # {'usd': {'currency_tail': 'USD', rate: USD_RATE}}
        # и переписать получение текущего баланса через этот словарь
        # это будет читаться проще и легче дописываться
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Зачем сравнение и почему 1?
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                # round(cash_remained, 2) вынести в отдельную переменную,
                # чтобы не вычислять внутри строки
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Лучше придерживаться единого стиля форматирования строки
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    # не надо переопределять, т.к. тут нет никакой нового логики
    def get_week_stats(self):
        super().get_week_stats()
