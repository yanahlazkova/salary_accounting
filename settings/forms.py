from cProfile import label
from os import name

from django import forms
from django.core.exceptions import ValidationError

from settings.models import SocialSettings


class SocialSettingsForm(forms.ModelForm):
    # effective_from = forms.DateField(
    #     label="Дата введення в дію",
    #     widget=forms.DateInput(
    #         attrs={
    #             'type': 'date',  # Це активує календар
    #             'min': "2000-01-02",
    #             'max': "2030-01-01",
    #             'class': 'form-control'  # Додаємо клас Bootstrap для гарного вигляду
    #         }
    #     )
    # )
    # min_salary = forms.DateField(
    #     label="Мінімальна заробітна плата (місячна)",
    #     widget=forms.NumberInput(
    #         attrs={
    #             'type': 'number',
    #             'min': "0,01",
    #             'pattern': '[0-9]{8}.[0-9]{2}',
    #             'class': 'form-control',
    #         }
    #     ),
    # )

    class Meta:
        model = SocialSettings
        fields = ['effective_from',
                  'min_salary',
                  'pm_able_bodied',
                  'pdfo_rate',
                  'vz_rate',
                  'esv_rate',  # attrs multiple - можна обрати декілька значень
                  ]
        error_messages = {
            'effective_from': {
                'unique': "Дані з такою датою вже існують. Оберіть іншу дату.",
            },
        }

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

    # def clean_effective_from(self):
    #     date = self.cleaned_data.get('effective_from')
    #
    #     # Перевіряємо, чи є вже такий запис у базі (тільки для нових записів)
    #     if SocialSettings.objects.filter(effective_from=date).exists():
    #         raise forms.ValidationError(f'Дані з такою датою {date} вже існують.')
    #
    #     # ОБОВ'ЯЗКОВО повертаємо значення
    #     return date