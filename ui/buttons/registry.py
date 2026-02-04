from unittest import case

from ui.buttons.base import HTMXButton


class UIButtons:
    def __init__(self, name_button, url_name, icon=None, pk=None):
        self.url_name = url_name
        self.icon = icon
        self.pk = pk
        self.name_button = name_button
        match self.name_button:
            case 'create': self.create(self.url_name, self.icon)
            case 'edit': self.edit(self.url_name, self.pk, self.icon)
            case 'delete': self.delete(self.url_name, self.pk, self.icon)
            case 'view': self.view(self.url_name, self.pk, self.icon)
            case 'copy': self.copy(url_name, self.pk, self.icon)
            case 'exit': self.exit(url_name, self.icon)
            case 'save': self.save(url_name, self.pk, self.icon)

    @staticmethod
    def create(url_name, icon=None):
        return HTMXButton(
            label="Додати",
            icon=icon or 'bi bi-plus-circle',
            url_name=url_name,
            # css_class=css_class,
            # hx_target=target,
        )

    @staticmethod
    def edit(url_name, pk, icon=None):
        return HTMXButton(
            label="Редагувати",
            icon=icon or "bi bi-pencil me-2",
            url_name=url_name,
            url_kwargs={"pk": pk},
#             css_class=css_class,
#             hx_target=target,
        )

    @staticmethod
    def delete(url_name, pk, icon=None):
        return HTMXButton(
            label="Видалити",
            icon=icon or "bi bi-trash",
            url_name=url_name,
            url_kwargs={"pk": pk},
#             css_class="btn btn-sm btn-outline-danger",
            hx_method="delete",
            confirm="Видалити запис?",
#             hx_target=target,
        )

    @staticmethod
    def view(url_name, pk, icon=None):
        return HTMXButton(
            label="Перегляд",
            icon=icon or "bi bi-eye",
            url_name=url_name,
            url_kwargs={"pk": pk},
#             css_class=css_class,
#             hx_target=target,
        )

    @staticmethod
    def copy(url_name, pk, icon=None):
        return HTMXButton(
            label="Копіювати",
            icon=icon or "bi bi-copy",
            url_name=url_name,
            url_kwargs={"pk": pk},
#             css_class=css_class,
#             hx_target=target,
        )

    @staticmethod
    def exit(url_name, icon=None):
        return HTMXButton(
            label="Закрити",
            icon=icon or "bi bi-arrow-left-square",
            url_name=url_name,
            # url_kwargs={"pk": pk}, # для відображення раніше обраного у таблиці
#             css_class=css_class,
#             hx_target=target,
        )

    @staticmethod
    def save(url_name, pk, icon=None):
        return HTMXButton(
            label="Зберегти",
            icon=icon or "bi bi-floppy",
            url_name=url_name,
            url_kwargs={"pk": pk},
#             css_class=css_class,
#             hx_target=target,
        )