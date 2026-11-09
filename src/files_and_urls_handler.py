"""Функции чтения текста из локальных файлов.

Пока работу с url никак не проверял, но в теории оно работает
"""
import requests
from pathlib import Path
from typing import List

from src.date_regex import find_dates


def read_text_from_url(url: str) -> str:
    """Загружает страницу по URL и возвращает текст.

    Функция принимает на вход url. Это адрес веб-страницы.

    Функция возвращает текст страницы.
    """
    response = requests.get(url, timeout=10.0)
    response.raise_for_status()

    content = response.text

    return content


def read_text_from_file(path: str) -> str:
    """Читает текст из локального файла.

    Функция принимает на вход path. Это путь к файлу.

    Функция возвращает текст файла.
    """
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")

    return text


def find_dates_in_url(url: str) -> List[str]:
    """Ищет корректные даты на веб-странице по URL.

    Функция принимает на вход url. Это адрес веб-страницы.

    Функция возвращает список найденных дат.
    """
    text = read_text_from_url(url)
    return find_dates(text)


def find_dates_in_file(path: str) -> List[str]:
    """Ищет корректные даты в локальном файле.

    Функция принимает на вход path. Это путь к файлу.

    Функция возвращает список найденных дат.
    """
    text = read_text_from_file(path)
    return find_dates(text)
