from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def css(filePath):
    return mark_safe('<link rel="stylesheet" type="text/css" href="'+settings.STATIC_URL+filePath+'"/>')

@register.simple_tag
def js(filePath):
    return mark_safe('<script type="text/javascript" src="'+settings.STATIC_URL+filePath+'"></script>')

@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)

@register.simple_tag
def modelsObjectsEquals(obj1, obj2):
    return obj1 != None and obj2 != None and obj1.id == obj2.id


@register.filter
def call(obj, args): #args comprend le nom de la méthode en premier element et les arguments ensuite
    method = getattr(obj, args[0])
    return method(*args[1:])

@register.filter
def add(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)