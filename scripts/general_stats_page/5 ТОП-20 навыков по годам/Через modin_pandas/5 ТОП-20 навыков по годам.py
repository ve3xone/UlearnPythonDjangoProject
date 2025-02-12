import os
import re
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from itertools import islice
import ray # Нужно для работы modin.pandas
import modin.pandas as pd # Многопоток #3 minutes and 24 seconds
import numpy as np
import matplotlib.pyplot as plt
import requests


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

    # Генерируем список задач для каждого месяца и года
    tasks = [(year, month, currencies) for year in range(2003, 2025)
                                       for month in range(1, 13)
                                       if not (year == 2024 and month == 12)]

    # Используем многопоточность для выполнения запросов
    result = {}
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
    salary_from = row['salary_from']  # Минимальная зарплата
    salary_to = row['salary_to']  # Максимальная зарплата
    currency = row['salary_currency']  # Валюта зарплаты
    date = row['data']  # Дата публикации вакансии

    # Рассчитываем среднюю зарплату
    res = (salary_from + salary_to) / 2 if salary_from and salary_to else salary_from or salary_to
    if not res or currency == 'RUR' or not currency:
        return res

    # Конвертируем в рубли, если валюта отличается
    return table_curr.get(date, {}).get(currency, np.nan) * res if date in table_curr else np.nan


def extract(value):
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


def create_html_table(yearly_count, year):
    """
    Создает HTML-таблицу на основе данных о зарплатах по годам.

    Args:
        yearly_count (pd.DataFrame): DataFrame с данными о средней зарплате по годам.
        year: Какой год.

    Returns:
        None
    """
    # Преобразуем DataFrame Modin в Pandas только для вызова to_html
    if isinstance(yearly_count, pd.DataFrame):
        pandas_df = yearly_count._to_pandas()  # Конвертируем в Pandas DataFrame
    else:
        pandas_df = yearly_count  # Если это уже Pandas, используем его напрямую

    # Сброс индекса и корректное именование столбцов
    pandas_df.columns = ["Навык", "Частота"]  # Устанавливаем названия столбцов

    # Удаляем строки с пропущенными значениями
    pandas_df = pandas_df.dropna()

    # Сортируем по убыванию значений в столбце "Частота"
    pandas_df = pandas_df.sort_values(by="Частота", ascending=False)

    # Создаем HTML-таблицу с использованием Pandas
    html_string = pandas_df.to_html(
        index=False,  # Отключаем индекс в HTML
        border=1,
        classes='table table-dark table-bordered table-hover table-sm',
        float_format='{:,.0f}'.format  # Форматирование чисел
    )

    # Заменяем text-align: right; на text-align: center;
    html_string = re.sub(r'text-align: right;', 'text-align: center;', html_string)

    with open(f'top-20-vacs-{year}.html', 'w', encoding='utf-8') as f:
        f.write(html_string)

    print("[i] HTML таблица успешно создана!")


def top_skills(year, df):
    """
    Анализирует и визуализирует топ-20 наиболее востребованных навыков за указанный год.

    Args:
        year (int): Год, за который нужно проанализировать данные.
        df (pd.DataFrame): DataFrame с данными о вакансиях. Ожидаются следующие столбцы:
            - 'year': Год публикации вакансии.
            - 'key_skills': Навыки, указанные в вакансиях.

    Returns:
        None: Создает HTML-таблицу и сохраняет график в формате PNG с топ-20 навыков.
    """
    all_skills = df[(df['year'] == year) & (df['key_skills'].notna())]
    all_skills = all_skills['key_skills'].str.cat(sep='\n').split('\n')
    skill_frequency = Counter(all_skills)

    sorted_dict_desc = dict(sorted(skill_frequency.items(), key=lambda item: item[1], reverse=True))
    first_20_pairs = dict(islice(sorted_dict_desc.items(), 20))

    skills_frame = pd.DataFrame.from_dict(first_20_pairs, orient='index').reset_index()
    skills_frame.columns = ['skill', 'freq']
    skills_frame = skills_frame.sort_values(by='freq')
    skills_frame_rename = skills_frame.rename(columns={'skill': 'Навык', 'freq': 'Частота'})
    skills_frame_rename = skills_frame_rename.reset_index(drop=True)
    skills_frame_rename.index = skills_frame_rename.index + 1
    create_html_table(skills_frame_rename, year=year)

    _, ax = plt.subplots(figsize=(17, 13))
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
    plt.barh(skills_frame['skill'], skills_frame['freq'], color='blue')
    plt.xticks(rotation=45,color='white', fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid(axis='y',color='white')
    plt.savefig("ТОП-20 навыков по " + str(year) + " году.png", transparent=True, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    # Инициализируем движок Modin для многопоточной обработки
    os.environ["MODIN_ENGINE"] = "ray"
    ray.init()

    # Почему лучшее использовать modin.pandas?
    # Потому что read_csv у pandas занимает 5 мин 30 сек
    # А у modin.pandas всего 50 сек

    # Читаем данные из CSV-файла
    dataframe = pd.read_csv("Z:\\vacancies_2024.csv", parse_dates=['published_at']) #Использую RAMDISK
    tab_curr = get_all_currency() # Получаем курсы валют
    df_copy = dataframe.copy()
    df_copy['data'] = df_copy['published_at'].apply(extract)
    df_copy['avg_salary'] = df_copy.apply(lambda row: avg_salary(row, tab_curr), axis=1)
    df_copy = df_copy[df_copy['avg_salary'] < 10_000_000]
    df_copy['year'] = df_copy['published_at'].apply(extract_year)

    # Обрабатываем данные и создаем визуализации
    for i in range(2015, 2025):
        top_skills(i, df=df_copy)
