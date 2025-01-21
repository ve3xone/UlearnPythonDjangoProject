import os
import re
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
import ray  # Для работы с modin.pandas
import modin.pandas as pd  # Многопоточная обработка
import numpy as np
import matplotlib.pyplot as plt
import requests


def fetch_currency_data(year, month, currency_codes):
    """
    Получает данные о курсах валют за указанный месяц и год, учитывая номинал.

    Args:
        year (int): Год запроса.
        month (int): Месяц запроса.
        currency_codes (list): Список кодов валют для фильтрации.

    Returns:
        tuple: Ключ в формате 'YYYY-MM' и словарь с курсами валют.
    """
    date_str = f"01/{month:02d}/{year}" # Форматируем дату для запроса
    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={date_str}"

    # Пытаемся получить данные в течение 40 попыток
    for attempt in range(40):
        try:
            response = requests.get(url)
            print(f'{response.status_code} - {url}')
            if response.status_code == 200:
                break
            print(f'[!] Ждем 60 секунд... Неудачный запрос: {response.status_code} - {url}')
            time.sleep(60)
        except Exception as e:
            print(f"Ошибка при запросе: {e}. Попытка {attempt + 1} из 40.")
            time.sleep(60)
    else:
        print(f"Не удалось получить данные за {date_str} после 40 попыток.")
        return f"{year}-{month:02d}", {}

    try:
        root = ET.fromstring(response.content)
        rates = {}
        for item in root.findall('Valute'):
            char_code = item.find('CharCode').text
            if char_code in currency_codes:
                nominal = int(item.find('Nominal').text)
                value = float(item.find('Value').text.replace(',', '.'))
                rates[char_code] = value / nominal
        return f"{year}-{month:02d}", rates
    except Exception as e:
        print(f"Ошибка парсинга данных за {date_str}: {e}")
        return f"{year}-{month:02d}", {}


def fetch_currency_history():
    """
    Получает исторические данные о курсах валют за период с января 2003 года по ноябрь 2024 года.

    Returns:
        dict: Словарь с курсами валют по месяцам.
    """
    currency_codes = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']

    # Генерируем список задач для каждого месяца и года
    tasks = [(year, month, currency_codes) for year in range(2003, 2025)
                                         for month in range(1, 13)
                                         if not (year == 2024 and month == 12)]

    # Используем многопоточность для выполнения запросов
    history = {}
    with ThreadPoolExecutor() as executor:
        for date_key, rates in executor.map(lambda args: fetch_currency_data(*args), tasks):
            history[date_key] = rates

    return history


def calculate_average_salary(row, currency_table):
    """
    Рассчитывает среднюю зарплату в рублях на основе данных строки DataFrame.

    Args:
        row (pd.Series): Строка DataFrame с данными о зарплате.
        currency_table (dict): Словарь курсов валют.

    Returns:
        float: Средняя зарплата в рублях или NaN, если данные отсутствуют.
    """
    salary_from = row['salary_from']  # Минимальная зарплата
    salary_to = row['salary_to']  # Максимальная зарплата
    currency = row['salary_currency']  # Валюта зарплаты
    date = row['data']  # Дата публикации вакансии

    # Рассчитываем среднюю зарплату
    average_salary = (salary_from + salary_to) / 2 if salary_from and salary_to else salary_from or salary_to
    if not average_salary or currency == 'RUR' or not currency:
        return average_salary

    # Конвертируем в рубли, если валюта отличается
    return currency_table.get(date, {}).get(currency, np.nan) * average_salary if date in currency_table else np.nan


def extract_date_prefix(value):
    """
    Извлекает дату в формате 'YYYY-MM'.

    Args:
        value (str): Полное значение даты.

    Returns:
        str: Дата в формате 'YYYY-MM'.
    """
    return str(value)[:7] # Извлекаем первые 7 символов


def extract_year(value):
    """
    Извлекает год из строки даты.

    Args:
        value (str): Полное значение даты.

    Returns:
        int: Год.
    """
    return int(str(value)[:4]) # Извлекаем первые 4 символа


def create_html_table(data_frame):
    """
    Создает HTML-таблицу из DataFrame и сохраняет её в файл.

    Args:
        data_frame (pd.DataFrame): DataFrame для преобразования.

    Returns:
        None
    """
    # Конвертируем DataFrame из Modin в pandas
    if isinstance(data_frame, pd.DataFrame):
        pandas_df = data_frame._to_pandas()
    else:
        pandas_df = data_frame

    pandas_df.columns = ["Город", "Средняя зарплата"]
    pandas_df = pandas_df.dropna() # Убираем строки с NaN

    # Генерируем HTML-код таблицы
    html_string = pandas_df.to_html(
        index=False,
        border=1,
        classes='table table-dark table-bordered table-hover table-sm',
        float_format='{:,.0f}'.format
    )
    html_string = re.sub(r'text-align: right;', 'text-align: center;', html_string)

    # Сохраняем таблицу в файл
    with open('count_by_city.html', 'w', encoding='utf-8') as f:
        f.write(html_string)

    print("[i] HTML таблица успешно создана!")


def process_salary_data(df, currency_table):
    """
    Обрабатывает данные о зарплатах и создает HTML и график распределения вакансий.

    Args:
        df (pd.DataFrame): DataFrame с данными вакансий.
        currency_table (dict): Словарь курсов валют.

    Returns:
        None
    """
    df['data'] = df['published_at'].apply(extract_date_prefix) # Извлекаем месяц и год
    df['average_salary'] = df.apply(lambda row: calculate_average_salary(row, currency_table), axis=1) # Рассчитываем среднюю зарплату
    df = df[df['average_salary'] < 10_000_000] # Убираем аномально высокие значения
    df['year'] = df['published_at'].apply(extract_year) # Извлекаем год

    aggregated_data = df._to_pandas().pivot_table(
        index='area_name',
        values=['average_salary', 'name'],
        aggfunc={'average_salary': 'mean', 'name': 'count'}
    ).reset_index().sort_values(by=['name', 'average_salary'], ascending=False)

    top_cities = aggregated_data[['area_name', 'name']].head(9)
    other_cities_count = aggregated_data['name'].iloc[9:].sum()

    other_city = pd.DataFrame({'area_name': ['Другие'], 'name': [other_cities_count]})

    final_data = pd.concat([top_cities, other_city], axis=0).reset_index(drop=True)
    create_html_table(final_data) # Создаем HTML-таблицу

    # Визуализация данных
    _, ax = plt.subplots(figsize=(15, 13))
    ax.set_facecolor('#25fc3b')
    plt.gcf().set_facecolor('#25fc3b')
    plt.style.use('dark_background')
    plt.pie(final_data['name'], autopct='%1.1f%%', startangle=40, labels=final_data['area_name'])
    plt.title("Доля вакансий по городам", color='white')
    plt.savefig("vacancy_distribution_by_city.png", transparent=True, bbox_inches='tight') # Сохраняем график
    plt.close()


if __name__ == "__main__":
    # Инициализируем движок Modin для многопоточной обработки
    os.environ["MODIN_ENGINE"] = "ray"
    ray.init()

    # Загрузка данных
    dataframe = pd.read_csv("Z:\\vacancies_2024.csv", parse_dates=['published_at'])

    # Обработка данных
    currency_data = fetch_currency_history()
    process_salary_data(dataframe, currency_data)
