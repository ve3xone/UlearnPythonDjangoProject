import os
import ray
import modin.pandas as pd  # Для многопоточной работы с DataFrame
import numpy as np
import re
import matplotlib.pyplot as plt
import requests
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from itertools import islice

# Инициализация Modin с использованием Ray
os.environ["MODIN_ENGINE"] = "ray"
ray.init()

def fetch_currency_data(year, month, currencies):
    """
    Получает курсы валют за указанный месяц и год, скорректированные по номиналу.

    Аргументы:
        year (int): Год, за который нужны данные.
        month (int): Месяц, за который нужны данные.
        currencies (list): Список кодов валют для фильтрации.

    Возвращает:
        tuple: Ключ в формате 'YYYY-MM' и словарь курсов валют.
    """
    date_str = f"01/{month:02d}/{year}"
    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={date_str}"

    try:
        for attempt in range(40):
            try:
                response = requests.get(url)
                print(f'{response.status_code} - {url}')
                if response.status_code == 200:
                    break
                print(f'[!] Повтор через 60 секунд из-за статуса: {response.status_code}')
                time.sleep(60)
            except Exception:
                print(f"Ошибка запроса. Попытка {attempt + 1} из 40. ({url})")
                time.sleep(60)

        # Парсинг XML-данных
        root = ET.fromstring(response.content)
        rates = {}
        for item in root.findall('Valute'):
            char_code = item.find('CharCode').text
            if char_code in currencies:
                nominal = int(item.find('Nominal').text)
                value = float(item.find('Value').text.replace(',', '.'))
                rates[char_code] = value / nominal

        return f"{year}-{month:02d}", rates

    except Exception as e:
        print(f"Ошибка при получении данных за {date_str}: {e}")
        return f"{year}-{month:02d}", {}

def fetch_all_currencies():
    """
    Получает курсы валют за период с января 2003 года по ноябрь 2024 года.

    Возвращает:
        dict: Словарь с курсами валют по месяцам.
    """
    currencies = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']
    tasks = [(year, month, currencies) for year in range(2003, 2025)
             for month in range(1, 13) if not (year == 2024 and month == 12)]
    results = {}

    with ThreadPoolExecutor() as executor:
        for key, data in executor.map(lambda args: fetch_currency_data(*args), tasks):
            results[key] = data

    return results

def calculate_average_salary(row, currency_rates):
    """
    Рассчитывает среднюю зарплату на основе данных строки и курсов валют.

    Аргументы:
        row (pd.Series): Строка DataFrame с данными о зарплате.
        currency_rates (dict): Словарь курсов валют.

    Возвращает:
        float: Средняя зарплата в рублях или NaN, если данных недостаточно.
    """
    salary_from = row['salary_from']
    salary_to = row['salary_to']
    currency = row['salary_currency']
    date = row['data']

    salary = (salary_from + salary_to) / 2 if salary_from and salary_to else salary_from or salary_to
    if not salary or currency == 'RUR' or not currency:
        return salary

    return currency_rates.get(date, {}).get(currency, np.nan) * salary if date in currency_rates else np.nan

def extract_year_month(value):
    """
    Извлекает дату в формате 'YYYY-MM'.

    Аргументы:
        value (str): Полная строка даты.

    Возвращает:
        str: Дата в формате 'YYYY-MM'.
    """
    return str(value)[:7]

def extract_year(value):
    """
    Извлекает год из строки даты.

    Аргументы:
        value (str): Полная строка даты.

    Возвращает:
        int: Извлеченный год.
    """
    return int(str(value)[:4])

def create_html_table(dataframe, year):
    """
    Создает HTML-таблицу из DataFrame и сохраняет её в файл.

    Аргументы:
        dataframe (pd.DataFrame): DataFrame с данными для конвертации в HTML.
        year (int): Год, для которого создаётся таблица.
    """
    if isinstance(dataframe, pd.DataFrame):
        dataframe = dataframe._to_pandas()

    dataframe.columns = ["Навык", "Частота"]
    dataframe = dataframe.dropna()
    html_content = dataframe.to_html(index=False, border=1,
                                      classes='table table-dark table-bordered table-hover table-sm',
                                      float_format='{:,.0f}'.format)
    html_content = re.sub(r'text-align: right;', 'text-align: center;', html_content)

    with open(f'top-20-skills-{year}.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"[i] HTML-таблица для {year} успешно создана!")

def generate_top_skills(year, dataframe):
    """
    Определяет и визуализирует топ-20 навыков за указанный год.

    Аргументы:
        year (int): Год для анализа навыков.
        dataframe (pd.DataFrame): DataFrame с данными о навыках.
    """
    skills_data = dataframe[(dataframe['year'] == year) & dataframe['key_skills'].notna()]
    skills = skills_data['key_skills'].str.cat(sep='\n').split('\n')
    skill_counts = Counter(skills)
    top_skills = dict(islice(sorted(skill_counts.items(), key=lambda item: item[1], reverse=True), 20))

    skills_df = pd.DataFrame.from_dict(top_skills, orient='index').reset_index()
    skills_df.columns = ['Навык', 'Частота']
    skills_df = skills_df.sort_values(by='Частота').reset_index(drop=True)
    create_html_table(skills_df, year=year)

    fig, ax = plt.subplots(figsize=(17, 13))
    plt.title(f"ТОП-20 навыков по {year} году", color='white', fontsize=24)
    ax.set_facecolor('#25fc3b')
    plt.gcf().set_facecolor('#25fc3b')
    plt.style.use('dark_background')
    
    # делаем рамку белой
    for spine in ax.spines.values():
        spine.set_edgecolor('white')  # Цвет рамки
        spine.set_linewidth(1)  # Толщина рамки (можно уменьшить)

    # Настройка цвета и толщины тиков (меток осей)
    ax.tick_params(axis='both', colors='white', width=1)
    plt.barh(skills_df['Навык'], skills_df['Частота'], color='blue')
    plt.xticks(rotation=45,color='white', fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid(axis='y',color='white')
    plt.savefig("ТОП-20 навыков по " + str(year) + " году.png", transparent=True, bbox_inches='tight')
    plt.close()

# Загрузка и обработка данных
df = pd.read_csv("Z:\\vacancies_2024.csv", parse_dates=['published_at'])
currency_rates = fetch_all_currencies()

# Подготовка данных
df['data'] = df['published_at'].apply(extract_year_month)
df['avg_salary'] = df.apply(lambda row: calculate_average_salary(row, currency_rates), axis=1)
df = df[df['avg_salary'] < 10_000_000]
df['year'] = df['published_at'].apply(extract_year)

# Генерация отчетов для каждого года
for year in range(2015, 2025):
    generate_top_skills(year, dataframe=df)
