from django.test import TestCase
from myapp.models import MyModel


class TestCleanHtml(TestCase):
    def test_create_and_save_in_db(self):
        """
        Tests saving a HTML field in database
        :return:
        """
        obj = MyModel()
        obj.some_html_field = "<p>Test</p>"
        obj.save()

        obj.refresh_from_db()

        self.assertEqual(obj.some_html_field, "<p>Test</p>")

    def test_create_and_save_complex_html_string_in_db(self):
        """
        Tests saving a HTML field with complex html string in database
        :return:
        """
        complex_html_string = """<h1>Groot Ipsum</h1>
<p>I am Groot. I am Groot. I am Groot. We are Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. We are Groot. We are Groot. We are Groot. We are Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. We are Groot. </p>
<p>I am Groot. I am Groot. <span style="color:red;">I am Groot</span>. 
We are Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. We are Groot. We are Groot. We are Groot. We are Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. We are Groot.
</p>
<h3>Some title</h3>
<p>I am Groot. <i>I am Groot</i>. I am Groot. We are Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. We are Groot. We are Groot. We are Groot. We are Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. We are Groot.
</p>"""
        obj = MyModel()
        obj.some_html_field = complex_html_string
        obj.save()

        self.maxDiff = None

        obj.refresh_from_db()

        self.assertEqual(obj.some_html_field, complex_html_string)

    def test_try_save_with_invalid_content(self):
        """
        Tries to save a html field with some invalid and malicious content
        :return:
        """
        malicious_html_string = """<h1>Groot Ipsum</h1>
        <script type="text/javascript">
        alert('Do something evil in Javascript');
        </script>
        <p>I am Groot. I am Groot. I am Groot. We are Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. We are Groot. We are Groot. We are Groot. We are Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. We are Groot. </p>
        <p>I am Groot. I am Groot. <span style="color:red">I am Groot</span>. We are Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. We are Groot. We are Groot. We are Groot. We are Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. We are Groot.
        </p>
        <h3>Some title</h3>
        <p>I am Groot. <i>I am Groot</i>. I am Groot. We are Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. We are Groot. We are Groot. We are Groot. We are Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. We are Groot.
        </p>"""
        obj = MyModel()
        obj.some_html_field = malicious_html_string
        obj.save()

        obj.refresh_from_db()

        self.assertNotEqual(obj.some_html_field, malicious_html_string)
        self.assertFalse("<script" in obj.some_html_field)
        self.assertFalse("alert" in obj.some_html_field)
