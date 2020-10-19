from pymongo import MongoClient
from pprint import pprint


def get_vacancies(salary: float, data):
    for item in data.find({'$or': [{'max': {'$gt': salary}}, {'min': {'$lt': salary}}]}):
        pprint(item)


while True:
    need_salary = input('Введите зарплату: ')
    try:
        need_salary = float(need_salary)
        break
    except ValueError:
        print('Нужно вводить цифры')

client = MongoClient('127.0.0.1', 27017)
db = client['vacancy']
hh = db.hh
sj = db.sj
get_vacancies(need_salary, hh)
get_vacancies(need_salary, sj)
