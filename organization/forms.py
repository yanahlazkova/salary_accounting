from django.forms import ModelForm
from django import forms

from organization.models import Organization, Ustanova


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name',
            'edrpou',
            'mfo',
            'address',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control w-50'})

            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(format='%Y-%m-%d',
                                               attrs={'type': 'date',
                                                      'class': 'form-control w-50'})
                field.input_formats = ["%Y-%m-%d"]


class UstanovaForm(ModelForm):
    class Meta:
        model = Ustanova
        fields = [
            'name',
            'kpk',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control w-50'})

            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(format='%Y-%m-%d',
                                               attrs={'type': 'date',
                                                      'class': 'form-control w-50'})
                field.input_formats = ["%Y-%m-%d"]
