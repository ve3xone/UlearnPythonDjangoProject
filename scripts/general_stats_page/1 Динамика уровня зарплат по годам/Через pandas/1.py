import re
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def fetch_currency_data(year, month, target_currencies):
    """
    Получает данные о курсе валют за указанный месяц и год.

    Args:
        year (int): Год запроса.
        month (int): Месяц запроса.
        target_currencies (list): Список кодов валют для фильтрации.

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
            print(f"[!] Ждем 60 сек... попытка {attempt + 1}: {response.status_code}")
            time.sleep(60)
        except requests.RequestException as e:
            print(f"Ошибка запроса: {e}. Попытка {attempt + 1} из 40.")
            time.sleep(60)
    else:
        print(f"Не удалось получить данные после 40 попыток: {url}")
        return f"{year}-{month:02d}", {}

    try:
        root = ET.fromstring(response.content)
        result = {}
        for item in root.findall('Valute'):
            char_code = item.find('CharCode').text
            if char_code in target_currencies:
                nominal = int(item.find('Nominal').text)
                value = float(item.find('Value').text.replace(',', '.'))
                result[char_code] = value / nominal
        return f"{year}-{month:02d}", result
    except ET.ParseError as e:
        print(f"Ошибка парсинга XML: {e}")
        return f"{year}-{month:02d}", {}


def get_currency_rates():
    """
    Получает курсы валют за период с января 2003 года по декабрь 2024 года.

    Returns:
        dict: Словарь с курсами валют по месяцам.
    """
    target_currencies = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']
    tasks = [(year, month, target_currencies) for year in range(2003, 2025)
             for month in range(1, 13) if not (year == 2024 and month == 12)]

    results = {}
    with ThreadPoolExecutor() as executor:
        for key, rates in executor.map(lambda args: fetch_currency_data(*args), tasks):
            results[key] = rates

    return results


def calculate_avg_salary(row, currency_rates):
    """
    Рассчитывает среднюю зарплату на основе данных о вакансии.

    Args:
        row (pd.Series): Строка DataFrame с данными о зарплате.
        currency_rates (dict): Словарь курсов валют.

    Returns:
        float: Средняя зарплата в рублях или NaN, если данные отсутствуют.
    """
    salary_from = row['salary_from']
    salary_to = row['salary_to']
    currency = row['salary_currency']
    date = row['date']

    avg_salary = (salary_from + salary_to) / 2 if salary_from and salary_to else salary_from or salary_to
    if not avg_salary or currency == 'RUR' or not currency:
        return avg_salary

    return currency_rates.get(date, {}).get(currency, np.nan) * avg_salary if date in currency_rates else np.nan


def extract_month_year(date_value):
    """
    Извлекает дату в формате 'YYYY-MM'.

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


def create_html_table(pandas_df):
    """
    Создает HTML-таблицу на основе данных о зарплатах по годам.

    Args:
        pandas_df (pd.DataFrame): DataFrame с данными о средней зарплате по годам.

    Returns:
        None
    """
    pandas_df.columns = ["Год", "Средняя зарплата"]
    pandas_df = pandas_df.dropna()

    html_content = pandas_df.to_html(
        index=False,
        border=1,
        classes='table table-dark table-bordered table-hover table-sm',
        float_format='{:,.0f}'.format
    )
    html_content = re.sub(r'text-align: right;', 'text-align: center;', html_content)

    with open('salary_by_year.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print("[i] HTML таблица успешно создана!")


def process_salary_data(df, currency_rates):
    """
    Обрабатывает данные о зарплатах и создает визуализацию и HTML-таблицу.

    Args:
        df (pd.DataFrame): DataFrame с данными о вакансиях.
        currency_rates (dict): Словарь курсов валют.

    Returns:
        None
    """
    df['date'] = df['published_at'].apply(extract_month_year)
    df['avg_salary'] = df.apply(lambda row: calculate_avg_salary(row, currency_rates), axis=1)
    df = df[df['avg_salary'] < 10_000_000]
    df['year'] = df['published_at'].apply(extract_year)

    salary_pivot = df.pivot_table(index='year', values='avg_salary').reset_index()
    salary_pivot['avg_salary'] = salary_pivot['avg_salary'].astype(int)

    create_html_table(salary_pivot)

    _, ax = plt.subplots(figsize=(14, 10), facecolor='none')
    ax.set_facecolor('#25fc3b')
    plt.gcf().set_facecolor('#25fc3b')
    plt.style.use('dark_background')

    # делаем рамку белой
    for spine in ax.spines.values():
        spine.set_edgecolor('white')  # Цвет рамки
        spine.set_linewidth(1)  # Толщина рамки (можно уменьшить)

    # Настройка цвета и толщины тиков (меток осей)
    ax.tick_params(axis='both', colors='white', width=1)

    plt.title("Динамика уровня зарплат по годам", color='white', fontsize=24)
    plt.bar(salary_pivot['year'], salary_pivot['avg_salary'], color='blue')
    plt.plot(salary_pivot['year'], salary_pivot['avg_salary'], color='red', marker='o')
    plt.xlabel("Год", color='white', fontsize=14)
    plt.xticks(color='white')
    plt.ylabel("Средняя зарплата", color='white', fontsize=14)
    plt.yticks(color='white')
    plt.grid(axis='y', color='white')
    plt.savefig("salary_trends.png", transparent=True, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    dataframe = pd.read_csv("Z:\\vacancies_2024.csv", parse_dates=['published_at'])
    curr_rates = get_currency_rates()
    process_salary_data(dataframe, curr_rates)
