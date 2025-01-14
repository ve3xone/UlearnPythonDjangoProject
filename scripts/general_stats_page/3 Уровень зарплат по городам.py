
import os
import ray # Нужно для работы modin.pandas
import modin.pandas as pd # Многопоток #3 minutes and 24 seconds
# import pandas as pd # Однопоток
import numpy as np
import re
import matplotlib.pyplot as plt
import requests
import time
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

def create_html_table(pandas_df):
    # Группировка по 'area_name' с расчетом средней зарплаты
    pandas_df = pandas_df.groupby('area_name', as_index=False)['avg_salary'].mean()

    # Сортировка по средней зарплате в порядке убывания
    pandas_df = pandas_df.sort_values(by='avg_salary', ascending=False)

    # Сброс индекса и корректное именование столбцов
    # pandas_df = pandas_df.reset_index()  # Преобразуем индекс в столбец
    pandas_df.columns = ["Расположение", "Средняя Зарплата"]  # Устанавливаем названия столбцов

    # Удаляем строки с пропущенными значениями
    pandas_df = pandas_df.dropna()

    # Создаем HTML-таблицу с использованием Pandas
    html_string = pandas_df.to_html(
        index=False,  # Отключаем индекс в HTML
        border=1,
        classes='dataframe table table-dark',
        float_format='{:,.0f}'.format  # Форматирование чисел
    )

    # Заменяем text-align: right; на text-align: center;
    html_string = re.sub(r'text-align: right;', 'text-align: center;', html_string)

    with open('salary_by_city.html', 'w', encoding='utf-8') as f:
        f.write(html_string)

    print("[i] HTML таблица успешно создана!")

def process_salary_data(df, table_curr):
    """
    Обрабатывает данные о зарплатах и строит html и график динамики зарплат.

    Args:
        df (pd.DataFrame): DataFrame с данными вакансий.
        table_curr (dict): Словарь курсов валют.

    Returns:
        None
    """
    df_copy = df.copy()
    df_copy['data'] = df_copy['published_at'].apply(extract)
    df_copy['avg_salary'] = df_copy.apply(lambda row: avg_salary(row, table_curr), axis=1)
    df_copy = df_copy[df_copy['avg_salary'] < 10_000_000]
    df_copy['year'] = df_copy['published_at'].apply(extract_year)

    pandas_df = df_copy._to_pandas()
    
    # Общее количество вакансий
    total_vacancies = pandas_df['name'].count()

    # Подсчет количества вакансий по городам
    city_vacancy_counts = pandas_df['area_name'].value_counts()

    # Определение значимых городов (где доля вакансий > 1%)
    sign_cities = city_vacancy_counts[city_vacancy_counts > total_vacancies * 0.01].index

    # Фильтрация DataFrame по значимым городам
    filtered_df = pandas_df[pandas_df['area_name'].isin(sign_cities)]

    pd_df_copy_salary_level = filtered_df.pivot_table(
        index='area_name', 
        values=['avg_salary', 'name'], 
        aggfunc={'avg_salary':'mean', 'name':'count'}
    ).reset_index().sort_values(by=["name",'avg_salary'], ascending=False).head(16)

    pd_df_copy_salary_level = pd_df_copy_salary_level[
        ['area_name', 'avg_salary']
    ].sort_values(by='avg_salary', ascending=True)
    # pd_df_copy_salary_level = pd_df_copy_salary_level.groupby('area_name').sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='none')
    ax.set_facecolor('#25fc3b')
    plt.gcf().set_facecolor('#25fc3b')
    plt.style.use('dark_background')

    # делаем рамку белой
    for spine in ax.spines.values():
        spine.set_edgecolor('white')  # Цвет рамки
        spine.set_linewidth(1)  # Толщина рамки (можно уменьшить)

    # Настройка цвета и толщины тиков (меток осей)
    ax.tick_params(axis='both', colors='white', width=1)

    plt.title("Уровень зарплат по городам, где доля вакансий больше 1 % всех вакансий", color='white')
    plt.barh(pd_df_copy_salary_level['area_name'], pd_df_copy_salary_level['avg_salary'], color='blue')
    plt.xlabel("Средняя зарплата", color='white')
    plt.xticks(color='white')
    # plt.ylabel(color='white')
    plt.yticks(color='white')
    # plt.legend(fontsize=14, facecolor='none', edgecolor='white')
    plt.grid(axis='y', color='white')
    plt.savefig("Уровень зарплат по городам, где доля вакансий больше 1 % всех вакансий.png", transparent=True, bbox_inches='tight')
    plt.close()
    create_html_table(pd_df_copy_salary_level)

# Нужно для работы modin.pandas
os.environ["MODIN_ENGINE"] = "ray"
ray.init()

df = pd.read_csv("Z:\\vacancies_2024.csv", parse_dates=['published_at']) #Использую RAMDISK
table_curr = get_all_currency()
process_salary_data(df, table_curr)
# df_full = df.copy()
# df_full['data'] = df_full['published_at'].apply(extract)
# df_full['avg_salary'] = df_full.apply(avg_salary,axis=1)
# df_full = df_full[df_full['avg_salary'] < 10_000_000]
# df_full.shape
# df_full['year'] = df_full['published_at'].apply(extract_year)
# df_full_salary_level = df_full._to_pandas().pivot_table(index='area_name', values=['avg_salary', 'name'], aggfunc={'avg_salary':'mean', 'name':'count'}).reset_index().sort_values(by=["name",'avg_salary'], ascending=False).head(16)
# df_full_salary_level = df_full_salary_level[['area_name', 'avg_salary']]
# # df_full_salary_level.rename(columns={'area_name': 'Расположение', 'avg_salary': 'Средняя Зарплата'}, inplace=True)
# # df_full_salary_level
# df_full_salary_level_for_save = df_full_salary_level
# df_full_salary_level_for_save.to_csv("Уровень зарплат по городам")
# df_full_salary_level = df_full_salary_level.sort_values(by='avg_salary', ascending=True)
# fig, ax = plt.subplots(figsize=(12, 7))
# ax.set_facecolor('#F1F1F1')
# plt.gcf().set_facecolor('#F1F1F1')
# plt.barh(df_full_salary_level['area_name'], df_full_salary_level['avg_salary'])
# plt.title("Уровень зарплат по городам, где доля вакансий больше 1 % всех вакансий")
# plt.xlabel('Средняя зарплата')
# plt.grid(axis='y')
# plt.savefig("Уровень зарплат по городам, где доля вакансий больше 1 % всех вакансий.png");
