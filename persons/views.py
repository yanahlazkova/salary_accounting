from django.http import HttpResponse
from django.shortcuts import render


def personnel(request):
    print('Hello!!!')
    return HttpResponse(f'Personnel Page, {request.user.username if request.user.is_authenticated else 'Goose'}')
