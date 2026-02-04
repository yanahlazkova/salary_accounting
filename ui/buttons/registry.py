from unittest import case

from ui.buttons.base import HTMXButton


class UIButtons:
    @staticmethod
    def build(name, url_name, pk=None, icon=None):
        match name:
            case 'create':
                return UIButtons.create(url_name, icon)
            case 'edit':
                return UIButtons.edit(url_name, pk, icon)
            case 'delete':
                return UIButtons.delete(url_name, pk, icon)
            case 'view':
                return UIButtons.view(url_name, pk, icon)
            case 'copy':
                return UIButtons.copy(url_name, pk, icon)
            case 'exit':
                return UIButtons.exit(url_name, icon)
            case 'save':
                return UIButtons.save(url_name, pk, icon)

        print('Помилка - кнопки не існує')
        return 'Error'

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