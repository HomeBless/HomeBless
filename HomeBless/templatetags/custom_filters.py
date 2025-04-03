from django import template

register = template.Library()


@register.filter
def remove_page_param(query_string):
    if not query_string:
        return ''
    params = query_string.split('&')
    filtered_params = [p for p in params if not p.startswith('page=')]
    return '&'.join(filtered_params)
