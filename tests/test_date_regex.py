"""Тесты для модуля src.date_regex."""

import unittest

from src.date_regex import find_dates, is_valid_date


VALID_DATES = [
    # Обычные корректные даты
    "01.01.0001",
    "10.11.2026",
    "11.09.2001",
    "29.02.2016",
    "28.02.2021",
    "26.12.1991",
    "24.02.2022",
    "16.07.1945",
    "20.08.2023",
    "20.08.2077",
    "17.08.2033",
    "16.03.2034",
    "12.06.2035",
    "18.11.2011",
    "31.12.2026",

    # Високосные годы: делятся на 4, но не на 100.
    "29.02.2020",
    "29.02.2024",
    "29.02.2096",
    "29.02.0004",
    "29.02.0096",
    "29.02.0104",

    # Високосные годы: делятся на 400.
    "29.02.2000",
    "29.02.2400",
    "29.02.1600",
    "29.02.0400",
    "29.02.0800",
    "29.02.0000",

    # 28 февраля всегда корректно
    "28.02.1900",
    "28.02.2100",
    "28.02.2021",
    "28.02.2020",
]


INVALID_DATES = [
    # Пустые значения
    "",
    " ",
    ".",
    "..",
    "...",

    # Неправильный формат
    "16.2.2026",
    "16.2.2026",
    "1.02.2026",
    "16-02-2026",
    "16/02/2026",
    "16.02.202",
    "16.02.20266",
    "16.02.2026 ",
    " 16.02.2026",
    "16 .02.2026",
    "16. 02.2026",
    "16.02 .2026",
    "16.02. 2026",

    # Неправильный месяц.
    "01.00.1984",
    "01.13.1984",
    "01.99.1984",

    # Неправильный день
    "00.01.1968",
    "32.01.1968",
    "99.01.1968",

    # 31 число в месяцах с 30 днями
    "31.04.2020",
    "31.06.2020",
    "31.09.2020",
    "31.11.2020",

    # Февраль
    "29.02.2021",
    "29.02.1900",
    "29.02.2100",
    "29.02.2200",
    "29.02.2300",
    "30.02.2020",
    "31.02.2020",
    "00.02.2020",
]


COMMON_YEAR_MAX_DAYS = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


LEAP_YEAR_MAX_DAYS = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


LEAP_YEARS = [
    "0000",
    "0004",
    "0096",
    "0104",
    "0400",
    "0800",
    "1600",
    "2000",
    "2020",
    "2024",
    "2400",
    "9600",
]


NON_LEAP_YEARS = [
    "0001",
    "0099",
    "0100",
    "1900",
    "2021",
    "2100",
    "2200",
    "2300",
    "9900",
]


class TestDateValidation(unittest.TestCase):
    """Тесты проверки одной строки как даты."""

    def test_valid_dates(self) -> None:
        for value in VALID_DATES:
            with self.subTest(value=value):
                self.assertTrue(is_valid_date(value))

    def test_invalid_dates(self) -> None:
        for value in INVALID_DATES:
            with self.subTest(value=value):
                self.assertFalse(is_valid_date(value))

    def test_non_string_returns_false(self) -> None:
        values = [
            None,
            123,
            20200101.0,
            ["01.01.2020"],
            {"date": "01.01.2020"},
        ]

        for value in values:
            with self.subTest(value=value):
                self.assertFalse(is_valid_date(value))


