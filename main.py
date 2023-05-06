from requests import get, ConnectionError


def get_func_attrs(func):
    try:
        attrs = func.__attrs__
        print(f'Attributes for function {str(func)}')
        for atr in attrs:
            print(atr)
    except:
        print(f'Cant get function {str(func)} attributes')


# Адрес api метода для запроса get
url = 'https://api.hh.ru/vacancies'
search_text = '(python стажер OR стажировка IT OR intern python OR junior python) AND ' \
              'NOT (1C OR HR OR менеджер OR PHP OR Java OR JavaScript)'

param = {
    "text": search_text,  # название вакансии
    "area": ['1', '2019', '232'],  # Москва
    "page": 0,
    "per_page": 10,
    #"experience": "noExperience",    # нет опыта работы
    "employment":   # тип ханятости
        [
            "full",     # полная занятость
            "part",     # частичная
            "probation"    # стажировка
        ],
    "professional_roles": '11'  # Информационные технологии
}

# prof_role = get('https://api.hh.ru/professional_roles').json()
# import json
# print(type(prof_role))
#
#
# with open('prof_role.json', 'w', encoding='utf-8') as json_output:
#     json.dump(prof_role, json_output, indent=4, ensure_ascii=False)
#
# for dic in prof_role['categories']:
#     print(dic['id'], dic['name'])
#
# print(*prof_role['categories'][7]['roles'], sep='\n')

print('\n----------')
response = get(url, param)
print(response)
print(response.headers)
data = response.json()
print(data.keys())

print(f'Количестов вакансий: {data["found"]}')
print(f'Количестов страниц: {data["pages"]}')
print(f'Количестов вакансий на страницу: {data["per_page"]}')
print(f'Ссылка на запрос: {data["alternate_url"]}')


# import json
# with open('res.json', 'w', encoding='utf-8') as json_output:
#     json.dump(data, json_output, indent=4, ensure_ascii=False)

print(data['pages'])

import pandas as pd

df = pd.DataFrame(columns=
                  ['id', 'vacancy_name', 'company_name', 'prof_role', 'work_type','link',
                   'address', 'working_time_intervals', 'salary_from',
                   'salary_to'
                   ])

for i in range(0, data['pages']):
#for i in range(0, 2):
    cycled_param = {
        "text": search_text,  # название вакансии
        "area": ['1', '2019', '232'],  # Москва
        "page": i,
        "per_page": 10,
        #"experience": "noExperience",  # нет опыта работы
        "employment":  # тип ханятости
            [
                "full",  # полная занятость
                "part",  # частичная
                "probation"  # стажировка
            ],
        "professional_roles": '11'  # Информационные технологии
    }

    cycled_response = get(url, cycled_param)
    print(f"\nRequest num {i}\n")


    result = cycled_response.json()['items']
    for j in range(len(result)):

        my_dict = {}
        my_dict['id'] = result[j]["id"]
        my_dict['vacancy_name'] = result[j]["name"]
        my_dict['vacancy_name'] = result[j]["name"]
        my_dict['link'] = result[j]["alternate_url"]

        try:
            my_dict['working_time_intervals'] = result[j]["working_time_intervals"][0]['name']
        except:
            my_dict['working_time_intervals'] = ''


        if result[j]["salary"]:
            if result[j]["salary"]["from"]:
                my_dict['salary_from'] = result[j]["salary"]["from"]
            if result[j]["salary"]["to"]:
                my_dict['salary_from'] = result[j]["salary"]["to"]
        else:
            my_dict['salary_from'] = None
        try:
            my_dict['address'] = result[j]["address"]["raw"]
        except:
            my_dict['address'] = None
        my_dict['company_name'] = result[j]["employer"]["name"]
        my_dict['prof_role'] = result[j]["professional_roles"][0]["name"]
        my_dict['work_type'] = result[j]["employment"]["name"]

        try:
            print(result[j]['key_skills'])
        except:
            pass

        #print(f'id вакансии: {result[j]["id"]}')
        #print(f'Название вакансии: {result[j]["name"]}')
        #print(f'Ссылка на вакансию: {result[j]["alternate_url"]}')
        #print(f'ЗП: {result[j]["salary"]}')
        # try:
        #     print(f'Адресс: {result[j]["address"]["raw"]}')
        # except:
        #     print(f'Адресс:')
        #print(f'Название компании: {result[j]["employer"]["name"]}')
        #print(f'snippet: {result[j]["snippet"]}')
        #print(f'Напраление работы: {result[j]["professional_roles"][0]["name"]}')
        #print(f'Типы работы: {result[j]["employment"]["name"]}')
        #print(f'snippet: {result[j]["snippet"]}')
        #print("----------------------------------------------------------------\n")
        #print(my_dict)


        df.loc[len(df.index)] = my_dict

from openpyxl.workbook import Workbook

df.to_excel("output.xlsx")

print(df[df['work_type'] == 'Стажировка'].sort_values(by='company_name').to_string())