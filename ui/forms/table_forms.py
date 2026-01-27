from django import forms


class TableFilterForm(forms.Form):
    search = forms.CharField(required=False, label="Пошук")
    active = forms.BooleanField(required=False, label="Активні")
