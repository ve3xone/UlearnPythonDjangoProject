import pandas as pd  # Использование многопоточного pandas
import numpy as np
import matplotlib.pyplot as plt
import requests
import time
import re
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor


def fetch_currency_data(year, month, currency_codes):
    """
    Получает данные о курсах валют за указанный месяц и год.

    Args:
        year (int): Год запроса.
        month (int): Месяц запроса.
        currency_codes (list): Список кодов валют для фильтрации.

    Returns:
        tuple: Ключ (строка формата 'YYYY-MM') и словарь с курсами валют.
    """
    date_str = f"01/{month:02d}/{year}"
    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={date_str}"

    for attempt in range(40):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
            time.sleep(60)  # Ожидание перед повторной попыткой
        except Exception as exc:
            print(f"Ошибка при выполнении запроса: {exc}. Попытка {attempt + 1} из 40.")
            time.sleep(60)
    else:
        print(f"Не удалось получить данные после 40 попыток: {url}")
        return f"{year}-{month:02d}", {}

    root = ET.fromstring(response.content)
    currency_data = {}

    for item in root.findall('Valute'):
        char_code = item.find('CharCode').text
        if char_code in currency_codes:
            nominal = int(item.find('Nominal').text)
            value = float(item.find('Value').text.replace(',', '.'))
            currency_data[char_code] = value / nominal

    return f"{year}-{month:02d}", currency_data


def get_all_currency_data():
    """
    Получает курсы валют из ЦБР за период с января 2003 года по декабрь 2024 года.

    Returns:
        dict: Словарь с курсами валют по месяцам.
    """
    currency_codes = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']
    currency_rates = {}

    tasks = [
        (year, month, currency_codes)
        for year in range(2003, 2025)
        for month in range(1, 13)
        if not (year == 2024 and month == 12)
    ]

    with ThreadPoolExecutor() as executor:
        for key, rates in executor.map(lambda args: fetch_currency_data(*args), tasks):
            currency_rates[key] = rates

    return currency_rates


def calculate_average_salary(row, currency_table):
    """
    Рассчитывает среднюю зарплату на основе данных строки DataFrame.

    Args:
        row (pd.Series): Строка DataFrame с данными о зарплате.
        currency_table (dict): Словарь курсов валют.

    Returns:
        float: Средняя зарплата в рублях или NaN при отсутствии данных.
    """
    salary_from = row['salary_from']
    salary_to = row['salary_to']
    currency = row['salary_currency']
    date = row['data']

    average_salary = (
        (salary_from + salary_to) / 2 if salary_from and salary_to else salary_from or salary_to
    )

    if not average_salary or currency == 'RUR' or not currency:
        return average_salary

    return currency_table.get(date, {}).get(currency, np.nan) * average_salary


def extract_month_year(date):
    """
    Извлекает дату в формате 'YYYY-MM'.

    Args:
        date (str): Полное значение даты.

    Returns:
        str: Дата в формате 'YYYY-MM'.
    """
    return str(date)[:7]


def extract_year(date):
    """
    Извлекает год из строки даты.

    Args:
        date (str): Полное значение даты.

    Returns:
        int: Год.
    """
    return int(str(date)[:4])


def create_html_table(data_frame):
    """
    Создает HTML-таблицу из DataFrame и сохраняет ее в файл.

    Args:
        data_frame (pd.DataFrame): DataFrame с данными для отображения.
    """
    data_frame = data_frame.dropna()

    if 'name' in data_frame.columns:
        data_frame = data_frame.drop(columns=['name'])

    data_frame.columns = ["Расположение", "Средняя зарплата"]
    html_string = data_frame.to_html(
        index=False,
        border=1,
        classes='table table-dark table-bordered table-hover table-sm',
        float_format='{:,.0f}'.format
    )
    html_string = re.sub(r'text-align: right;', 'text-align: center;', html_string)

    with open('salary_by_city.html', 'w', encoding='utf-8') as file:
        file.write(html_string)

    print("[i] HTML таблица успешно создана!")


if __name__ == "__main__":
    data = pd.read_csv("Z:\\vacancies_2024.csv", parse_dates=['published_at'])
    filtered_data = data.copy()

    include_terms = [
        'java', 'ява', 'джава', 'java-программист', 'spring', 'hibernate',
        'struts', 'vaadin', 'micronaut', 'quarkus', 'play framework', 'jhipster',
        'jakarta ee', 'log4j', 'slf4j', 'JPA', 'JDBC', 'jvm'
    ]

    exclude_terms = [
        'javascript', 'node.js', 'typescript', 'angular', 'react', 'vue',
        'c', 'golang', 'go', 'c++', 'assembly', 'rust', 'kotlin', 'groovy', 'scala'
    ]

    filtered_data = filtered_data[
        filtered_data['name'].str.lower().str.contains('|'.join(include_terms), na=False) &
        ~filtered_data['name'].str.lower().str.contains('|'.join(exclude_terms), na=False)
    ]

    filtered_data[['salary_from', 'salary_to']] = filtered_data[['salary_from', 'salary_to']].astype(float)
    filtered_data['data'] = filtered_data['published_at'].apply(extract_month_year)

    currency_data = get_all_currency_data()
    filtered_data['avg_salary'] = filtered_data.apply(lambda row: calculate_average_salary(row, currency_data), axis=1)

    filtered_data = filtered_data[filtered_data['avg_salary'] < 10_000_000]
    filtered_data['year'] = filtered_data['published_at'].apply(extract_year)

    pivot_table = (
        filtered_data
        .pivot_table(
            index='area_name',
            values=['avg_salary', 'name'],
            aggfunc={'avg_salary': 'mean', 'name': 'count'}
        )
        .reset_index()
        .sort_values(by=['name', 'avg_salary'], ascending=False)
        .head(16)
    )

    pivot_table = pivot_table.sort_values(by='avg_salary', ascending=True)
    create_html_table(pivot_table)
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
    plt.barh(pivot_table['area_name'], pivot_table['avg_salary'], color='blue')
    plt.title("Уровень зарплат Java-программиста по городам", color='white')
    plt.xlabel('Средняя зарплата', color='white')
    plt.grid(axis='y', color='white')
    plt.savefig("Уровень зарплат Java-программиста по городам.png", transparent=True, bbox_inches='tight')

