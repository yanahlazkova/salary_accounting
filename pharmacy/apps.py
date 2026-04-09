from django.apps import AppConfig


class PharmacyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pharmacy'
    verbose_name = 'Ліки в аптеках'

    page_title = "Пошук ліків"

    app_icon = 'bi bi-heart-pulse me-2'

