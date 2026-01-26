from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from salary_accounting.ui.button_registry import HTMXButtons
from .forms import SocialSettingsForm
from .models import SocialSettings


def settings(request):
    print(f'settings: {request.method}')

    data_db = SocialSettings.objects.all().values()  # .order_by('-effective_from')
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
        'buttons': [HTMXButtons.create(
            url_name='add_social_settings',
            icon='setting')

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

    # Якщо звичайний запит — віддаємо сторінку, яка "огортає" контент в base.html
    return render(request, 'base_page.html', context)


def add_social_settings(request):
    print(f'add: {request.method}')
    button_view = HTMXButtons.view(url_name='view', pk=1)
    context = {
        'section_name': 'Налаштування соціальних показників',
        'icon_title': 'bi bi-gear me-2','title': 'Додати соціальні показники',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'form_action': 'add_social_settings',
        'buttons': [
            HTMXButtons.exit(url_name='settings'),
            button_view,
            HTMXButtons.save(url_name='save', pk=1)
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
        button_view.disabled = True

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


def edit_social_settings(request, pk):
    print(f'edit: {request.method}')
    data_db = SocialSettings.objects.get(id=pk)
    context = {
        'section_name': 'Налаштування соціальних показників',
        'icon_title': 'bi bi-gear me-2',
        'title': f'Редагування соціальні показники з id: {pk}',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'form_action': 'edit',
        'data': data_db,
        'buttons': [
            HTMXButtons.exit(url_name='settings'),
            HTMXButtons.view(url_name='view', pk=pk),
            HTMXButtons.save(url_name='save', pk=pk),
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
            print('method GET - base_form.html')
            return render(request, 'base_form.html', context)
        else:
            # Якщо звичайний запит — віддаємо сторінку, яка "огортає" таблицю в base.html
            print('base_page_form')
            return render(request, 'base_page_form.html', context)

    elif request.method == 'POST':
        print(f'method = {request.method}')
        return HttpResponse(f'Editing f{pk}')


def view_social_settings(request, pk):
    print(f'view: {request.method}')
    data_db = SocialSettings.objects.get(id=pk)
    context = {
        'section_name': 'Налаштування соціальних показників',
        'icon_title': 'bi bi-gear me-2',
        'title': f'Cоціальні показники з id: {pk}',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'data': data_db,
        'buttons': [
            HTMXButtons.exit(url_name='settings'),
            HTMXButtons.edit(url_name='edit', pk=pk),
            # HTMXButtons.copy(url_name='edit', pk=pk),
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
            print('base_page_form')
            return render(request, 'base_page_form.html', context)
    elif request.method == 'POST':
        print(f'method = {request.method}')

        return HttpResponse(f'Editing method POST (id: f{pk})')

def save_social_settings(request, pk):
    print(f'save: {request.method}')
    data_db = SocialSettings.objects.get(id=pk)
    context = {
        'section_name': 'Налаштування соціальних показників',
        'icon_title': 'bi bi-gear me-2',
        'title': f'Cоціальні показники з id: {pk}',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'data': data_db,
        'buttons': [
            HTMXButtons.exit(url_name='settings'),
            HTMXButtons.edit(url_name='edit', pk=pk),
            # HTMXButtons.copy(url_name='edit', pk=pk),
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
            print('base_page_form')
            return render(request, 'base_page_form.html', context)
    elif request.method == 'POST':
        print(f'method = {request.method}')

        return HttpResponse(f'Saving method POST (id: f{pk})')
