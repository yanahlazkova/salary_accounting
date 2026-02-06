from ui.buttons.registry import UIButtons


class SectionPageToolbarMixin:
    toolbar_buttons = ()

    def get_toolbar_buttons(self):
        obj = getattr(self, 'object', None)
        pk = getattr(obj, 'pk', None)
        # pk = getattr(self.object, 'pk', None)

        buttons = []
        for btn in self.toolbar_buttons:
            buttons.append(
                UIButtons.build(
                    name=btn['action'],
                    url_name=btn['url'],
                    pk=pk,
                )
            )
        return buttons
