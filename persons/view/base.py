from ui.icons import ICONS
from ui.mixins.mixins import SectionMetaMixin
from ui.mixins.section import AppSectionMixin

class PersonsBaseView(SectionMetaMixin):
    """ дані для сторінок розділу Кадри """
    app_label = 'persons'

    page_titles = {
        'persons': 'Фізичні особи',
        'orders': 'Накази',
        'personal_account': 'Особовий рахунок'
    }
