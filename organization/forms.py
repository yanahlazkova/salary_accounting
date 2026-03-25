from django.forms import ModelForm
from django import forms

from organization.models import Organization, Ustanova, BankAccount


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
            'short_name',
            'kpk',
            'head',
            # 'location',
            # 'address',
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


class BankAccountCreateForm(ModelForm):
    class Meta:

        model = BankAccount
        fields = [
            'account',
            'fund',
            'ustanova',
        ]

    def __init__(self, *args, **kwargs):
        # self.ustanova = kwargs.pop('ustanova', None)
        # print(f'ustanova: {self.ustanova}')

        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control w-auto'})

            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(format='%Y-%m-%d',
                                               attrs={'type': 'date',
                                                      'class': 'form-control w-auto'})
                field.input_formats = ["%Y-%m-%d"]

        if 'ustanova' in self.fields:
            self.fields['ustanova'].empty_label = "Установа не вибрана"
        #     # Залишаємо випадаючий список, але в ньому буде лише одна установа
            ustanova_obj = self.initial.get('ustanova') or self.data.get('ustanova')
            if ustanova_obj:
                self.fields['ustanova'].queryset = Ustanova.objects.filter(kpk=ustanova_obj.kpk)
                # # Додаємо атрибут disabled, щоб не можна було клацнути (опційно)
                # self.fields['ustanova'].widget.attrs['disabled'] = True
        #         # Робимо поле прихованим, щоб користувач не бачив список
        #         self.fields['ustanova'].widget = forms.HiddenInput()
            self.fields['ustanova'].empty_label = None

        # if 'fund' in self.fields:
        #     choices = list(self.fields['fund'].choices)
        #     choices[0] = ('', 'Дані не вибрані')
        #     self.fields['fund'].choices = choices

class BankAccountForm(ModelForm):
        class Meta:

            model = BankAccount
            fields = [
                'account',
                'fund',
                'ustanova',
            ]

        def __init__(self, *args, **kwargs):
            # self.ustanova = kwargs.pop('ustanova', None)
            # print(f'ustanova: {self.ustanova}')

            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs.update({'class': 'form-control w-auto'})

                if isinstance(field, forms.DateField):
                    field.widget = forms.DateInput(format='%Y-%m-%d',
                                                   attrs={'type': 'date',
                                                          'class': 'form-control w-auto'})
                    field.input_formats = ["%Y-%m-%d"]


