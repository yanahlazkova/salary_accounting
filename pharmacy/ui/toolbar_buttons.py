from django.apps import apps

from ui.buttons.base import HTMXButton


class ToolbarMixin:
    """ Формує toolbar-кнопки на основі app_icons додатку. """

    app_label: str = None
    toolbar_buttons: list[str] = []  # ['create', 'edit', 'delete']

    def get_section_config(self):
        if not self.app_label:
            raise ValueError("app_label is required")
        return apps.get_app_config(self.app_label)

    def get_app_icons(self) -> dict:
        if not self.app_label:
            return {}

        config = self.get_section_config()
        return getattr(config, 'app_icons', {}) or {}

    def get_toolbar_buttons(self):
        icons = self.get_app_icons()
        # kwargs = self.get_object_url_kwargs()

        buttons = []
        for name in self.toolbar_buttons:
            button = (
                UIButtonsPharmacy(name)
                .set_url_name(self.get_toolbar_url(name))
                # .set_kwargs(kwargs)
                # .set_pk(pk)
                .set_icon(icons.get(name))
                .build()
            )
            buttons.append(button)
        return buttons

    def get_toolbar_url(self, name: str) -> str:
        """ Конвенція імен URL:
               settings:create
               settings:edit
               settings:delete """
        if not self.app_label:
            return '#'
        config = self.get_section_config()
        urls = getattr(config, 'app_urls', {}) or {}
        return f'{self.app_label}:{urls[name]}'


class UIButtonsPharmacy:
    DEFAULT_CSS_CLASS = 'btn btn-outline-info me-2'

    def __init__(self, name: str):
        self.name = name
        self.url_name = '#'
        self.kwargs = {}
        self.icon = None
        self.css_class = self.DEFAULT_CSS_CLASS

    def set_url_name(self, url_name):
        self.url_name = url_name
        return self

    def set_icon(self, icon):
        self.icon = icon
        return self

    def build(self) -> HTMXButton:
        match self.name:
            case 'update_categories':
                return self._update_categories()
            case 'update_drugs':
                return self._update_drugs()

        raise ValueError(f'Кнопка "{self.name}" не існує')

    def _update_categories(self):
        return HTMXButton(
            name='update_categories',
            label="Оновити категорії",
            icon=self.icon or "bi bi-plus-circle",
            url_name=self.url_name,
            # url_kwargs=self.kwargs,
            css_class=self.css_class,
        )

    def _update_drugs(self):
        return HTMXButton(
            name='update_drugs',
            label="Оновити ліки",
            icon=self.icon or "bi bi-plus-circle",
            url_name=self.url_name,
            # url_kwargs=self.kwargs,
            css_class=self.css_class,
        )