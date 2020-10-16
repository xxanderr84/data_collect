import requests
from bs4 import BeautifulSoup as bs
import json


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

# https://www.superjob.ru/vacancy/search/?keywords=python&noGeo=1&page=2
main_link = 'https://www.superjob.ru/'
add_link = 'vacancy/search/?keywords=python&noGeo=1'
while True:
    response = requests.get(main_link + add_link, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancies_list = soup.findAll('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})
    for vacancy in vacancies_list:
        vacancy_data = {'site': main_link}
        vacancy_info = vacancy.find('a')
        vacancy_data['title'] = vacancy_info.text
        vacancy_data['url'] = vacancy_info['href']
        vacancy_salary = vacancy.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'})
        if vacancy_salary is None:
            vacancy_data.update(get_salary(''))
        else:
            vacancy_data.update(get_salary(vacancy_salary.text))
        vacancies.append(vacancy_data)
    next_page = soup.find('a', {'rel': 'next'})
    if next_page is None:
        break
    add_link = next_page['href']

with open('response.json', 'w') as f:
    json.dump(vacancies, f)
