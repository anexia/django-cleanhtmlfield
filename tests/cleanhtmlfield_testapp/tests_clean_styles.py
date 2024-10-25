from django.test import SimpleTestCase

from django_cleanhtmlfield.helpers import clean_styles


class TestCleanStyles(SimpleTestCase):
    def test_clean_styles_multiple_double_dots(self):
        """
        Tests that cleaning css styles leaves styles with multiple dots in place
        :return:
        """
        self.assertEqual("color:red:foo();", clean_styles("color:red:foo();"))

    def test_clean_styles_adds_semicolon(self):
        """
        Tests whether clean styles add a semicolon
        :return:
        """
        self.assertEqual("color:red;", clean_styles("color:red"))

        self.assertEqual(
            "color:red;font-size:10pt;", clean_styles("color:red; font-size:10pt")
        )

    def test_clean_styles_single(self):
        """
        Tests that cleaning styles removes extra spaces
        :return:
        """
        self.assertEqual("padding:9px;", clean_styles("padding: 9px; "))

        self.assertEqual("margin:9px;", clean_styles("margin: 9px; "))

        self.assertEqual("padding-top:9px;", clean_styles("padding-top: 9px; "))

    def test_clean_styles_multiple(self):
        """
        Tests that cleaning styles works with multiple styles
        :return:
        """
        self.assertEqual(
            "padding:9px;margin-top:10px;margin-bottom:10px;",
            clean_styles("padding: 9px; margin-top: 10px; margin-bottom: 10px;"),
        )

    def test_clean_styles_invalid_element(self):
        """
        Tests that cleaning styles removes invalid elements
        :return:
        """
        self.assertEqual(
            "padding:9px;margin-bottom:10px;",
            clean_styles(
                "padding: 9px; some-invalid-attribute: 10px; margin-bottom: 10px;"
            ),
        )

    def test_clean_styles_preserve_styles_whitespace(self):
        """
        Tests that cleaning styles optionally does not remove whitespace
        :return:
        """
        with self.settings(PRESERVE_STYLES_WHITESPACE=True):
            self.assertEqual("padding: 9px;", clean_styles("padding: 9px; "))

            self.assertEqual("padding : 9px;", clean_styles("padding : 9px; "))

            self.assertEqual("padding:  9px;", clean_styles("padding:  9px; "))

            self.assertEqual(
                "padding: 9px; margin-top: 10px; margin-bottom: 10px;",
                clean_styles("padding: 9px; margin-top: 10px; margin-bottom: 10px;"),
            )

            self.assertEqual(
                "padding: 9px;margin-top: 10px;margin-bottom: 10px;",
                clean_styles("padding: 9px;margin-top: 10px;margin-bottom: 10px;"),
            )
