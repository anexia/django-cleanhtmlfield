import logging
from bs4 import BeautifulSoup

from django.conf import settings

logger = logging.getLogger(__name__)


def convert_text_to_html(input_str):
    """
    Converts a textfield (without html) to an html field
    This is useful for migrations or management commands where you need to manually convert the content of a field

    :param input_str:
    :return:
    """
    # convert newlines to line breaks
    input_str = "<p>" + input_str + "</p>"

    soup = BeautifulSoup(input_str, "html.parser")
    input_str = soup.encode_contents(encoding="utf8").decode("utf8")
    input_str = input_str.replace(u"\n", u"<br/>")

    return clean_html(input_str, strip_unsafe=True)


def convert_html_to_text(input_str):
    """
    Converts a html field to a textfield (without html)
    This is useful for migrations or management commands where you need to manually convert the content of a field

    :param input_str:
    :return:
    """
    # remove all existing newlines
    input_str = input_str.replace(u"\n", u"")
    # convert line breaks to newlines
    input_str = input_str.replace(u"<br>", u"\n")
    input_str = input_str.replace(u"<br/>", u"\n")
    input_str = input_str.replace(u"<br />", u"\n")
    input_str = input_str.replace(u"&nbsp;", u" ")

    # strip all html tags
    soup = BeautifulSoup(input_str, "html.parser")

    return soup.get_text()


def clean_styles(styles_string):
    """
    Cleans styles for acceptable styles
    :param styles_string:
    :return: string cleaned style
    """
    cleaned_styles = []
    cleaned_styles_string = ""

    for style_string in styles_string.split(';'):
        if style_string.strip() == '':
            continue

        if ':' not in style_string:
            logger.warning("Removing style string '{}' as it does not contain a :".format(style_string))
            continue

        style = style_string.split(':', 1)
        style_name = style[0].lower().strip()
        style_value = style[1].strip()

        if style_name in getattr(settings, 'ACCEPTABLE_STYLES', tuple()):
            cleaned_styles.append({'name': style_name, 'value': style_value})
        else:
            logger.warning(
                "Removing style string '{}' as the style name '{}' is not "
                "listed in the ACCEPTABLE_STYLES setting".format(
                    style_string, style_name
                )
            )

    for style in cleaned_styles:
        cleaned_styles_string += "%s:%s;" % (style['name'], style['value'])

    return cleaned_styles_string


def clean_hrefs(href_string):
    """
    Cleans hyperlink/href attributes that might contain malicious javascript
    :param href_string:
    :return:
    """
    if href_string.startswith("javascript:"):
        logger.warning("Removing href string '{}' as it contains dangerous code".format(href_string))
        return None

    return href_string


def clean_html(html, strip_unsafe=False):
    """
    clean a html string
    if strip_unsave is set, potentially malicious tags (defined in ``settings.REMOVE_WITH_CONTENT``) are also removed

    :param html: the input HTML string that needs to be cleaned
    :type html: basestring
    :param strip_unsafe:
    :type strip_unsafe: bool
    :return: cleaned html
    :rtype: basestring
    """
    if not html:
        return ""

    doc = BeautifulSoup(html, "html.parser")

    if strip_unsafe:
        for tag in doc.find_all(True):
            if tag.name not in getattr(settings, 'ACCEPTABLE_ELEMENTS', tuple()):
                logger.warning(
                    "Found tag {} which is not in the ACCEPTABLE_ELEMENTS setting".format(tag.name)
                )
                if tag.name in getattr(settings, 'REMOVE_WITH_CONTENT', tuple()):
                    tag.decompose()
                else:
                    tag.unwrap()

            try:
                for attr in tag.attrs.keys():
                    # strip all tags that are not in acceptable attributes
                    if attr not in getattr(settings, 'ACCEPTABLE_ATTRIBUTES', tuple()):
                        logger.warning(
                            "Removing attribute {} of tag {} as it is not listed in the "
                            "ACCEPTABLE_ATTRIBUTES settings".format(attr, tag.name)
                        )
                        del tag[attr]
                        continue

                    # special cases for attributes style and href
                    if attr == 'style':
                        tag[attr] = clean_styles(tag[attr])
                    elif attr == 'href':
                        tag[attr] = clean_hrefs(tag[attr])

            except:
                pass

    # ToDo: Check if we need to be python2 compatible with that
    # doc = unicode(doc)
    # try:
    #     if HTMLField.EMPTY_HTML_REGEXP.match(doc.encode("UTF-8")):
    #         return u""
    # except:
    #     pass
    # encode the result with beautifulsoups html converter, thus "keeping" &nbsp; as &nbsp; (instead of \xa0)
    return doc.encode_contents(formatter='html').decode()
