from django.db import models

from django_cleanhtmlfield.fields import HTMLField


class MyModel(models.Model):
    some_html_field = HTMLField(strip_unsafe=True)
