import re
from django import forms
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _

from django_cleanhtmlfield.helpers import clean_html


class HTMLField(fields.TextField):
    """
    HTMLField
    Allows storing specified HTML tags with specified attributes and arbitrary content
    Internally, this is handled as a TextField
    """

    description = _(u"HTML Field")

    EMPTY_HTML_REGEXP = re.compile(r'^<p>( |\s|&nbsp;)*</p>$')

    def __init__(self, strip_unsafe=False, widget_form_class=None, *args, **kwargs):
        """
        :param strip_unsafe: boolean Needs to be set to true if you want the HTML Field to strip unsafe elements
        :param widget_form_class: string Custom css class for the editor
        :param kwargs:
        """
        self.strip_unsafe, self.widget_form_class = strip_unsafe, widget_form_class

        # verify that certain attributes are not set for this field (primary_key, unique, max_length), as this would
        # be a conflict with the purpose of the HTMLField
        for arg in ('primary_key', 'unique', 'max_length'):
            if arg in kwargs:
                raise TypeError("'%s' is not a valid argument for %s." % (arg, self.__class__))

        super(HTMLField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        """
        Internally a HTMLField is a TextField
        :return:
        """
        return "TextField"

    def get_db_prep_value(self, value, connection, prepared=False):
        """Prepares the python object for saving in the database.
        """
        if not value:
            return value

        return clean_html(value, strip_unsafe=self.strip_unsafe)

    def formfield(self, *args, **kwargs):
        defaults = {'form_class': forms.CharField}
        css_class = 'wysiwyg'

        if 'initial' in kwargs:
            defaults['required'] = False

        # allow the css class of the widget to be overwritten
        if self.widget_form_class:
            css_class = self.widget_form_class

        defaults['widget'] = forms.Textarea(
            attrs={
                'class': css_class,
            }
        )

        defaults.update(kwargs)
        return super(HTMLField, self).formfield(*args, **defaults)
