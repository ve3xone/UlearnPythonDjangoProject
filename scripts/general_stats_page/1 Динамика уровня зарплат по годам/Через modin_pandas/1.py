# Импортируем необходимые библиотеки для работы с данными, многопоточности и визуализации
import os
import ray  # Для работы modin.pandas
import modin.pandas as pd  # Многопоточная обработка данных
import re
import numpy as np
import matplotlib.pyplot as plt
import requests
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor


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
    date_str = f"01/{month:02d}/{year}"  # Форматируем дату для запроса
    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={date_str}"  # URL для получения данных

    # Пытаемся получить данные в течение 40 попыток
    for attempt in range(40):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break  # Прерываем цикл, если запрос успешен
            print(f"[!] Ждем 60 сек... попытка {attempt + 1}: {response.status_code}")
            time.sleep(60)  # Ждем 60 секунд перед следующей попыткой
        except requests.RequestException as e:
            print(f"Ошибка запроса: {e}. Попытка {attempt + 1} из 40.")
            time.sleep(60)
    else:
        print(f"Не удалось получить данные после 40 попыток: {url}")
        return f"{year}-{month:02d}", {}

    # Парсим XML-ответ и извлекаем курсы валют
    try:
        root = ET.fromstring(response.content)
        result = {}
        for item in root.findall('Valute'):
            char_code = item.find('CharCode').text  # Код валюты
            if char_code in target_currencies:
                nominal = int(item.find('Nominal').text)  # Номинал валюты
                value = float(item.find('Value').text.replace(',', '.'))  # Курс валюты
                result[char_code] = value / nominal  # Рассчитываем курс с учетом номинала
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
    # Генерируем список задач для каждого месяца и года
    tasks = [(year, month, target_currencies) for year in range(2003, 2025) 
             for month in range(1, 13) if not (year == 2024 and month == 12)]

    results = {}
    # Используем многопоточность для выполнения запросов
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
    salary_from = row['salary_from']  # Минимальная зарплата
    salary_to = row['salary_to']  # Максимальная зарплата
    currency = row['salary_currency']  # Валюта зарплаты
    date = row['date']  # Дата публикации вакансии

    # Рассчитываем среднюю зарплату
    avg_salary = (salary_from + salary_to) / 2 if salary_from and salary_to else salary_from or salary_to
    if not avg_salary or currency == 'RUR' or not currency:
        return avg_salary

    # Конвертируем в рубли, если валюта отличается
    return currency_rates.get(date, {}).get(currency, np.nan) * avg_salary if date in currency_rates else np.nan


def extract_month_year(date_value):
    """
    Извлекает дату в формате 'YYYY-MM'.

    Args:
        date_value (str): Полное значение даты.

    Returns:
        str: Дата в формате 'YYYY-MM'.
    """
    return str(date_value)[:7]  # Извлекаем первые 7 символов


def extract_year(date_value):
    """
    Извлекает год из строки даты.

    Args:
        date_value (str): Полное значение даты.

    Returns:
        int: Год.
    """
    return int(str(date_value)[:4])  # Извлекаем первые 4 символа


def create_html_table(df):
    """
    Создает HTML-таблицу на основе данных о зарплатах по годам.

    Args:
        df (pd.DataFrame): DataFrame с данными о средней зарплате по годам.

    Returns:
        None
    """
    pandas_df = df._to_pandas()  # Конвертируем DataFrame из Modin в pandas
    pandas_df.columns = ["Год", "Средняя зарплата"]
    pandas_df = pandas_df.dropna()  # Убираем строки с NaN

    # Генерируем HTML-код таблицы
    html_content = pandas_df.to_html(
        index=False,
        border=1,
        classes='table table-dark table-bordered table-hover table-sm',
        float_format='{:,.0f}'.format
    )
    html_content = re.sub(r'text-align: right;', 'text-align: center;', html_content)

    # Сохраняем таблицу в файл
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
    df['date'] = df['published_at'].apply(extract_month_year)  # Извлекаем месяц и год
    df['avg_salary'] = df.apply(lambda row: calculate_avg_salary(row, currency_rates), axis=1)  # Рассчитываем среднюю зарплату
    df = df[df['avg_salary'] < 10_000_000]  # Убираем аномально высокие значения
    df['year'] = df['published_at'].apply(extract_year)  # Извлекаем год

    # Создаем сводную таблицу
    salary_pivot = df.pivot_table(index='year', values='avg_salary').reset_index()
    salary_pivot['avg_salary'] = salary_pivot['avg_salary'].astype(int)

    create_html_table(salary_pivot)  # Создаем HTML-таблицу

    # Визуализация данных
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='none')
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
    plt.savefig("salary_trends.png", transparent=True, bbox_inches='tight')  # Сохраняем график
    plt.close()


if __name__ == "__main__":
    # Инициализируем движок Modin для многопоточной обработки
    os.environ["MODIN_ENGINE"] = "ray"
    ray.init()

    # Читаем данные из CSV-файла
    df = pd.read_csv("Z:\\vacancies_2024.csv", parse_dates=['published_at'])
    currency_rates = get_currency_rates()  # Получаем курсы валют
    process_salary_data(df, currency_rates)  # Обрабатываем данные и создаем визуализации
