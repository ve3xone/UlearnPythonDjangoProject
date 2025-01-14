import os
import ray # Нужно для работы modin.pandas
import modin.pandas as pd # Многопоток #3 minutes and 24 seconds
#import pandas as pd # Однопоток
import numpy as np
from collections import Counter
from itertools import islice
import matplotlib.pyplot as plt
import requests
import time
import re
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor


def fetch_currency_data(year, month, currencies):
    """
    Получает данные о курсе валют за указанный месяц и год, учитывая номинал.

    Args:
        year (int): Год запроса.
        month (int): Месяц запроса.
        currencies (list): Список кодов валют для фильтрации.

    Returns:
        tuple: Ключ (строка формата 'YYYY-MM') и словарь с курсами валют.
    """
    date_str = f"01/{month:02d}/{year}"
    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={date_str}"

    try:
        # Для того чтоб если упал реквест
        # Пытается выполнить запрос до 40 раз в случае неудачи
        # делая паузу в 60 секунд между попытками
        # На гугл коллаб были проблемы после данных действий данные были полные
        for attempt in range(40):
            try:
                response = requests.get(url)
                
                print(f'{response.status_code} - {url}')
                if response.status_code != 200:
                    print(f'[!] Ждем 60 сек... так как не получили ответ: {response.status_code} - {url}')
                    time.sleep(60)
                    continue
                
                break
            except:
                print(f"Ошибка при выполнении запроса. Попытка {attempt + 1} из 40. ({url})")
                time.sleep(60)

        # Парсинг XML
        root = ET.fromstring(response.content)
        result = {}
        for item in root.findall('Valute'):
            char_code = item.find('CharCode').text
            if char_code in currencies:
                nominal = int(item.find('Nominal').text)  # Номинал валюты
                value = float(item.find('Value').text.replace(',', '.'))  # Курс валюты
                result[char_code] = value / nominal  # Корректировка курса с учетом номинала

        return f"{year}-{month:02d}", result

    except Exception as e:
        print(f"Error fetching data for {date_str}: {e}")
        return f"{year}-{month:02d}", {}


def get_all_currency():
    """
    Получает курсы валют из ЦБР за период с января 2003 года по декабрь 2024 года.

    Returns:
        dict: Словарь с курсами валют по месяцам.
    """
    currencies = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']
    result = {}

    tasks = [(year, month, currencies) for year in range(2003, 2025) 
                                       for month in range(1, 13) 
                                       if not (year == 2024 and month == 12)]

    with ThreadPoolExecutor() as executor:
        for key, monthly_data in executor.map(lambda args: fetch_currency_data(*args), tasks):
            result[key] = monthly_data

    return result


def avg_salary(row, table_curr):
    """
    Рассчитывает среднюю зарплату на основе данных из строки DataFrame.

    Args:
        row (pd.Series): Строка DataFrame с данными о зарплате.
        table_curr (dict): Словарь курсов валют.

    Returns:
        float: Средняя зарплата в рублях или NaN, если данные отсутствуют.
    """
    salary_from = row['salary_from']
    salary_to = row['salary_to']
    currency = row['salary_currency']
    date = row['data']

    res = (salary_from + salary_to) / 2 if salary_from and salary_to else salary_from or salary_to
    if not res or currency == 'RUR' or not currency:
        return res

    return table_curr.get(date, {}).get(currency, np.nan) * res if date in table_curr else np.nan


def extract(value):
    """
    Извлекает дату в формате 'YYYY-MM'.

    Args:
        value (str): Полное значение даты.

    Returns:
        str: Дата в формате 'YYYY-MM'.
    """
    return str(value)[:7]


def extract_year(value):
    """
    Извлекает год из строки даты.

    Args:
        value (str): Полное значение даты.

    Returns:
        int: Год.
    """
    return int(str(value)[:4])


