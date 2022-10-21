from django.test import SimpleTestCase

from django_cleanhtmlfield.helpers import clean_styles


class TestCleanStyles(SimpleTestCase):
    def test_clean_styles_multiple_double_dots(self):
        """
        Tests that cleaning css styles leaves styles with multiple dots in place
        :return:
        """
        self.assertEquals(clean_styles("color:red:foo();"), "color:red:foo();")

    def test_clean_styles_adds_semicolon(self):
        """
        Tests whether clean styles add a semicolon
        :return:
        """
        self.assertEquals(clean_styles("color:red"), "color:red;")

        self.assertEquals(
            clean_styles("color:red; font-size:10pt"), "color:red;font-size:10pt;"
        )

    def test_clean_styles_single(self):
        """
        Tests that cleaning styles removes extra spaces
        :return:
        """
        self.assertEquals(clean_styles("padding: 9px; "), "padding:9px;")

        self.assertEquals(clean_styles("margin: 9px; "), "margin:9px;")

        self.assertEquals(clean_styles("padding-top: 9px; "), "padding-top:9px;")

    def test_clean_styles_multiple(self):
        """
        Tests that cleaning styles works with multiple styles
        :return:
        """
        self.assertEquals(
            clean_styles("padding: 9px; margin-top: 10px; margin-bottom: 10px;"),
            "padding:9px;margin-top:10px;margin-bottom:10px;",
        )

    def test_clean_styles_invalid_element(self):
        """
        Tests that cleaning styles removes invalid elements
        :return:
        """
        self.assertEquals(
            clean_styles(
                "padding: 9px; some-invalid-attribute: 10px; margin-bottom: 10px;"
            ),
            "padding:9px;margin-bottom:10px;",
        )

    def test_clean_styles_preserve_styles_whitespace(self):
        """
        Tests that cleaning styles optionally does not remove whitespace
        :return:
        """
        with self.settings(PRESERVE_STYLES_WHITESPACE=True):
            self.assertEquals(clean_styles("padding: 9px; "), "padding: 9px;")

            self.assertEquals(clean_styles("padding : 9px; "), "padding : 9px;")

            self.assertEquals(clean_styles("padding:  9px; "), "padding:  9px;")

            self.assertEquals(
                clean_styles("padding: 9px; margin-top: 10px; margin-bottom: 10px;"),
                "padding: 9px; margin-top: 10px; margin-bottom: 10px;",
            )

            self.assertEquals(
                clean_styles("padding: 9px;margin-top: 10px;margin-bottom: 10px;"),
                "padding: 9px;margin-top: 10px;margin-bottom: 10px;",
            )
