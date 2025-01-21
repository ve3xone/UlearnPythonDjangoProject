from datetime import datetime
from typing import Optional, List, Dict, Any
import asyncio
import httpx
from bs4 import BeautifulSoup


def format_date_human_readable(iso_date: str) -> str:
    """
    Преобразует дату из формата ISO 8601 в человеко-читаемый формат на русском языке.

    Аргументы:
        iso_date (str): Дата в формате ISO 8601.

    Возвращает:
        str: Дата в формате 'день месяц годг. часы:минуты:секунды'.
    """
    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
        7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }
    iso_date_corrected = iso_date[:-5] if '+' in iso_date else iso_date
    dt = datetime.strptime(iso_date_corrected, "%Y-%m-%dT%H:%M:%S")
    month = months[dt.month]
    return dt.strftime(f"%d {month} %Yг. %H:%M:%S")


async def fetch_data(client: httpx.AsyncClient, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Выполняет асинхронный GET-запрос для получения данных с указанного URL.

    Аргументы:
        client (httpx.AsyncClient): Клиент для выполнения запросов.
        url (str): URL для запроса.
        params (Optional[Dict[str, Any]]): Дополнительные параметры запроса.

    Возвращает:
        Optional[Dict[str, Any]]: JSON-ответ в виде словаря или None, если запрос не удался.
    """
    try:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        print(f"Ошибка запроса: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP ошибка: {e.response.status_code}")
        return None


async def format_salary(salary: Optional[Dict[str, Any]]) -> str:
    """
    Форматирует информацию о зарплате в человеко-читаемую строку.

    Аргументы:
        salary (Optional[Dict[str, Any]]): Данные о зарплате из API.

    Возвращает:
        str: Отформатированная строка зарплаты или сообщение по умолчанию, если данные отсутствуют.
    """
    if not salary:
        return "Доход не указан"

    salary_from = salary.get('from')
    salary_to = salary.get('to')
    currency = salary.get('currency', '')

    if salary_from is None and salary_to is not None:
        return f"До {salary_to} {currency}."
    elif salary_from is not None and salary_to is None:
        return f"От {salary_from} {currency}."
    elif salary_from and salary_to:
        return f"От {salary_from} до {salary_to} {currency}"
    return "Доход не указан"


def extract_text_from_html(html: str) -> str:
    """
    Удаляет HTML-теги из предоставленного содержимого HTML.

    Аргументы:
        html (str): Сырой HTML-контент.

    Возвращает:
        str: Обычный текст, извлечённый из HTML.
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()


def format_skills(skills: List[Dict[str, Any]]) -> str:
    """
    Форматирует список навыков в строку, разделённую запятыми.

    Аргументы:
        skills (List[Dict[str, Any]]): Список словарей с навыками.

    Возвращает:
        str: Отформатированная строка с названиями навыков или сообщение по умолчанию, если навыки отсутствуют.
    """
    if not skills:
        return 'Навыки не указаны'
    return ', '.join(skill['name'] for skill in skills)


async def fetch_vacancy_details(client: httpx.AsyncClient, vacancy_url: str) -> Dict[str, str]:
    """
    Получает подробную информацию о вакансии.

    Аргументы:
        client (httpx.AsyncClient): Клиент для выполнения запросов.
        vacancy_url (str): URL вакансии.

    Возвращает:
        Dict[str, str]: Словарь с описанием и навыками вакансии.
    """
    details = await fetch_data(client, vacancy_url)
    if details:
        return {
            'description': extract_text_from_html(details.get('description', 'Описание отсутствует')),
            'skills': format_skills(details.get('key_skills', []))
        }
    return {'description': '', 'skills': ''}


async def get_vacancies(profession: str) -> List[Dict[str, Any]]:
    """
    Получает список вакансий для заданной профессии.

    Аргументы:
        profession (str): Профессия для поиска.

    Возвращает:
        List[Dict[str, Any]]: Список деталей вакансий.
    """
    params = {
        'text': profession,
        'period': 1,
        'per_page': 10,
        'search_field': 'name',
        'page': 0,
        'order_by': 'publication_time'
    }

    async with httpx.AsyncClient() as client:
        vacancies_data = await fetch_data(client, 'https://api.hh.ru/vacancies', params=params)

        if not vacancies_data:
            return []

        tasks = []
        results = []

        for vacancy in vacancies_data.get('items', []):
            vacancy_info = {
                'id': vacancy['id'],
                'title': vacancy['name'],
                'company': vacancy['employer']['name'],
                'salary_info': await format_salary(vacancy['salary']),
                'region': vacancy['area']['name'],
                'published_at': format_date_human_readable(vacancy['published_at']),
                'description': '',
                'skills': ''
            }
            tasks.append(fetch_vacancy_details(client, vacancy['url']))
            results.append(vacancy_info)

        details_list = await asyncio.gather(*tasks)

        for vacancy_info, details in zip(results, details_list):
            vacancy_info.update(details)

        return results