class TestFindDates(unittest.TestCase):
    """Тесты поиска дат внутри произвольного текста."""

    def test_find_single_date(self) -> None:
        text = "Бла-Бла-Бла: 31.12.2023."
        self.assertEqual(find_dates(text), ["31.12.2023"])

    def test_find_multiple_dates(self) -> None:
        text = (
            "Начало 01.01.2024, середина 15.06.2024, "
            "конец 31.12.2024. Ошибка: 31.02.2024."
        )

        self.assertEqual(find_dates(text), ["01.01.2024", "15.06.2024", "31.12.2024"])

    def test_invalid_day_for_month(self) -> None:
        text = "Неверно 31.04.2020 и 29.02.2021"
        self.assertEqual(find_dates(text), [])

    def test_no_leading_zero(self) -> None:
        text = "Не дата: 1.01.2019, 01.1.2023, 1.1.2077"
        self.assertEqual(find_dates(text), [])

    def test_not_find_inside_long_number(self) -> None:
        text = "Не дата 12301.01.2020456"
        self.assertEqual(find_dates(text), [])

    def test_not_find_after_dot_prefix(self) -> None:
        text = "Версия 1.01.01.2024 не должна находиться частично"
        self.assertEqual(find_dates(text), [])

    def test_not_find_dot_suffix(self) -> None:
        text = "Дата 01.01.2024.1 не должна находиться как полная дата"
        self.assertEqual(find_dates(text), [])

    def test_date_before_end_dot(self) -> None:
        text = "Дата: 01.01.2025."
        self.assertEqual(find_dates(text), ["01.01.2025"])

    def test_leap_day(self) -> None:
        text = "Високосная дата 29.02.2020"
        self.assertEqual(find_dates(text), ["29.02.2020"])

    def test_non_leap_feb_29(self) -> None:
        text = "Не високосная дата 29.02.2021"
        self.assertEqual(find_dates(text), [])

    def test_empty_text(self) -> None:
        self.assertEqual(find_dates(""), [])

    def test_non_string_error(self) -> None:
        with self.assertRaises(TypeError):
            find_dates(None)  # type: ignore[arg-type]


class TestRegexBranches(unittest.TestCase):
    """Тесты отдельных альтернатив регулярного выражения."""

    def test_31_day_months(self) -> None:
        months = ["01", "03", "05", "07", "08", "10", "12"]

        for month in months:
            with self.subTest(month=month):
                self.assertTrue(is_valid_date(f"01.{month}.2018"))
                self.assertTrue(is_valid_date(f"31.{month}.2018"))

    def test_30_day_months(self) -> None:
        months = ["04", "06", "09", "11"]

        for month in months:
            with self.subTest(month=month):
                self.assertTrue(is_valid_date(f"01.{month}.2018"))
                self.assertTrue(is_valid_date(f"30.{month}.2018"))
                self.assertFalse(is_valid_date(f"31.{month}.2018"))

    def test_february_non_leap_max_day(self) -> None:
        self.assertTrue(is_valid_date("28.02.2021"))
        self.assertFalse(is_valid_date("29.02.2021"))

    def test_february_leap_divisible_by_4_not_100(self) -> None:
        self.assertTrue(is_valid_date("29.02.2020"))
        self.assertTrue(is_valid_date("29.02.2024"))
        self.assertTrue(is_valid_date("29.02.0004"))

    def test_february_leap_divisible_by_400(self) -> None:
        self.assertTrue(is_valid_date("29.02.2000"))
        self.assertTrue(is_valid_date("29.02.2400"))
        self.assertTrue(is_valid_date("29.02.0400"))
        self.assertTrue(is_valid_date("29.02.0000"))

    def test_february_century_not_divisible_by_400(self) -> None:
        self.assertFalse(is_valid_date("29.02.1900"))
        self.assertFalse(is_valid_date("29.02.2100"))
        self.assertFalse(is_valid_date("29.02.2200"))
        self.assertFalse(is_valid_date("29.02.2300"))


class TestAllMonthDayCombinations(unittest.TestCase):
    """Перебор всех дней и месяцев для обычных и високосных годов."""

    def _check_year(self, year: str, max_days: dict) -> None:
        for month, limit in max_days.items():
            for day in range(1, 32):
                value = f"{day:02d}.{month:02d}.{year}"
                expected = day <= limit

                with self.subTest(value=value):
                    self.assertEqual(is_valid_date(value), expected)

    def test_common_year_2021(self) -> None:
        self._check_year("2021", COMMON_YEAR_MAX_DAYS)

    def test_leap_year_2020(self) -> None:
        self._check_year("2020", LEAP_YEAR_MAX_DAYS)


class TestLeapYears(unittest.TestCase):
    """Тесты високосных и невисокосных годов."""

    def test_feb_29_in_leap_years(self) -> None:
        for year in LEAP_YEARS:
            with self.subTest(year=year):
                self.assertTrue(is_valid_date(f"29.02.{year}"))

    def test_feb_29_in_non_leap_years(self) -> None:
        for year in NON_LEAP_YEARS:
            with self.subTest(year=year):
                self.assertFalse(is_valid_date(f"29.02.{year}"))

    def test_feb_28_is_always_valid(self) -> None:
        years = LEAP_YEARS + NON_LEAP_YEARS

        for year in years:
            with self.subTest(year=year):
                self.assertTrue(is_valid_date(f"28.02.{year}"))
