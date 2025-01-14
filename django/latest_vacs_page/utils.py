import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import Optional, List, Dict, Any


def format_iso_date(date_str: str) -> str:
    """
    Исправляет формат даты ISO 8601, добавляя двоеточие в зону времени.

    Аргументы:
        date_str (str): Строка с датой в формате ISO.

    Возвращает:
        str: Отформатированная строка даты ISO.
    """
    return date_str[:-5] + ':' + date_str[-5:]


async def fetch_data(session: aiohttp.ClientSession, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Выполняет асинхронный GET-запрос для получения данных с указанного URL.

    Аргументы:
        session (aiohttp.ClientSession): Сессия для выполнения запросов.
        url (str): URL для запроса.
        params (Optional[Dict[str, Any]]): Дополнительные параметры запроса.

    Возвращает:
        Optional[Dict[str, Any]]: JSON-ответ в виде словаря или None, если запрос не удался.
    """
    async with session.get(url, params=params) as response:
        if response.status != 200:
            print(f"Ошибка запроса: {response.status}")
            return None
        return await response.json()


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


async def fetch_vacancy_details(session: aiohttp.ClientSession, vacancy_url: str) -> Dict[str, str]:
    """
    Получает подробную информацию о вакансии.

    Аргументы:
        session (aiohttp.ClientSession): Сессия для выполнения запросов.
        vacancy_url (str): URL вакансии.

    Возвращает:
        Dict[str, str]: Словарь с описанием и навыками вакансии.
    """
    details = await fetch_data(session, vacancy_url)
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

    async with aiohttp.ClientSession() as session:
        vacancies_data = await fetch_data(session, 'https://api.hh.ru/vacancies', params=params)

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
                'published_at': vacancy['published_at'],
                'description': '',
                'skills': ''
            }
            tasks.append(fetch_vacancy_details(session, vacancy['url']))
            results.append(vacancy_info)

        details_list = await asyncio.gather(*tasks)

        for vacancy_info, details in zip(results, details_list):
            vacancy_info.update(details)

        return results