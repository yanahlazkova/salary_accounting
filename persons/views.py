from dataclasses import field

from django.http import HttpResponse, Http404
from django.shortcuts import render

from persons.forms import PersonForm
from persons.models import Person, Orders
from salary_accounting.ui.button_registry import UIButtons


def add_person(request):
    context = {
        'section_name': 'Фізичні особи',
        'title': 'Фізична особа (створення)',
        'icon_title': 'be bi-people me-2',
        'icon_name': 'be bi-person-add me-2',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'form_action': 'add_person',
        'buttons': [
            UIButtons.exit(url_name='personnel'),
            UIButtons.save(url_name='edit_person', pk=1),

            # {
            #     'redirect_button': 'personnel',
            #     'icon_button': 'bi bi-arrow-left-square', # 'bi bi-backspace',
            #     'title_button': 'Назад',
            # },
            # {
            #     'redirect_button': 'add_person',
            #     'icon_button': 'bi bi-copy me-2',  # 'bi bi-backspace',
            #     'title_button': 'Копіювати',
            # }
        ],
        'content_form': 'base_form.html',
    }
    if request.method == 'GET':
        print(f'method = {request.method}')
        form = PersonForm()
        context['form'] = form
    # ПЕРЕВІРКА: Чи це HTMX запит?
    if request.headers.get('HX-Request'):
        # Віддаємо тільки таблицю (без меню)
        print('form_social_settings')
        return render(request, 'base_form.html', context)
    else:
        # Якщо звичайний запит — віддаємо сторінку, яка "огортає" таблицю в base.html
        print('page_form_social_settings')
        return render(request, 'base_page_form.html', context)


def add_order(request):
    return render(request, 'page_form_person.html', {
        'title': 'Наказ (створення)',
        'message': 'Заповніть обов\'язкові поля',
        'redirect_button': 'orders',  # url при закритті сторінки (кнопки Вийти, Зберегти)

    })


def edit_personnel(request, personnel_id):
    # return render(request, 'edit_order.html', {})
    return HttpResponse(f'Фізична особа id: {personnel_id}')


def edit_order(request, order_id):
    return HttpResponse(f'Наказ id: {order_id}')


def personnel(request):
    data_db = Person.objects.all().values()
    table_titles = [f.name for f in Person._meta.get_fields()]
    rows_data = []
    for obj in data_db:
        rows_data.append({
            'id': obj['id'],  # Звернення через дужки (словник)
            'values': [obj.get(f.name) for f in Person._meta.fields]
        })
    context = {
        'title': 'Фізичні особи',
        'icon_title': 'be bi-people me-2',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'table_titles': table_titles,  # ['ПІБ', 'id', 'Стать', 'Співробітник', 'Працює'],
        'table_rows': rows_data,
        # 'editing': 'edit_personnel',  # вказує яку функцію визивати у шаблоні
        # 'button_add': 'add_person',
        # 'button_icon': "bi bi-person-add me-2 text-info",
        'buttons': [
            UIButtons.create(url_name='add_person', name_app='person'),
        ],
        'contents': ['base_table.html'],

    }
    if request.headers.get('HX-Request'):
        print('base_content.html')
        # Віддаємо контент (без меню)
        return render(request, 'base_content.html', context)

    # Якщо звичайний запит — віддаємо сторінку, яка "огортає" контент в base.html
    print('base_page.html')
    return render(request, 'base_page.html', context)

def view_person(request, pk):
    person = Person.objects.get(pk=pk)
    context = {
        'section_name': 'Налаштування соціальних показників',
        'icon_title': 'bi bi-gear me-2', 'title': 'Додати соціальні показники',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'form_action': 'add_social_settings',
        'buttons': [
            UIButtons.exit(url_name='settings'),
            # UIButtons.view(url_name='view_person', pk=pk),
            # UIButtons.save(url_name='save', pk=pk)
        ],
        'content_form': ['base_form.html'],
    }

def list_orders(request):
    table_titles = [f.name for f in Orders._meta.get_fields()]
    context = {
        'title': 'Накази',
        'table_titles': table_titles,
        'table_rows': {'first': ['5-к', '2010-02-03', 'прийняття на посаду', 'Кадри. Прийняття'],
                       'second': ['1-к', '2010-02-03', 'прийняття на посаду', 'Кадри. Прийняття'],
                       'third': ['1-к', '2010-02-03', 'прийняття на посаду', 'Кадри. Прийняття'],
                       'fourth': ['5-к', '2010-02-03', 'прийняття на посаду', 'Кадри. Прийняття'],
                       'fifth': ['5-к', '2010-02-03', 'прийняття на посаду', 'Кадри. Прийняття']},
        'editing': 'edit_order',  # вказує яку функцію визивати у шаблоні
        'button_add': 'add_order',
        'button_icon': "bi bi-file-earmark-plus text-info",

    }
    return render(request, 'list_orders.html', context)
