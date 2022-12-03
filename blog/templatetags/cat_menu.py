from atexit import register
from operator import imod
from django import template
from blog.models import Section

register = template.Library()


@register.simple_tag
def get_cats():
        return Section.objects.all()

@register.simple_tag
def get_3cats():
        return Section.objects.all()[:3]