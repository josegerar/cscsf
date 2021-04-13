from django.utils import formats, datetime_safe


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def format_datetime(value):
    """retorna un valor formateado en formato fecha hora"""
    if value is None:
        return ''
    formater = formats.get_format('DATETIME_INPUT_FORMATS')[0]
    if hasattr(value, 'strftime'):
        value = datetime_safe.new_datetime(value)
        return value.strftime(formater)
    return value
