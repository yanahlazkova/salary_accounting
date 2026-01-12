from django.http import HttpResponse, Http404
from django.shortcuts import render


def add_person(request):
    return render(request, 'person.html', {
        'title': 'Фізична особа (створення)',
        'message': 'Заповніть обов\'язкові поля',
        'redirect_button': 'personnel',
    })


def add_order(request):
    return render(request, 'person.html', {
        'title': 'Наказ (створення)',
        'message': 'Заповніть обов\'язкові поля',
        'redirect_button': 'orders', # url при закритті сторінки (кнопки Вийти, Зберегти)

    })


def edit_personnel(request, personnel_id):
    # return render(request, 'edit_order.html', {})
    return HttpResponse(f'Фізична особа id: {personnel_id}')


def edit_order(request, order_id):
    return HttpResponse(f'Наказ id: {order_id}')


def list_personnel(request):
    return render(request, 'personnel.html', {
        'title': 'Фізичні особи',
        'table_titles': ['ПІБ', 'id', 'Стать', 'Співробітник', 'Працює'],
        'table_rows': {'first': ['id-first', 'Стать-first', 'Співробітник-first', 'Працює-first'],
                       'second': ['id-second', 'Стать-second', 'Співробітник-second', 'Працює-second'],
                       'third': ['id-third', 'Стать-third', 'Співробітник-third', 'Працює-third'],
                       'fourth': ['id-fourth', 'Стать-fourth', 'Співробітник-fourth', 'Працює-fourth'],
                       'fifth': ['id-fifth', 'Стать-fifth', 'Співробітник-fifth', 'Працює-fifth']},
        'editing': 'edit_personnel',  # вказує яку функцію визивати у шаблоні
        'button_add': 'add_person',
        'button_icon': "bi bi-person-add me-2 text-info",

    })


def list_orders(request):
    return render(request, 'list_orders.html', {
        'title': 'Накази',
        'table_titles': ['id', 'Номер', 'Дата', 'Короткий зміст', 'Тип наказу'],
        'table_rows': {'first': ['5-к', '2010-02-03', 'прийняття на посаду', 'Кадри. Прийняття'],
                       'second': ['1-к', '2010-02-03', 'прийняття на посаду', 'Кадри. Прийняття'],
                       'third': ['1-к', '2010-02-03', 'прийняття на посаду', 'Кадри. Прийняття'],
                       'fourth': ['5-к', '2010-02-03', 'прийняття на посаду', 'Кадри. Прийняття'],
                       'fifth': ['5-к', '2010-02-03', 'прийняття на посаду', 'Кадри. Прийняття']},
        'editing': 'edit_order',  # вказує яку функцію визивати у шаблоні
        'button_add': 'add_order',
        'button_icon': "bi bi-file-earmark-plus text-info",

    })
