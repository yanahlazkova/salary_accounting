from django import forms
from django.forms import ModelForm

from persons.models import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Словник з бажаною шириною для конкретних полів
        # Проходимо циклом по всіх полях форми
        for field_name, field in self.fields.items():
            print(field_name, field)
            # Додаємо загальний клас для всіх
            field.widget.attrs.update({'class': 'form-control w-75'})

            # Якщо поле — це дата, міняємо тип на календар
            if isinstance(field, forms.DateField):
                field.widget = (forms.
                                DateInput(attrs={'type': 'date',
                                                 'class': 'form-control w-25',
                                                 # 'style': 'width: 150px'
                                                 }))

            # Якщо поле — це випадаючий список, вказуємо ширину
            # if field_name == 'gender':
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs.update({'class': 'form-control w-25'})

            # Користувач не зможе ввести число менше 0
            if isinstance(field, forms.BooleanField):
                field.widget = forms.CheckboxInput({'type': 'checkbox'})
