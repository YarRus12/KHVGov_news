import datetime

months = {1: 'января',
          2: 'февраля',
          3: 'марта',
          4: 'апреля',
          5: 'мая',
          6: 'июня',
          7: 'июля',
          8: 'августа',
          9: 'сентября',
          10: 'октября',
          11: 'ноября',
          12: 'декабря',
          }

def change_date(text: str) -> str:
    """Функция принимает в себя строковое значение с сайта
    Разделяет его и преобразует в дату,
    Возвращает функция текстовую дату принятого формата"""
    d, m, year = text.split(' ')
    year_ = int(year)
    for number, name in months.items():
        if name == m:
            month_ = number
    day_ = int(d)
    return str(datetime.date(year=year_, month=month_, day=day_))