def create_html_table(yearly_count, year):
    # Удаляем строки с пропущенными значениями
    yearly_count = yearly_count.dropna()

    # Преобразуем DataFrame Modin в Pandas только для вызова to_html
    # Создаем HTML-таблицу с использованием Pandas
    html_string = yearly_count._to_pandas().to_html(
        index=False,  # Отключаем индекс в HTML
        border=1,
        classes='table table-dark table-bordered table-hover table-sm',
        float_format='{:,.0f}'.format  # Форматирование чисел
    )

    # Заменяем text-align: right; на text-align: center;
    html_string = re.sub(r'text-align: right;', 'text-align: center;', html_string)

    with open(f'top20-my-vac-year_{year}.html', 'w', encoding='utf-8') as f:
        f.write(html_string)
    
    print("[i] HTML таблица успешно создана!")


def top_skills_analytics(year):
    all_skills = df_copy[(df_copy['year'] == year) & (df_copy['key_skills'].notna())]
    all_skills = all_skills['key_skills'].str.cat(sep='\n').split('\n')
    skill_frequency = Counter(all_skills)

    sorted_dict_desc = dict(sorted(skill_frequency.items(), key=lambda item: item[1], reverse=True))
    first_20_pairs = dict(islice(sorted_dict_desc.items(), 20))


    skills_frame = pd.DataFrame.from_dict(first_20_pairs, orient='index').reset_index()
    skills_frame.columns = ['skill', 'freq']
    skill = skills_frame.sort_values(by='freq', ascending=True)
    skills_frame = skills_frame.sort_values(by='freq', ascending=False)
    skills_frame_rename = skills_frame.rename(columns={'skill': 'Навык', 'freq': 'Частота'})
    skills_frame_rename = skills_frame_rename.reset_index(drop=True)
    skills_frame_rename.index = skills_frame_rename.index + 1

    create_html_table(skills_frame_rename, year)

    fig, ax = plt.subplots(figsize=(40, 30))
    ax.set_facecolor('#25fc3b')
    plt.gcf().set_facecolor('#25fc3b')
    plt.style.use('dark_background')

    # делаем рамку белой
    for spine in ax.spines.values():
        spine.set_edgecolor('white')  # Цвет рамки
        spine.set_linewidth(1)  # Толщина рамки (можно уменьшить)
    
    # Настройка цвета и толщины тиков (меток осей)
    ax.tick_params(axis='both', colors='white', width=1)
    plt.title(f"ТОП-20 навыков за {year} для java-программиста", fontsize=30, color='white')
    plt.barh(skill['skill'], skill['freq'], color='blue')
    plt.yticks(fontsize=29)
    plt.xticks(rotation=45, fontsize=29)
    plt.grid(axis='y', color='white')
    plt.savefig("top20_skills_for_java-программиста_" + str(year) + "_year.png", transparent=True, bbox_inches='tight')


if __name__ == "__main__":
    # Нужно для работы modin.pandas
    os.environ["MODIN_ENGINE"] = "ray"
    ray.init()

    df = pd.read_csv("Z:\\vacancies_2024.csv", parse_dates=['published_at']) #Использую RAMDISK
    
    df_copy = df.copy()
    names = [
        'java', 'ява', 'джава', 'java-программист', 'spring', 'hibernate', 'struts', 
        'vaadin', 'micronaut', 'quarkus', 'play framework', 'jhipster', 'jakarta ee', 
        'log4j', 'slf4j', 'JPA', 'JDBC', 'jvm'
    ]
    exclusions = ['javascript', 'node.js', 'typescript', 'angular', 'react', 'vue',
                  'c', 'golang', 'go', 'c++', 'assembly', 'rust', 'kotlin', 'groovy', 'scala']  # Список исключений

    # Фильтрация с учетом исключений
    df_copy = df_copy[
        df_copy['name'].str.lower().str.contains('|'.join(names), na=False) &
        ~df_copy['name'].str.lower().str.contains('|'.join(exclusions), na=False)
    ]
    df_copy[['salary_from','salary_to']] = df_copy[['salary_from','salary_to']].map(lambda x: float(x))
    df_copy['data'] = df_copy['published_at'].apply(extract)
    table_curr = get_all_currency()
    df_copy['avg_salary'] = df_copy.apply(lambda row: avg_salary(row, table_curr), axis=1)
    df_copy = df_copy[df_copy['avg_salary'] < 10_000_000]
    df_copy['year'] = df_copy['published_at'].apply(extract_year)

    for i in range(2015, 2025):
        top_skills_analytics(i)
