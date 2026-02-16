from ui.buttons.base import HTMXButton


class UIButtons:
    DEFAULT_CSS_CLASS = 'btn btn-outline-info me-2'

    def __init__(self, name: str):
        self.name = name
        self.url_name = '#'
        self.pk = None
        self.icon = None
        self.css_class = self.DEFAULT_CSS_CLASS

    def get_name(self):
        return self.name

    def set_url_name(self, url_name):
        self.url_name = url_name
        return self

    def set_pk(self, pk):
        self.pk = pk
        return self

    def set_slug_url_name(self, slug_url_name):
        self.url_name = slug_url_name
        return self

    def set_icon(self, icon):
        self.icon = icon
        return self

    def set_css_class(self, css_class):
        self.css_class = css_class
        return self

        # --------- factory ---------

    def build(self) -> HTMXButton:
        match self.name:
            case 'create':
                return self._create()
            case 'edit':
                return self._edit()
            case 'delete':
                return self._delete()
            case 'view':
                return self._view()
            case 'copy':
                return self._copy()
            case 'exit':
                return self._exit()
            case 'save':
                return self._save()

        raise ValueError(f'Кнопка "{self.name}" не існує')

    def _create(self):
        return HTMXButton(
            name='create',
            label="Додати",
            icon=self.icon or "bi bi-plus-circle",
            url_name=self.url_name,
            css_class=self.css_class,
        )

    def _edit(self):
        return HTMXButton(
            name='edit',
            label="Редагувати",
            icon=self.icon or "bi bi-pencil",
            url_name=self.url_name,
            url_kwargs={"pk": self.pk},
            css_class=self.css_class,
        )

    def _delete(self):
        return HTMXButton(
            name='delete',
            label="Видалити",
            icon=self.icon or "bi bi-trash",
            url_name=self.url_name,
            url_kwargs={"pk": self.pk},
            css_class=self.css_class,
            hx_method="delete",
            confirm="Видалити запис?",
        )

    def _view(self):
        return HTMXButton(
            name='view',
            label="Перегляд",
            icon=self.icon or "bi bi-eye",
            url_name=self.url_name,
            url_kwargs={"pk": self.pk},
            css_class=self.css_class,
        )

    def _copy(self):
        return HTMXButton(
            name='copy',
            label="Копіювати",
            icon=self.icon or "bi bi-copy",
            url_name=self.url_name,
            url_kwargs={"pk": self.pk},
            css_class=self.css_class,
        )

    def _exit(self):
        return HTMXButton(
            name='exit',
            label="Закрити",
            icon=self.icon or "bi bi-arrow-left-square",
            url_name=self.url_name,
            css_class=self.css_class,
        )

    def _save(self):
        return HTMXButton(
            name='save',
            label="Зберегти",
            icon=self.icon or "bi bi-floppy",
            url_name=self.url_name,
            url_kwargs={"pk": self.pk} if self.pk else {},
            css_class=self.css_class,
        )