import os
import ray  # Для работы с modin.pandas
import modin.pandas as pd  # Многопоточная обработка данных
import numpy as np
import matplotlib.pyplot as plt
import requests
import time
import re
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

def fetch_currency_rates(year, month, currency_codes):
    """
    Получает курсы валют за указанный месяц и год.

    Args:
        year (int): Год.
        month (int): Месяц.
        currency_codes (list): Список кодов валют для обработки.

    Returns:
        tuple: Ключ в формате 'YYYY-MM' и словарь курсов валют.
    """
    date_string = f"01/{month:02d}/{year}"
    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={date_string}"

    for attempt in range(40):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
            print(f"[!] Ошибка {response.status_code}. Повтор через 60 секунд: {url}")
            time.sleep(60)
        except Exception as e:
            print(f"[!] Ошибка при запросе ({attempt + 1}/40): {e}")
            time.sleep(60)
    else:
        return f"{year}-{month:02d}", {}

    try:
        root = ET.fromstring(response.content)
        rates = {}
        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            if char_code in currency_codes:
                nominal = int(valute.find('Nominal').text)
                value = float(valute.find('Value').text.replace(',', '.'))
                rates[char_code] = value / nominal
        return f"{year}-{month:02d}", rates
    except Exception as e:
        print(f"[!] Ошибка парсинга XML: {e}")
        return f"{year}-{month:02d}", {}

def fetch_all_currency_rates():
    """
    Получает курсы валют с января 2003 года по декабрь 2024 года.

    Returns:
        dict: Словарь с курсами валют по месяцам.
    """
    currency_codes = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']
    tasks = [(year, month, currency_codes) for year in range(2003, 2025) for month in range(1, 13)]

    rates = {}
    with ThreadPoolExecutor() as executor:
        for key, data in executor.map(lambda args: fetch_currency_rates(*args), tasks):
            rates[key] = data

    return rates

def calculate_avg_salary(row, exchange_rates):
    """
    Рассчитывает среднюю зарплату в рублях.

    Args:
        row (pd.Series): Строка данных.
        exchange_rates (dict): Словарь курсов валют.

    Returns:
        float: Средняя зарплата в рублях.
    """
    salary_from = row['salary_from']
    salary_to = row['salary_to']
    currency = row['salary_currency']
    date = row['data']

    avg_salary = (salary_from + salary_to) / 2 if salary_from and salary_to else salary_from or salary_to
    if not avg_salary or currency == 'RUR' or not currency:
        return avg_salary

    return exchange_rates.get(date, {}).get(currency, np.nan) * avg_salary if date in exchange_rates else np.nan

def extract_date(value):
    """
    Извлекает дату в формате 'YYYY-MM'.

    Args:
        value (str): Дата.

    Returns:
        str: Дата в формате 'YYYY-MM'.
    """
    return str(value)[:7]

def extract_year(value):
    """
    Извлекает год из даты.

    Args:
        value (str): Дата.

    Returns:
        int: Год.
    """
    return int(str(value)[:4])

def create_html_report(df):
    """
    Создает HTML-отчет из DataFrame.

    Args:
        df (pd.DataFrame): Данные для отчета.
    """
    df = df.dropna()

    if 'name' in df.columns:
        df = df.drop(columns=['avg_salary'])

    df.columns = ["Город", "Кол-во вакансий"]
    html_content = df._to_pandas().to_html(
        index=False,
        border=1,
        classes='table table-dark table-bordered table-hover table-sm',
        float_format='{:,.0f}'.format
    )
    html_content = re.sub(r'text-align: right;', 'text-align: center;', html_content)

    with open('vacancy_report.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print("[i] HTML-отчет успешно создан!")

if __name__ == "__main__":
    os.environ["MODIN_ENGINE"] = "ray"
    ray.init()

    df = pd.read_csv("Z:\\vacancies_2024.csv", parse_dates=['published_at'])

    keywords = [
        'java', 'ява', 'джава', 'java-программист', 'spring', 'hibernate',
        'struts', 'vaadin', 'micronaut', 'quarkus', 'play framework', 'jhipster',
        'jakarta ee', 'log4j', 'slf4j', 'JPA', 'JDBC', 'jvm'
    ]

    exclusions = [
        'javascript', 'node.js', 'typescript', 'angular', 'react', 'vue',
        'c', 'golang', 'go', 'c++', 'assembly', 'rust', 'kotlin', 'groovy', 'scala'
    ]

    filtered_df = df[
        df['name'].str.lower().str.contains('|'.join(keywords), na=False) &
        ~df['name'].str.lower().str.contains('|'.join(exclusions), na=False)
    ]

    filtered_df[['salary_from', 'salary_to']] = filtered_df[['salary_from', 'salary_to']].apply(pd.to_numeric, errors='coerce')
    filtered_df['data'] = filtered_df['published_at'].apply(extract_date)

    exchange_rates = fetch_all_currency_rates()
    filtered_df['avg_salary'] = filtered_df.apply(lambda row: calculate_avg_salary(row, exchange_rates), axis=1)
    filtered_df = filtered_df[filtered_df['avg_salary'] < 10_000_000]
    filtered_df['year'] = filtered_df['published_at'].apply(extract_year)

    pivot_df = filtered_df._to_pandas().pivot_table(
        index='area_name',
        values=['avg_salary', 'name'],
        aggfunc={'avg_salary': 'mean', 'name': 'count'}
    ).reset_index().sort_values(by=['name', 'avg_salary'], ascending=False)

    top_cities = pivot_df.head(9)
    other_cities_count = pivot_df['name'].iloc[9:].sum()
    other_cities = pd.DataFrame({'area_name': ['Другие'], 'name': [other_cities_count]})

    final_df = pd.concat([top_cities, other_cities], axis=0)

    create_html_report(final_df)

    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_facecolor('#25fc3b')
    plt.gcf().set_facecolor('#25fc3b')
    plt.style.use('dark_background')

    # делаем рамку белой
    for spine in ax.spines.values():
        spine.set_edgecolor('white')  # Цвет рамки
        spine.set_linewidth(1)  # Толщина рамки (можно уменьшить)

    # Настройка цвета и толщины тиков (меток осей)
    ax.tick_params(axis='both', colors='white', width=1)
    plt.pie(final_df['name'], autopct='%1.1f%%', startangle=140, labels=final_df['area_name'])
    plt.title("Доля вакансий java-программиста по городам", color='white')
    plt.grid(axis='y', color='white')
    plt.legend(labels=final_df['area_name'])
    plt.savefig("Доля вакансий java-программист по городам.png", transparent=True, bbox_inches='tight')
    print("[i] Диаграмма успешно сохранена!")
