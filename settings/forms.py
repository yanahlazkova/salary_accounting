from django import forms
from .models import PayrollSettings

class PayrollSettingsForm(forms.ModelForm):
    class Meta:
        model = PayrollSettings
        fields = '__all__'
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pm_for_able_bodied': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pdfo_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'vz_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'esv_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

