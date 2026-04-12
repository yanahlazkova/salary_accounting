from enum import auto

from django.forms import ModelForm
from django import forms


from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        label="Пошук",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control w-auto',
            'placeholder': 'Введіть назву ліків...'
        })
    )

    def __init__(self, *args, search_fields=None, **kwargs):
        """
        search_fields = [
            ('firstname', 'Імʼя'),
            ('lastname', 'Прізвище'),
            ('email', 'Email'),
        ]
        """
        super().__init__(*args, **kwargs)

        if search_fields:
            self.fields['fields'] = forms.MultipleChoiceField(
                choices=search_fields,
                widget=forms.CheckboxSelectMultiple(attrs={
                    'class': 'form-check-input'
                }),
                required=False,
                label="Шукати у"
            )