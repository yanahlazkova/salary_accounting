from django.shortcuts import render, redirect


def settings(request):
    context = {
        'buttons':
            [
                {
                    'title_button': 'Додати',
                    # 'redirect_button': '',
                    'icon_button': 'bi bi-building-add me-2',
                }
            ]
    }

    return render(request, 'page_social_settings.html', context)