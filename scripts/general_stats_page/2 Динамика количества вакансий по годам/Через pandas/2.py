import pandas as pd
import re
import matplotlib.pyplot as plt


def extract_date(value):
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


def save_html_table(pandas_df):
    """
    Создает HTML-таблицу из DataFrame и сохраняет её в файл.

    Args:
        pandas_df (pd.DataFrame): DataFrame с данными для таблицы.

    Returns:
        None
    """
    pandas_df = pandas_df.reset_index()  # Преобразуем индекс в столбец
    pandas_df.columns = ["Год", "Количество вакансий"]  # Устанавливаем названия столбцов
    pandas_df = pandas_df.dropna()  # Удаляем строки с пропущенными значениями

    html_content = pandas_df.to_html(
        index=False,
        border=1,
        classes='table table-dark table-bordered table-hover table-sm',
        float_format='{:,.0f}'.format
    )
    html_content = re.sub(r'text-align: right;', 'text-align: center;', html_content)

    with open('count_by_year.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print("[i] HTML таблица успешно создана!")


def process_vacancy_data(dataframe):
    """
    Обрабатывает данные о вакансиях, создаёт HTML-таблицу и график динамики вакансий по годам.

    Args:
        dataframe (pd.DataFrame): DataFrame с данными вакансий.

    Returns:
        None
    """
    df_copy = dataframe.copy()
    df_copy['date'] = df_copy['published_at'].apply(extract_date)
    df_copy['year'] = df_copy['published_at'].apply(extract_year)
    df_copy = df_copy[["name", "area_name", "year"]]

    vacancy_count_by_year = df_copy.pivot_table(index='year', values='name', aggfunc='count')
    save_html_table(vacancy_count_by_year)

    vacancy_count_by_year = vacancy_count_by_year.reset_index()

    fig, ax = plt.subplots(figsize=(15, 10), facecolor='none')
    ax.set_facecolor('#25fc3b')
    plt.gcf().set_facecolor('#25fc3b')
    plt.style.use('dark_background')

    for spine in ax.spines.values():
        spine.set_edgecolor('white')
        spine.set_linewidth(1)

    ax.tick_params(axis='both', colors='white', width=1)

    plt.title("Динамика количества вакансий по годам", color='white')
    plt.bar(vacancy_count_by_year['year'], vacancy_count_by_year['name'], color='blue')
    plt.plot(vacancy_count_by_year['year'], vacancy_count_by_year['name'], color='red', marker='o')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.grid(axis='y', color='white')

    plt.savefig("vacancy_trend_by_year.png", transparent=True, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    # Загружаем данные
    file_path = "Z:\\vacancies_2024.csv"
    df = pd.read_csv(file_path, parse_dates=['published_at'])

    process_vacancy_data(df)
