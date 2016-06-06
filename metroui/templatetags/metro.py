from django.template import Context
from django.template.loader import get_template
from django.template import Library
from django import forms
from api.utils import FieldRenderMixin

register = Library()


def get_context_template(element, label=False):
    element_type = element.__class__.__name__.lower()

    if element_type == 'boundfield':
        template = get_template("_metro_form_field.html")
        context = Context({'field': element, 'label': label})
    else:
        if hasattr(element, 'management_form'):
            template = get_template("metro_formset.html")
            context = Context({'formset': element, 'label': label})
        else:
            template = get_template("metro_form.html")
            context = Context({'form': element, 'label': label})
    return template, context


@register.filter
def addcss(field, error):
    _adderrrors = ' error' if error else ''
    if isinstance(field.field.widget, forms.TextInput):
        return FieldRenderMixin.TEXT_INPUT + _adderrrors
    elif isinstance(field.field.widget, forms.Select):
        return FieldRenderMixin.SELECT_INPUT + _adderrrors
    elif isinstance(field.field.widget, forms.Textarea):
        return FieldRenderMixin.TEXT_AREA + _adderrrors
    elif isinstance(field.field.widget, forms.CheckboxInput):
        return FieldRenderMixin.CHECK_INPUT + _adderrrors


@register.filter
def metrorender(element, label='False'):
    label = label == 'True'
    template, context = get_context_template(element, label)
    return template.render(context)


@register.filter
def is_check_or_radio_fields(field):
    return isinstance(field.field.widget, forms.CheckboxInput) or \
           isinstance(field.field.widget, forms.RadioSelect)




