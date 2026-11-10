"""Консольное меню для пользователя

Можно проверить одну строку, многострочный текст, файл (.txt, .html - прога интерпретириует их как текстовые в любом
случае), сайт по URL (тестировал на:
https://delo-press.ru/journals/documents/oformlenie-dokumentov/42737-vremennye-periody-i-chislovye-intervaly/).
"""

from typing import List
from src.date_regex import find_dates, is_valid_date
from src.files_and_urls_handler import find_dates_in_file, find_dates_in_url


def format_dates(dates: List[str]) -> str:
    """Возвращает текстовое представление списка дат.

    Функция принимает на вход dates. Это список найденных дат.

    Функция возвращает строку
    """
    if not dates:
        return "Даты не найдены."

    return "Найденные даты:\n" + "\n".join(dates)


def validate_date(value: str) -> bool:
    """Возвращает сообщение о корректности даты.

    Функция принимает на вход value. Это проверяемая строка.

    Функция возвращает bool значение
    """
    if is_valid_date(value):
        return True

    return False


def search_text(text: str) -> str:
    """Возвращает сообщение с датами, найденными в тексте.

    Функция принимает на вход text. Это текст для поиска.

    Функция возвращает строку со списком найденных дат.
    """
    try:
        return format_dates(find_dates(text))
    except Exception as exc:
        return f"Произошла непредвиденная ошибка: {exc}"


def search_file(path: str) -> str:
    """Возвращает сообщение с датами, найденными в файле.

    Функция принимает на вход path. Это путь к файлу.

    Функция возвращает строку со списком найденных дат или сообщением об ошибке.
    """
    try:
        return format_dates(find_dates_in_file(path))
    except Exception as exc:
        return f"Ошибка чтения файла: {exc}"


def search_url(path: str) -> str:
    """Возвращает сообщение с датами, найденными по URL.

    Функция принимает на вход path. Это путь к файлу.

    Функция возвращает строку со списком найденных дат или сообщением об ошибке.
    """
    return format_dates(find_dates_in_url(path))


def read_multiline_text() -> str:
    """Читает многострочный текст до пустой строки.

    Функция возвращает введённый текст как одну строку.
    """
    print("Введите текст. Пустая строка завершает ввод:")

    lines = []

    while True:
        line = input()

        if line == "":
            break

        lines.append(line)

    return "\n".join(lines)


def main():
    """Простое меню в консоли."""
    while True:
        try:
            print()
            print("Меню:")
            print("1 - проверить дату")
            print("2 - найти даты во введённом тексте")
            print("3 - найти даты в файле")
            print("4 - найти даты по URL")
            print("0 - выход")

            choice = input("Выберите пункт: ").strip()

            if choice == "1":
                value = input(
                    "Введите дату в формате ДД.ММ.ГГГГ: ",
                ).strip()

                if validate_date(value):
                    print("Дата корректна.")
                else:
                    print("Дата некорректна.")

            elif choice == "2":
                text = read_multiline_text()
                print(search_text(text))

            elif choice == "3":
                path = input("Введите путь к файлу: ").strip()
                print(search_file(path))

            elif choice == "4":
                path = input("Введите URL: ").strip()
                print(search_url(path))

            elif choice == "0":
                break

            else:
                print("Неизвестный пункт меню.")

        except (EOFError, KeyboardInterrupt) as exc:
            print(f"Произошла непредвиденная ошибка: {exc}")
            break


if __name__ == "__main__":
    main()
