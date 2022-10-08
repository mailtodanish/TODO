from django.template import Library

register = Library()

@register.filter(name='add_attr')
def add_attr(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, val = d.split(':')
            attrs[key] = val

    return field.as_widget(attrs=attrs)

@register.filter(name='calculate_seq_number')
def calculate_seq_number(counter, page_number):
    return (page_number -1) * 20 + counter + 1
