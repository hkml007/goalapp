from django import template

register = template.Library()

@register.filter
def can_edit(challenge, user):
    return challenge.can_edit(user)

@register.filter
def dict_get(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return False  # Default to False if dictionary is None (for the "disabled" check)
    return dictionary.get(key, False)