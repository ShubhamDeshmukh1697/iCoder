from django import template

register = template.Library()

@register.filter(name='get_val')

def get_val(dict1,key):
    print("get_val function", dict1.get(key))
    return dict1.get(key)
