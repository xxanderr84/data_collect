import sys
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup as bs


def add_vacancies(vacancy_list, data_collection):
    try:
        data_collection.insert_many(vacancy_list, ordered=False)
    finally:
        print(sys.exc_info()[0])


def get_salary(input_string: str):
    output_dict = {}
    if len(input_string) == 0 or input_string == 'По договорённости':
        output_dict['currency'] = None
        output_dict['min'] = None
        output_dict['max'] = None
        return output_dict
    temp = input_string.replace(' ', '')
    temp = temp.replace('\xa0', '')
    if temp.find('от') > 0:
        tmp_string = ''.join([k for k in temp if not k.isdigit()])
        tmp_string.replace('от ', '')
        output_dict['currency'] = tmp_string
        output_dict['min'] = ''.join(filter(str.isdigit, temp))
        output_dict['max'] = None
        return output_dict
    if temp.find('до') > 0:
        tmp_string = ''.join([k for k in temp if not k.isdigit()])
        tmp_string.replace('до ', '')
        output_dict['currency'] = tmp_string
        output_dict['max'] = ''.join(filter(str.isdigit, temp))
        output_dict['min'] = None
        return output_dict
    if temp.find('-') > 0:
        tmp_string = ''.join([i for i in temp if not i.isdigit()])
        tmp_string = tmp_string.replace('-', '')
        output_dict['currency'] = tmp_string
        temp = temp.replace(tmp_string, '')
        output_dict['min'] = float(temp[:temp.find('-')])
        output_dict['max'] = float(temp[temp.find('-') + 1:])
    return output_dict


# https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true
main_link = 'https://hh.ru/'
params = {'L_is_autosearch': 'false',
          'clusters': 'true',
          'enable_snippets': 'true',
          'text': 'python',
          'page': '0'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/86.0.4240.75 Safari/537.36'}
vacancies = []
while True:
    response = requests.get(main_link + 'search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancies_list = soup.findAll('div', {'data-qa': 'vacancy-serp__vacancy'})
    for vacancy in vacancies_list:
        vacancy_data = {'site': main_link}
        vacancy_title = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        vacancy_data['title'] = vacancy_title.text
        vacancy_data['url'] = vacancy_title['href']
        vacancy_data['_id'] = ''.join([k for k in vacancy_title['href'] if k.isdigit()])
        vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if vacancy_salary is None:
            vacancy_data.update(get_salary(''))
        else:
            vacancy_data.update(get_salary(vacancy_salary.text))
        vacancies.append(vacancy_data)
    next_page = soup.find('a', {'data-qa': 'pager-next'})
    if next_page is None:
        break
    params['page'] = next_page['data-page']
client = MongoClient('127.0.0.1', 27017)
db = client['vacancy']
hh = db.hh
add_vacancies(vacancies, hh)
