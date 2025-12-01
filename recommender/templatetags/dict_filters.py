"""
Template filters personalizados para acceder a diccionarios y listas.
"""
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Obtiene un item de un diccionario usando una clave."""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def contains(lista, item):
    """Verifica si un item está en una lista."""
    if lista is None:
        return False
    if not isinstance(lista, (list, tuple)):
        return False
    return item in lista

