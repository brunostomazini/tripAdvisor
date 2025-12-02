"""from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for new_field in self.visible_fields():
            new_field.field.widget.attrs.update({'class': "form-control"})
            if len(new_field.errors.data) > 0:
                new_field.field.widget.attrs.update(
                    {'class': "form-control is-invalid"}
                )
"""
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        if self.is_bound and self.errors:
            for field_name, errors in self.errors.items():
                if field_name in self.fields:
                    current_class = self.fields[field_name].widget.attrs.get('class', '')
                    self.fields[field_name].widget.attrs.update({
                        'class': f'{current_class} is-invalid'}
                        )