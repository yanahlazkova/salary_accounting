from django.apps import AppConfig


class PharmacyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pharmacy'
    verbose_name = 'Ліки в аптеках'

    page_title = "Пошук ліків"

    app_icon = 'bi bi-heart-pulse me-2'
    app_icons = {
        'update_category': 'bi bi-heart-pulse',
        'update_drugs': 'bi bi-heart-pulse',
    }
    list_app_icons = [{
        'update_category': 'update_category',
        'update_drugs': 'update_drugs',
    }]

    app_urls = {
        'update_categories': 'update_categories',
        'update_drugs': 'update_categories',
    }


