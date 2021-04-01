from django import template

from app.settings import MEDIA_URL, STATIC_URL

register = template.Library()


@register.filter
def view_prop(value, arg):
    if value is not None:
        strresult = getattr(value, arg)
        return strresult
    return ""


@register.filter
def get_url_image(value, arg):
    if value is not None:
        strresult = getattr(value, arg)
        if strresult:
            return '{}{}'.format(MEDIA_URL, strresult)
    return '{}{}'.format(STATIC_URL, 'img/user.png')
