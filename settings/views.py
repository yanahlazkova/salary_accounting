from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SocialSettingsForm
from .models import SocialSettings


def settings(request):
    data_db = SocialSettings.objects.all().values() #.order_by('-effective_from')
    table_titles = [f.verbose_name for f in SocialSettings._meta.fields]

    # Створюємо список списків (ID + значення полів)
    rows_data = []
    for obj in data_db:
        rows_data.append({
            'id': obj['id'],  # Звернення через дужки (словник)
            'values': [obj.get(f.name) for f in SocialSettings._meta.fields]
        })

    context = {
        'title': 'Налаштування соціальних показників',
        'icon_title': 'bi bi-gear me-2',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'buttons': [
            {
                'redirect_button': 'add_social_settings',
                'icon_button': 'bi bi-gear',
                'title_button': 'Додати',
            },
        ],
        'contents': [
            'social_settings.html',
            'base_table.html',
        ],
        'table_titles': table_titles,
        'table_rows': rows_data,
        'editing': 'editing',
    }

    # ПЕРЕВІРКА: Чи це HTMX запит?
    if request.headers.get('HX-Request'):
        # Віддаємо контент (без меню)
        return render(request, 'base_content.html', context)
        # return render(request, 'data_social_settings.html', context)

    # Якщо звичайний запит — віддаємо сторінку, яка "огортає" контент в base.html
    return render(request, 'base_page.html', context)
    # return render(request, 'page_social_settings.html', context)

def add_social_settings(request):
    context = {
        'title': 'Додати соціальні показники',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'form_action': 'add_social_settings',
        'buttons': [
            {
                'redirect_button': 'settings',
                'icon_button': 'bi bi-arrow-left-square', # 'bi bi-backspace',
                'title_button': 'Exit',
            }
        ]
    }

    if request.method == 'POST':
        form = SocialSettingsForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            # Для HTMX краще робити редирект через заголовок HX-Redirect
            if request.headers.get('HX-Request'):
                response = HttpResponse()
                response['HX-Redirect'] = reverse('settings')
                return response
            return redirect('settings')
        else:
            # Якщо форма невалідна, просто рендеримо її з помилками
            context['form'] = form
            return render(request, 'form_social_settings.html', context)

    elif request.method == 'GET':
        print(f'method = {request.method}')
        form = SocialSettingsForm()
        context['form'] = form
        # ПЕРЕВІРКА: Чи це HTMX запит?
        if request.headers.get('HX-Request'):
            # Віддаємо тільки таблицю (без меню)
            print('form_social_settings')
            return render(request, 'form_social_settings.html', context)
        else:
            # Якщо звичайний запит — віддаємо сторінку, яка "огортає" таблицю в base.html
            print('page_form_social_settings')
            return render(request, 'page_form_social_settings.html', context)

def edit_social_settings(request, id_social_settings):
    return HttpResponse(f'Editing f{id_social_settings}')