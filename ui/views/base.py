from dataclasses import dataclass

from ui.mixins.page_toolbar import SectionPageToolbarMixin

@dataclass
class UIBaseView(SectionPageToolbarMixin):
    page_title: str
    page_icon: str

    toolbar_buttons: list[str] | None = None
    page_actions: list[dict] | None = None

