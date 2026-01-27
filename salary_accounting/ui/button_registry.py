from salary_accounting.ui.buttons import HTMXButton


class HTMXButtons:
    target = "#main-content"
    css_class = "btn btn-outline-info"

    @staticmethod
    def create(url_name, icon, css_class=css_class, target=target):
        icon_create = {
            'plus': 'bi bi-plus-circle me-2',
            'setting': 'bi bi-gear me-2',
            'people': 'bi bi-person-add me-2',
            'archive': 'bi bi-archive me-2',
        }
        return HTMXButton(
            label="Додати",
            icon=icon_create[icon],
            url_name=url_name,
            css_class=css_class,
            hx_target=target,
        )

    @staticmethod
    def edit(url_name, pk, css_class=css_class, target=target):
        return HTMXButton(
            label="Редагувати",
            icon="bi bi-pencil me-2",
            url_name=url_name,
            url_kwargs={"pk": pk},
            css_class=css_class,
            hx_target=target,
        )

    @staticmethod
    def delete(url_name, pk, css_class=css_class, target=target):
        return HTMXButton(
            label="Видалити",
            icon="bi bi-trash",
            url_name=url_name,
            url_kwargs={"pk": pk},
            css_class="btn btn-sm btn-outline-danger",
            hx_method="delete",
            confirm="Видалити запис?",
            hx_target=target,
        )

    @staticmethod
    def view(url_name, pk, css_class=css_class, target=target):
        return HTMXButton(
            label="Перегляд",
            icon="bi bi-eye",
            url_name=url_name,
            url_kwargs={"pk": pk},
            css_class=css_class,
            hx_target=target,
        )

    @staticmethod
    def copy(url_name, pk, css_class=css_class, target=target):
        return HTMXButton(
            label="Копіювати",
            icon="bi bi-copy",
            url_name=url_name,
            url_kwargs={"pk": pk},
            css_class=css_class,
            hx_target=target,
        )

    @staticmethod
    def exit(url_name, css_class=css_class, target=target):
        return HTMXButton(
            label="Закрити",
            icon="bi bi-arrow-left-square",
            url_name=url_name,
            # url_kwargs={"pk": pk}, # для відображення раніше обраного у таблиці
            css_class=css_class,
            hx_target=target,
        )

    @staticmethod
    def save(url_name, pk, css_class=css_class, target=target):
        return HTMXButton(
            label="Зберегти",
            icon="bi bi-floppy",
            url_name=url_name,
            url_kwargs={"pk": pk},
            css_class=css_class,
            hx_target=target,
        )