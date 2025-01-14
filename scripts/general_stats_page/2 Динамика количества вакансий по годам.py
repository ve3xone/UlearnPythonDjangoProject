
import os
import ray # Нужно для работы modin.pandas
import modin.pandas as pd # Многопоток #3 minutes and 24 seconds
#import pandas as pd # Однопоток
import re
import matplotlib.pyplot as plt

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

def create_html_table(yearly_count):
    # Преобразуем DataFrame Modin в Pandas только для вызова to_html
    if isinstance(yearly_count, pd.DataFrame):
        pandas_df = yearly_count._to_pandas()  # Конвертируем в Pandas DataFrame
    else:
        pandas_df = yearly_count  # Если это уже Pandas, используем его напрямую

    # Сброс индекса и корректное именование столбцов
    pandas_df = pandas_df.reset_index()  # Преобразуем индекс в столбец
    pandas_df.columns = ["Год", "Кол-во вакансий"]  # Устанавливаем названия столбцов

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

    with open('count_by_year.html', 'w', encoding='utf-8') as f:
        f.write(html_string)

    print("[i] HTML таблица успешно создана!")

def process_salary_data(df):
    """
    Обрабатывает данные о зарплатах и строит html и график динамики вакансий.

    Args:
        df (pd.DataFrame): DataFrame с данными вакансий.
        table_curr (dict): Словарь курсов валют.

    Returns:
        None
    """
    df_copy = df.copy()
    df_copy['data'] = df_copy['published_at'].apply(extract)
    # df_copy['avg_salary'] = df_copy.apply(lambda row: avg_salary(row, table_curr), axis=1)
    # df_copy = df_copy[df_copy['avg_salary'] < 10_000_000]
    df_copy['year'] = df_copy['published_at'].apply(extract_year)
    df_copy = df_copy[["name", "area_name",'year']].copy()
    df_copy_count_pivot = df_copy.pivot_table(index='year', values=['name'], aggfunc='count')
    df_copy_count_pivot = df_copy_count_pivot.reset_index()
    df_copy_count_pivot_save = df_copy.pivot_table(index='year', values=['name'], aggfunc='count')
    create_html_table(df_copy_count_pivot_save)

    # figsize=(12, 7),
    fig, ax = plt.subplots(figsize=(15, 10), facecolor='none')
    ax.set_facecolor('#25fc3b')
    plt.gcf().set_facecolor('#25fc3b')
    plt.style.use('dark_background')

    # делаем рамку белой
    for spine in ax.spines.values():
        spine.set_edgecolor('white')  # Цвет рамки
        spine.set_linewidth(1)  # Толщина рамки (можно уменьшить)

    # Настройка цвета и толщины тиков (меток осей)
    ax.tick_params(axis='both', colors='white', width=1)

    plt.title("Динамика количества вакансий по годам", color='white')
    plt.bar(df_copy_count_pivot['year'],df_copy_count_pivot['name'], color='blue')
    plt.plot(df_copy_count_pivot['year'], df_copy_count_pivot['name'], color='red', marker='o')
    # plt.xlabel("Год", color='white')
    plt.xticks(color='white')
    # plt.ylabel("Средняя зарплата", color='white')
    plt.yticks(color='white')
    # plt.legend(fontsize=14, facecolor='none', edgecolor='white')
    plt.grid(axis='y', color='white')
    plt.savefig("Динамика количества вакансий по годам.png", transparent=True, bbox_inches='tight')
    plt.close()

# Нужно для работы modin.pandas
os.environ["MODIN_ENGINE"] = "ray"
ray.init()

# Почему лучшее использовать modin.pandas?
# Потому что read_csv у pandas занимает 5 мин 30 сек
# А у modin.pandas всего 50 сек
df = pd.read_csv("Z:\\vacancies_2024.csv", parse_dates=['published_at']) #Использую RAMDISK
process_salary_data(df)
