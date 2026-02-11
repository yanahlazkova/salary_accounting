from dataclasses import dataclass

from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.mixins.section import AppSectionMetaMixin


@dataclass
class UIBaseView(AppSectionMetaMixin):
    page_title: str = None
    page_icon: str = None

    toolbar_buttons: list[str] | None = None
    page_actions: list[dict] | None = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = self.page_title
        ctx["page_icon"] = self.page_icon
        print(f'UIBaseView{ctx}')
        return ctx


