from django import forms
from django.forms import ModelForm

from persons.models import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Проходимо циклом по всіх полях форми
        for field_name, field in self.fields.items():
            # Додаємо загальний клас для всіх
            field.widget.attrs.update({'class': 'form-control'})
            # Якщо поле — це дата, міняємо тип на календар
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})

            # Якщо поле — це Decimal (числове), додаємо крок 0.01
            if isinstance(field, forms.DecimalField):
                field.widget.attrs.update({'step': '0.01'})

            # Користувач не зможе ввести число менше 0
            if isinstance(field, forms.DecimalField) or isinstance(field, forms.IntegerField):
                field.widget.attrs.update({'min': '0', 'step': '0.01'})