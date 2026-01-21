from dataclasses import field

from django.http import HttpResponse, Http404
from django.shortcuts import render

from persons.forms import PersonForm
from persons.models import Person, Orders


def add_person(request):
    context = {
        'title': 'Фізична особа (створення)',
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'form_action': 'add_person',
        'buttons': [
            {
                'redirect_button': 'personnel',
                'icon_button': 'bi bi-arrow-left-square', # 'bi bi-backspace',
                'title_button': 'Назад',
            },
            {
                'redirect_button': 'personnel',
                'icon_button': 'bi bi-arrow-left-square',  # 'bi bi-backspace',
                'title_button': 'Змінити',
            }
        ]
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
        return render(request, 'page_form_person.html', context)


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


def list_personnel(request):
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
        'current_user': request.user.username if request.user.is_authenticated else 'Гість',
        'table_titles': table_titles,  # ['ПІБ', 'id', 'Стать', 'Співробітник', 'Працює'],
        'table_rows': rows_data,
        # 'editing': 'edit_personnel',  # вказує яку функцію визивати у шаблоні
        # 'button_add': 'add_person',
        # 'button_icon': "bi bi-person-add me-2 text-info",
        'buttons': [
            {
                'redirect_button': 'add_person',  # вказує яку функцію визивати у шаблоні
                'icon_button': "bi bi-person-add me-2 text-info",
                'title_button': 'Додати',
            }],

    }
    if request.headers.get('HX-Request'):
        # Віддаємо контент (без меню)
        return render(request, 'list_personnel.html', context)

    # Якщо звичайний запит — віддаємо сторінку, яка "огортає" контент в base.html
    return render(request, 'page_personnel.html', context)

    return render(request, 'personnel.html', context)


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
