import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import requests
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor


def fetch_currency_rates(year, month, target_currencies):
    """
    Получает данные о курсах валют за указанный год и месяц.

    Args:
        year (int): Год, за который запрашиваются данные.
        month (int): Месяц, за который запрашиваются данные.
        target_currencies (list): Список кодов валют для фильтрации.

    Returns:
        tuple: Ключ в формате 'YYYY-MM' и словарь с курсами валют.
    """
    date_str = f"01/{month:02d}/{year}"
    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={date_str}"

    for attempt in range(40):
        try:
            response = requests.get(url)
            print(f'{response.status_code} - {url}')
            if response.status_code == 200:
                break
            print(f'[!] Ждем 60 сек... так как не получили ответ: {response.status_code} - {url}')
            time.sleep(60)
        except requests.RequestException:
            print(f"Ошибка при выполнении запроса. Попытка {attempt + 1} из 40. ({url})")
            time.sleep(60)
    else:
        return f"{year}-{month:02d}", {}

    try:
        root = ET.fromstring(response.content)
        rates = {}
        for item in root.findall('Valute'):
            char_code = item.find('CharCode').text
            if char_code in target_currencies:
                nominal = int(item.find('Nominal').text)
                value = float(item.find('Value').text.replace(',', '.'))
                rates[char_code] = value / nominal
        return f"{year}-{month:02d}", rates
    except ET.ParseError as e:
        print(f"Ошибка парсинга XML для {date_str}: {e}")
        return f"{year}-{month:02d}", {}


def fetch_all_currency_rates():
    """
    Получает курсы валют за период с января 2003 года по декабрь 2024 года.

    Returns:
        dict: Словарь с курсами валют по месяцам.
    """
    target_currencies = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']
    rates = {}
    
    tasks = [(year, month, target_currencies) for year in range(2003, 2025) 
             for month in range(1, 13) if not (year == 2024 and month == 12)]

    with ThreadPoolExecutor() as executor:
        for key, monthly_rates in executor.map(lambda args: fetch_currency_rates(*args), tasks):
            rates[key] = monthly_rates

    return rates


def calculate_average_salary(row, currency_rates):
    """
    Рассчитывает среднюю зарплату в рублях.

    Args:
        row (pd.Series): Строка DataFrame с данными о зарплате.
        currency_rates (dict): Словарь с курсами валют.

    Returns:
        float: Средняя зарплата в рублях или NaN, если данные отсутствуют.
    """
    salary_from = row['salary_from']
    salary_to = row['salary_to']
    currency = row['salary_currency']
    date = row['data']

    salary_avg = (salary_from + salary_to) / 2 if salary_from and salary_to else salary_from or salary_to
    if not salary_avg or currency == 'RUR' or not currency:
        return salary_avg

    return currency_rates.get(date, {}).get(currency, np.nan) * salary_avg if date in currency_rates else np.nan


def extract_year_month(date_value):
    """
    Извлекает год и месяц в формате 'YYYY-MM'.

    Args:
        date_value (str): Полное значение даты.

    Returns:
        str: Дата в формате 'YYYY-MM'.
    """
    return str(date_value)[:7]


def extract_year(date_value):
    """
    Извлекает год из строки даты.

    Args:
        date_value (str): Полное значение даты.

    Returns:
        int: Год.
    """
    return int(str(date_value)[:4])


def generate_html_table(dataframe):
    """
    Создает HTML-таблицу из DataFrame и сохраняет её в файл.

    Args:
        dataframe (pd.DataFrame): DataFrame с данными о зарплатах.

    Returns:
        None
    """
    dataframe = dataframe.groupby('area_name', as_index=False)['avg_salary'].mean()
    dataframe = dataframe.sort_values(by='avg_salary', ascending=False).dropna()
    dataframe.columns = ["Расположение", "Средняя Зарплата"]

    html_content = dataframe.to_html(index=False, border=1,
                                     classes='table table-dark table-bordered table-hover table-sm',
                                     float_format='{:,.0f}'.format)
    html_content = re.sub(r'text-align: right;', 'text-align: center;', html_content)

    with open('salary_by_city.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print("[i] HTML таблица успешно создана!")


def process_salary_data(dataframe, currency_rates):
    """
    Обрабатывает данные о зарплатах, строит график и сохраняет HTML-таблицу.

    Args:
        dataframe (pd.DataFrame): DataFrame с данными вакансий.
        currency_rates (dict): Словарь с курсами валют.

    Returns:
        None
    """
    df_copy = dataframe.copy()
    df_copy['data'] = df_copy['published_at'].apply(extract_year_month)
    df_copy['avg_salary'] = df_copy.apply(lambda row: calculate_average_salary(row, currency_rates), axis=1)
    df_copy = df_copy[df_copy['avg_salary'] < 10_000_000]
    df_copy['year'] = df_copy['published_at'].apply(extract_year)

    total_vacancies = df_copy['name'].count()
    city_vacancy_counts = df_copy['area_name'].value_counts()
    significant_cities = city_vacancy_counts[city_vacancy_counts > total_vacancies * 0.01].index

    filtered_df = df_copy[df_copy['area_name'].isin(significant_cities)]
    salary_data = filtered_df.pivot_table(
        index='area_name', values=['avg_salary', 'name'],
        aggfunc={'avg_salary': 'mean', 'name': 'count'}
    ).reset_index().sort_values(by=['name', 'avg_salary'], ascending=False).head(16)

    salary_data = salary_data[['area_name', 'avg_salary']].sort_values(by='avg_salary', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 7))
    plt.title("Уровень зарплат по городам, где доля вакансий больше 1%", color='white')
    plt.barh(salary_data['area_name'], salary_data['avg_salary'], color='blue')
    plt.xlabel("Средняя зарплата", color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.grid(axis='y', color='white')
    plt.savefig("salary_by_city.png", transparent=True, bbox_inches='tight')
    plt.close()

    generate_html_table(salary_data)


dataframe = pd.read_csv("Z:\\vacancies_2024.csv", parse_dates=['published_at'])
currency_rates = fetch_all_currency_rates()
process_salary_data(dataframe, currency_rates)