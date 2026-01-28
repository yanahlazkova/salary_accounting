from salary_accounting.ui.buttons import HTMXButton


class UIButtons:

    @staticmethod
    def create(url_name, name_app):
        icon = {
            'person': 'bi bi-person-add me-2',
            'setting': 'bi bi-plus-circle me-2',
            'dictionary': 'bi bi-journal-plus me-2',
        }
        return HTMXButton(
            label="Створити",
            icon=icon[name_app],
            url_name=url_name,
            # css_class="btn btn-success",
        )

    @staticmethod
    def edit(url_name, name_app, pk):
        return HTMXButton(
            label="",
            icon="bi bi-pencil",
            url_name=url_name,
            url_kwargs={"pk": pk},
#             css_class="btn btn-sm btn-outline-primary",
        )

    @staticmethod
    def delete(url_name, name_app, pk):
        return HTMXButton(
            label="",
            icon="bi bi-trash",
            url_name=url_name,
            url_kwargs={"pk": pk},
#             css_class="btn btn-sm btn-outline-danger",
            hx_method="delete",
            confirm="Видалити запис?",
        )

    @staticmethod
    def view(url_name, pk):
        return HTMXButton(
            label="",
            icon="bi bi-eye",
            url_name=url_name,
            url_kwargs={"pk": pk},
#             css_class="btn btn-sm btn-outline-secondary",
#             hx_target=target,
        )

    @staticmethod
    def exit(url_name, name_app):
        icon = {
            'person': 'bi bi-people me-2',
            'setting': 'bi bi-gear me-2',
            'dictionary': 'bi bi-journal-text me-2',
        }
        return HTMXButton(
            label="",
            icon=icon[name_app],
            url_name=url_name,
#             css_class="btn btn-sm btn-outline-primary",
        )
