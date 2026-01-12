from django.shortcuts import render, redirect
from .models import PayrollSettings
from .forms import PayrollSettingsForm

def settings(request):
    # Отримуємо перший запис або створюємо порожній, якщо його ще немає
    settings_obj, created = PayrollSettings.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = PayrollSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            return redirect('home') # Повернення на головну після збереження
    else:
        form = PayrollSettingsForm(instance=settings_obj)

    return render(request, 'settings_form.html', {'form': form})

