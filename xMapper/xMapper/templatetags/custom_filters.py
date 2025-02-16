from django import template

register = template.Library()

@register.filter(name='newline_to_br')
def newline_to_br(value):
    return value.replace('\n', '<br>') if value else value
