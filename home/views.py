# home/views.py

from django.views.generic import ListView
from django.utils import timezone
from datetime import datetime, date  # ⬅️ КОРЕКТНИЙ ІМПОРТ date
import feedparser
from django.core.cache import cache

# ... (інші імпорти)

# --- Конфігурація ---
RSS_URL = 'https://buhgalter.com.ua/rss-for-users.rss'
NEWS_LIMIT = 20


# def listBuh(request):
#     feed = feedparser.parse(RSS_URL)
#     year = getattr(feed.entries[0], 'published_parsed').tm_year
#     print(year)

# --------------------

class Home(ListView):
    """
    Представлення для відображення головної сторінки.
    """
    template_name = 'home.html'
    context_object_name = 'latest_news'

    def get_queryset(self):  # ⬅️ Метод класу
        # Спроба отримати новини з кешу
        cached_news = cache.get('latest_rss_news')
        if cached_news:
            return cached_news

        # Якщо в кеші немає, завантажуємо з RSS...
        feed = feedparser.parse(RSS_URL)

        news_list = []
        today = date.today()  # ⬅️ Отримуємо поточну дату

        for entry in feed.entries:

            # Парсинг дати з формату RSS
            pub_date_dt = timezone.now()  # Об'єкт datetime (за замовчуванням)
            try:
                # Конвертуємо структуру time.struct_time у Python datetime object
                pub_date_dt = datetime(*entry.published_parsed[:6])
            except (AttributeError, TypeError):
                pass

            # Отримання категорії та опису з RSS (Якщо поля відсутні, використовуємо безпечне значення)
            category_term = entry.tags[0].term if hasattr(entry, 'tags') and entry.tags else 'Загальна'
            description_text = getattr(entry, 'summary', getattr(entry, 'description', 'Опис відсутній.'))

            # Створюємо словник
            news_list.append({
                'is_new': pub_date_dt.date() == today,  # ⬅️ Порівнюємо дату публікації з сьогоднішньою
                'title': getattr(entry, 'title', 'Без заголовка'),
                'link': getattr(entry, 'link', '#'),
                'description': description_text,
                'publication_date': pub_date_dt,
                # ⬅️ Передаємо об'єкт datetime, щоб можна було форматувати час у шаблоні
                'category': category_term,
            })

        # Зберігаємо результат у кеші на 3600 секунд (1 година)
        cache.set('latest_rss_news', news_list, 3600)
        return news_list

    def get_context_data(self, **kwargs):  # ⬅️ Метод класу
        """
        Додаємо статичну інформацію (закони та соц. показники) до контексту.
        """
        context = super().get_context_data(**kwargs)
        # ... (логіка додавання social_indicators та laws_and_regulations)

        # 1. Ключові соціальні показники
        context['social_indicators'] = {
            'current_year': timezone.now().year,
            'min_salary_monthly': '8 000 грн',
            'pm_for_able_bodied': '3 028 грн',
            'pdfo_rate': '18%',
            'vz_rate': '5%',  # Згідно з трудовим законодавством
            'esv_rate': '22%',
            }

        # 2. Основні закони та нормативи
        context['laws_and_regulations'] = [
            {
                'title': 'Кодекс законів про працю України (КЗпП)',
                'description': 'Регулює трудові відносини.',
                'link': 'https://zakon.rada.gov.ua/laws/show/322-08',
            },
            {
                'title': 'Закон України "Про Державний бюджет України на 2025 рік"',
                'description': 'Встановлює МЗП та ПМ.',
                'link': '#',
            },
        ]

        return context