from django import template

register = template.Library()

@register.filter(name='get')
def get(dictionary, key):
    """
    Permite acceder a un valor de diccionario usando una variable en el template.
    Uso: {{ mi_diccionario|get:mi_llave }}
    """
    if hasattr(dictionary, 'get'):
        return dictionary.get(key)
    return None