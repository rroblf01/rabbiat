from django import template
from handler.utils import get_structure_tool_as_html

register = template.Library()


@register.filter
def format_structure(prompt_id):
    return get_structure_tool_as_html(prompt_id)
