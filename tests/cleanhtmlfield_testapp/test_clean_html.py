from django.test import SimpleTestCase

from django_cleanhtmlfield.helpers import clean_html


class TestCleanHtml(SimpleTestCase):
    def test_clean_script_tags(self):
        """
        Tests that javascript "script" tags are removed
        :return:
        """
        self.assertEquals(
            clean_html(
                "<p>test</p><script>alert('hello');</script>", strip_unsafe=True
            ),
            "<p>test</p>",
        )

    def test_clean_html_keep_it(self):
        """
        Tests a rather long HTML string that should always be kept as it is
        :return:
        """
        some_html_str = """<h1>Groot Ipsum</h1>
<p>I am Groot. I am Groot. I am Groot. We are Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. We are Groot. We are Groot. We are Groot. We are Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. We are Groot. </p>
<p>I am Groot. I am Groot. <span style="color:red">I am Groot</span>. We are Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. We are Groot. We are Groot. We are Groot. We are Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. We are Groot.
</p>
<h3>Some title</h3>
<p>I am Groot. <i>I am Groot</i>. I am Groot. We are Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. We are Groot. We are Groot. We are Groot. We are Groot. We are Groot. I am Groot. We are Groot. I am Groot. I am Groot. I am Groot. We are Groot. We are Groot.
</p>"""
        self.assertEquals(clean_html(some_html_str), some_html_str)
