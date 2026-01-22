from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SocialSettingsForm
from .models import SocialSettings


def settings(request):
    print(f'settings: {request.method}')

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
        'open': 'view',
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
    print(f'add: {request.method}')

    context = {
        'title': 'Додати соціальні показники',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'form_action': 'add_social_settings',
        'buttons': [
            {
                'redirect_button': 'settings',
                'icon_button': 'bi bi-arrow-left-square', # 'bi bi-backspace',
                'title_button': 'Exit',
            },
            {
                'redirect_button': 'add_social_settings',
                'icon_button': 'bi bi-copy me-2',  # 'bi bi-backspace',
                'title_button': 'Копіювати',
            }
        ],
        'content_form': ['base_form.html'],
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
            return render(request, 'base_form.html', context)

    elif request.method == 'GET':
        print(f'method = {request.method}')
        form = SocialSettingsForm()
        context['form'] = form
        # ПЕРЕВІРКА: Чи це HTMX запит?
        if request.headers.get('HX-Request'):
            # Віддаємо тільки таблицю (без меню)
            print('base_form')
            return render(request, 'base_form.html', context)
        else:
            # Якщо звичайний запит — віддаємо сторінку, яка "огортає" таблицю в base.html
            print('base_page_form')
            return render(request, 'base_page_form.html', context)


def edit_social_settings(request, id_social_settings):
    print(f'edit: {request.method}')
    context = {
        'title': 'Редагування соціальних показників',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'form_action': f'editing {id_social_settings}',
        'buttons': [
            {
                'redirect_button': 'settings',
                'icon_button': 'bi bi-backspace',
                'title_button': 'Exit',
            },
            {
                'redirect_button': f'editing {id_social_settings}',
                'icon_button': 'bi bi-save2',
                'title_button': 'Зберегти',
            },
        ],
        'content_form': 'base_form.html',
    }
    if request.method == 'GET':
        print(f'method = {request.method}')
        form = SocialSettingsForm()
        context['form'] = form
        # ПЕРЕВІРКА: Чи це HTMX запит?
        if request.headers.get('HX-Request'):
            # Віддаємо тільки таблицю (без меню)
            print('method GET - base_form_view.html')
            return render(request, 'base_form_view.html', context)
        else:
            # Якщо звичайний запит — віддаємо сторінку, яка "огортає" таблицю в base.html
            print('base_page_form')
            return render(request, 'base_page_form.html', context)

    elif request.method == 'POST':
        print(f'method = {request.method}')
        return HttpResponse(f'Editing f{id_social_settings}')


def view_social_settings(request, id_social_settings):
    print(f'view: {request.method}')
    context = {
        'section_name': 'Налаштування соціальних показників',
        'icon_title': 'bi bi-gear me-2',
        'title': f'Cоціальні показники з id: {id_social_settings}',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'buttons': [
            {
                'redirect_button': 'settings',
                'icon_button': 'bi bi-backspace',
                'title_button': 'Закрити',
            },
            # {
            #     'redirect_button': f'editing {id_social_settings}',
            #     'icon_button': 'bi bi-save2',
            #     'title_button': 'Редагувати',
            # },
            # {
            #     'redirect_button': f'editing {id_social_settings}',
            #     'icon_button': 'bi bi-copy me-2',
            #     'title_button': 'Копіювати',
            # }
        ],
        'content_form': ['base_form_view.html'],
    }
    if request.method == 'GET':
        print(f'method = {request.method}')

    # ПЕРЕВІРКА: Чи це HTMX запит?
    if request.headers.get('HX-Request'):
        # Віддаємо тільки таблицю (без меню)
        print('base_form_view')
        return render(request, 'base_form_view.html', context)
    else:
        # Якщо звичайний запит — віддаємо сторінку, яка "огортає" таблицю в base.html
        print('page_form_social_settings')
        return render(request, 'base_page_form.html', context)

