from ui.buttons.registry import UIButtons


from ui.buttons.registry import UIButtons


class SectionPageToolbarMixin:
    toolbar_buttons = ()

    def get_toolbar_buttons(self, actions):
        buttons = []
        # print(f'toolbar_buttons: {self.toolbar_buttons}')

        if self.toolbar_buttons:
            for name in self.toolbar_buttons:
                buttons.append(UIButtons(name).build())
            return buttons

        if actions:
            for action in actions:
                btn = UIButtons(action['action'])

                if 'url' in action:
                    btn.set_url_name(action['url'])

                buttons.append(btn.build())

            return buttons

        return buttons


# class SectionPageToolbarMixin:
#     toolbar_buttons = ()
#
#     def get_toolbar_buttons(self):
#         obj = getattr(self, 'object', None)
#         pk = getattr(obj, 'pk', None)
#
#         buttons = []
#         for btn in self.toolbar_buttons:
#             buttons.append(
#                 UIButtons.build(
#                     name=btn['action'],
#                     url_name=btn['url'],
#                     pk=pk,
#                 )
#             )
#         return buttons
