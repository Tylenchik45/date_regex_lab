"""Тесты для пользовательского меню в консоли."""

import tempfile
import unittest
from pathlib import Path
from src.main import (format_dates, search_file, search_text, validate_date)


class TestFormatDates(unittest.TestCase):
    """Тесты форматирования списка дат."""

    def test_empty_list(self):
        self.assertEqual(format_dates([]), "Даты не найдены.")

    def test_one_date(self):
        self.assertEqual(format_dates(["01.01.2024"]), "Найденные даты:\n01.01.2024")

    def test_multiple_dates(self):
        self.assertEqual(format_dates(["01.01.2024", "31.12.2024"]), "Найденные даты:\n01.01.2024\n31.12.2024")


class TestValidateDate(unittest.TestCase):
    """Тесты проверки одной даты."""

    def test_valid_date(self):
        self.assertEqual(validate_date("29.02.2020"), True)

    def test_invalid_date(self):
        self.assertEqual(validate_date("29.02.2021"), False)

    def test_empty_string(self):
        self.assertEqual(validate_date(""), False)

    def test_date_with_spaces(self):
        self.assertEqual(validate_date(" 01.01.2024 "), False)


class TestSearchText(unittest.TestCase):
    """Тесты поиска дат в тексте."""

    def test_found_dates(self):
        message = search_text("Начало 24.02.2022, ошибка 31.02.2024")

        self.assertIn("24.02.2022", message)
        self.assertNotIn("31.02.2024", message)

    def test_no_dates(self):
        self.assertEqual(search_text("Бесполезный текст"), "Даты не найдены.")

    def test_empty_text(self):
        self.assertEqual(search_text(""), "Даты не найдены.")


class TestSearchFile(unittest.TestCase):
    """Тесты поиска дат в файле."""

    def test_find_in_temp_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "dates.txt"
            path.write_text("Дата 01.01.2024", encoding="utf-8")

            message = search_file(str(path))

            self.assertIn("01.01.2024", message)

    def test_find_in_temp_html_file(self):
        content = """
        <html>
          <body>
            <script>var fake = "29.02.2021";</script>
            <p>Мяу: 01.09.2025</p>
            <p>Гав: 31.04.2025</p>
          </body>
        </html>
        """

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "page.html"
            path.write_text(content, encoding="utf-8")

            message = search_file(str(path))

            self.assertIn("01.09.2025", message)
            self.assertNotIn("29.02.2021", message)
            self.assertNotIn("31.04.2025", message)

    def test_no_dates_in_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "dates.txt"
            path.write_text("Здесь нет дат", encoding="utf-8")

            message = search_file(str(path))

            self.assertEqual(message, "Даты не найдены.")

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "missing.txt"

            message = search_file(str(path))

            self.assertIn("Ошибка чтения файла", message)

    def test_invalid_encoding(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.bin"
            path.write_bytes(b"\xff\xfe")

            message = search_file(str(path))

            self.assertIn("Ошибка чтения файла", message)


if __name__ == "__main__":
    unittest.main()
