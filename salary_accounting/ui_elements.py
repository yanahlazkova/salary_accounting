from dataclasses import dataclass
from django.urls import reverse, NoReverseMatch

@dataclass
class ButtonConfig:
    title_button: str
    icon_button: str
    css_class: str = "btn-outline-info me-2"

# Глобальный справочник стилей кнопок
BUTTON_REGISTRY = {
    'save': ButtonConfig(title_button='Зберегти', icon_button='save'),
    'delete': ButtonConfig(title_button='Видалити', icon_button='trash'),
    'cancel': ButtonConfig(title_button='Відмінити', icon_button='times'),
    'add': ButtonConfig(title_button='Додати', icon_button='plus'),
    'add_setting': ButtonConfig(title_button='Додати', icon_button='bi bi-gear me-2'),
    'add_person': ButtonConfig(title_button='Додати', icon_button='bi bi-person-add me-2'),
    'exit': ButtonConfig(title_button='Закрити', icon_button='bi bi-arrow-left-square me-2'),
    'edit': ButtonConfig(title_button='Редагувати', icon_button='bi bi-pencil-fill me-2'),
    'copy': ButtonConfig(title_button='Копіювати', icon_button='bi bi-copy me-2'),
    'view': ButtonConfig(title_button='Перегляд', icon_button='bi bi-binoculars me-2'),
}