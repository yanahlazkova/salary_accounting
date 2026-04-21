# # https://apteka911.ua/robots.txt
# # https://www.add.ua/robots.txt - аптека доброго дня
# # https://1sa.com.ua/robots.txt
#
# """ sitemap.xml — це файл для пошукових роботів (Google),
# який містить посилання на всі сторінки сайту"""
# from pharmacy.models import Drug
#
# pharmacy = {
#     'apteka911': 'https://apteka911.ua/sitemap.xml',
#     'add': 'https://1sa.com.ua/sitemap.xml',
#     '1sa': 'https://www.add.ua/sitemap.xml',
# }
#
# city = {
#     'apteka911': 'borispol',
# }
#
# # Нижче наведено скрипт на Python, який автоматично:
# # Завантажує головний sitemap.xml.
# # Знаходить у ньому всі посилання на архіви товарів (.xml.gz). (для apteka911)
# # Розпаковує їх «на льоту» (без збереження на диск, щоб економити місце).
# # Витягує унікальні коди товарів за допомогою регулярних виразів.
#
# import requests
# import gzip
# import xml.etree.ElementTree as ET
# import re
# from io import BytesIO
# from fake_useragent import UserAgent
#
#
#
# def get_unique_drug_codes_apteka911():
#     ua = UserAgent()
#     main_sitemap_url = pharmacy['apteka911']
#     headers = {
#         'User-Agent': ua.random,
#         # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
#     }
#
#     # Набір (set) автоматично видаляє дублікати
#     unique_codes = set()
#
#     # Регулярний вираз для пошуку коду типу "p12181" або "d1099" у URL
#     # Шукаємо частину, що йде після назви ліків (наприклад, -p12181 або -d1099)
#     code_pattern = re.compile(r'-([pd]\d+)')
#
#     print(f"--- Завантаження головного sitemap ---")
#     try:
#         response = requests.get(main_sitemap_url, headers=headers)
#         response.raise_for_status()
#
#         root = ET.fromstring(response.content)
#         namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
#
#         # Шукаємо всі посилання на вкладені карти (sitemaps)
#         sitemaps = root.findall('ns:sitemap/ns:loc', namespace)
#
#         for sitemap_url in sitemaps:
#             url_text = sitemap_url.text
#
#             # Нас цікавлять лише архіви з ліками (cities)
#             # if 'drugs-manual' in url_text and url_text.endswith('.gz'):
#             if 'cities' in url_text and url_text.endswith('gz'):
#                 print(f"Обробка архіву: {url_text.split('/')[-1]}")
#
#                 gz_response = requests.get(url_text, headers=headers)
#
#                 # Розпаковуємо GZIP у пам'яті
#                 with gzip.GzipFile(fileobj=BytesIO(gz_response.content)) as f:
#                     gz_xml_content = f.read()
#                     inner_root = ET.fromstring(gz_xml_content)
#
#                     for url_tag in inner_root.findall('ns:url/ns:loc', namespace):
#                         full_url = url_tag.text
#                         print(f'==: {full_url.split("/")[-1]}: {city['apteka911']}')
#
#                         if city['apteka911'] in full_url:
#                             print(f'==?: {full_url.split("/")[-1] == city["apteka911"]}')
#
#                             # Витягуємо код із URL (наприклад, з /asparkam-p12181/ беремо p12181)
#                             match = code_pattern.search(full_url)
#                             if match:
#                                 unique_codes.add(match.group(1))
#
#     except Exception as e:
#         print(f"Помилка під час виконання: {e}")
#
#     return unique_codes
#
#
# # Запуск
# # codes = get_unique_drug_codes_apteka911()
# # print(f"\n--- ГОТОВО ---")
# # print(f"Знайдено унікальних товарів: {len(codes)}")
# # print(f"Приклади кодів: {list(codes)[:10]}")
# #
# # # Збереження у файл для подальшої роботи
# # with open("drug_codes.txt", "w") as f:
# #     for code in sorted(codes):
# #         f.write(code + "\n")
#
# import time
# import random
#
#
# def sync_drugs_from_sitemap():
#     ua = UserAgent()
#     session = requests.Session()
#
#     # Посилання на один із архівів товарів (можна автоматизувати перебір усіх)
#     sitemap_url = "https://apteka911.ua/content/sitemap/sitemap-drugs-manual-0.xml.gz"
#     api_url = "https://apteka911.ua/ua/shop/search"
#
#     headers_base = {
#         'accept': 'application/json, text/javascript, */*; q=0.01',
#         'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'x-requested-with': 'XMLHttpRequest',
#         'origin': 'https://apteka911.ua'
#     }
#
#     print("--- Завантаження карти сайту ---")
#     response = session.get(sitemap_url, headers={'User-Agent': ua.random})
#
#     with gzip.GzipFile(fileobj=BytesIO(response.content)) as f:
#         root = ET.fromstring(f.read())
#         namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
#         # Беремо перші 100 для тесту, щоб не чекати вічність
#         urls = [url.find('ns:loc', namespace).text for url in root.findall('ns:url', namespace)][:100]
#
#     print(f"Знайдено {len(urls)} посилань. Починаємо імпорт...")
#
#     for full_url in urls:
#         # Витягуємо аліас (наприклад, /ua/shop/asparkam-p12181)
#         alias = "/" + "/".join(full_url.split("/")[3:])
#
#         # Перевіряємо, чи немає вже такого коду в базі, щоб не дублювати запити
#         drug_code = alias.split('-')[-1].strip('/')
#         if Drug.objects.filter(code=drug_code).exists():
#             continue
#
#         # Змінюємо User-Agent для кожного запиту
#         headers = headers_base.copy()
#         headers['User-Agent'] = ua.random
#         headers['referer'] = full_url
#
#         payload = {
#             'pushHistory': 'true',
#             'alias': alias
#         }
#
#         try:
#             # ЗАПИТ ДО API ЗА КИРИЛИЧНОЮ НАЗВОЮ
#             res = session.post(api_url, headers=headers, data=payload, timeout=10)
#             if res.status_code == 200:
#                 json_data = res.json()
#
#                 # Витягуємо назву з JSON (поле 'name' в історії)
#                 history = json_data.get('data', {}).get('history', [])
#                 if history:
#                     real_name = history[0].get('name')  # ОСЬ НАША КИРИЛИЦЯ
#
#                     # Зберігаємо в Django базу
#                     Drug.objects.update_or_create(
#                         code=drug_code,
#                         defaults={
#                             'name': real_name,
#                             'alias': alias
#                         }
#                     )
#                     print(f"Збережено: {real_name} ({drug_code})")
#
#             # ЕМУЛЯЦІЯ ПОВЕДІНКИ ЛЮДИНИ: пауза між товарами
#             wait_time = random.uniform(1.5, 4.0)
#             time.sleep(wait_time)
#
#         except Exception as e:
#             print(f"Помилка на {alias}: {e}")
#             time.sleep(10)  # Довша пауза при помилці
#
#     print("Синхронізація завершена!")
import os
import django

# Вкажіть назву вашого проєкту (замість 'myproject' назва папки, де лежить settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salary_accounting.settings')
django.setup()

# ТІЛЬКИ ПІСЛЯ ЦЬОГО можна імпортувати моделі

import gzip
import random
import time
import xml.etree.ElementTree as ET
from io import BytesIO
import requests
from fake_useragent import UserAgent

from pharmacy.models import Drug_apteka911, CategoryApteka911


# def get_drugs_apteka911_by_category(session, target_url, headers):
#     print(f'full_url: {target_url}')
#     try:
#         response = session.get(target_url, headers=headers, timeout=10)
#         if response.status_code == 200:
#             json_data = response.json()
#             return json_data.get('data', {}).get('ajax_products', [])
#         else:
#             print(f"Помилка: {response.status_code}")
#             return []
#
#
#     except Exception as e:
#         print(f"Помилка API: {e}")
#         time.sleep(10)
#         return []

# from your_app.models import Drug # Переконайтеся, що модель імпортована

# def get_drugs_apteka911_from_sitemap():
#     LIST_DRUGS = []
#
#     # 1. Ініціалізація генератора юзер-агентів
#     ua = UserAgent()
#     session = requests.Session()
#
#     sitemap_url = 'https://apteka911.ua/sitemap.xml'
#     api_url = "https://apteka911.ua/ua/shop/search"
#     origin_url = 'https://apteka911.ua'
#
#     headers_base = {
#         'accept': 'application/json, text/javascript, */*; q=0.01',
#         'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'x-requested-with': 'XMLHttpRequest',
#         'origin': origin_url
#     }
#
#     print(f"--- Підготовка: Завантаження існуючих кодів з БД ---")
#     # 2. ОПТИМІЗАЦІЯ БД: Отримуємо всі існуючі коди одним запитом
#     # values_list('code', flat=True) повертає плоский список, який ми конвертуємо в set для миттєвого пошуку O(1)
#     # existing_codes = set(Drug.objects.values_list('code', flat=True))
#     # print(f"У базі вже є {len(existing_codes)} записів.")
#
#     print(f"--- Завантаження головного sitemap ---")
#
#     processed_count = 0  # 1. Ініціалізуємо лічильник перед початком циклів
#
#     try:
#         # 3. Додано timeout для безпеки
#         response = session.get(sitemap_url, headers={'User-Agent': ua.random}, timeout=15)
#         response.raise_for_status()  # Перевірка на помилки 404, 500
#
#         root = ET.fromstring(response.content)
#         namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
#
#         sitemaps = root.findall('ns:sitemap/ns:loc', namespace)
#
#         for sitemap_tag in sitemaps:
#             url_text = sitemap_tag.text
#
#             if 'filters' in url_text and url_text.endswith('gz'):
#                 print(f"Відкриваємо архів: {url_text}")
#
#                 try:
#                     # Додано timeout для архіву
#                     gz_response = session.get(url_text, headers={'User-Agent': ua.random}, timeout=20)
#                     gz_response.raise_for_status()
#
#                     # Безпечне розпакування у пам'яті
#                     with gzip.GzipFile(fileobj=BytesIO(gz_response.content)) as f:
#                         inner_root = ET.fromstring(f.read())
#
#                     random_count = random.randint(80, 120)
#
#                     for url_tag in inner_root.findall('ns:url/ns:loc', namespace):
#                         target_url = url_tag.text
#                         print(f'full_url: {target_url}')
#
#                         headers = headers_base.copy()
#
#                         headers.update({
#                             "referer": f"https://apteka911.ua/ua",
#                             "user-agent": ua.random,
#                         })
#
#                         session.cookies.update({
#                             'site_version': 'desktop',
#                             'wucmf_region': '89',
#                             # 'PHPSESSID': '601c139cc7ac20fdcbecfdfd55095eb8' - може змінюватись
#                         })
#
#                         page_number = 1
#                         # target_url = 'https://apteka911.ua/shop/lekarstvennyie-preparatyi/ot_boli_v_gorle'
#                         full_url = f'{target_url}/page={page_number}'
#
#                         try:
#                             res = session.get(target_url, headers=headers, timeout=10)
#                             if res.status_code == 200:
#                                 json_data = res.json()
#                                 # отримаємо кількість сторінок
#                                 full_pages = json_data.get('data', {}).get('pages', {}).get('npages', 1)
#                                 products = json_data.get('data', {}).get('ajax_products', [])
#                                 add_to_database(products)
#
#                                 print(f'Count pages: {full_pages}')
#                                 # якщо кількість сторінок більше 1, змінемо target_url і знов виконаємо запит
#                                 if full_pages > 1:
#                                     for page in range(2, full_pages+1):
#                                         full_url = f'{target_url}/page={page}'
#                                         products = get_drugs_apteka911_by_category(session, full_url, headers)
#                                         add_to_database(products)
#
#                                 processed_count += 1
#
#
#                             else:
#                                 print(f"Помилка: {res.status_code}")
#
#                             # 3. ПЕРЕВІРКА: кожні 100 препаратів
#                             if processed_count % random_count == 0:
#                                 random_count = random.randint(80, 120)
#                                 long_wait = random.uniform(30, 60)  # Пауза на 30-60 секунд
#                                 print(
#                                     f"--- Оброблено {processed_count} товарів. Велика пауза: {long_wait:.1f} сек. ---")
#                                 time.sleep(long_wait)
#                             else:
#                                 # Звичайна пауза між запитами
#                                 time.sleep(random.uniform(5, 15))
#                             # else:
#                             #     print(f"УВАГА: Для  історія порожня. Можливо, alias невірний.")
#
#                         except Exception as e:
#                             print(f"Помилка API: {e}")
#                             time.sleep(10)
#
#                 except Exception as e:
#                     print(f"Помилка завантаження/розпакування архіву {url_text}: {e}")
#
#         print("--- Синхронізація успішно завершена! ---")
#
#     except Exception as e:
#         print(f"Критична помилка під час виконання: {e}")
#
#     return LIST_DRUGS

# def add_to_database(list_drugs):
#
#     for drug in list_drugs:
#         Drug_apteka911.objects.update_or_create(
#             productID=drug.get('productID'),
#             defaults={
#                 'productName': drug.get('productName'),
#                 'alias': drug.get('alias'),
#                 'brandName': drug.get('brandName'),
#                 'formName': drug.get('formName'),
#                 'productAvail': True if drug.get('productAvail') == 'yes' else False,
#                 'productCountry': drug.get('productCountry'),
#                 'productForm': drug.get('productForm'),
#                 'productMeasure': drug.get('productMeasure'),
#                 'productMname': drug.get('productMname'),
#                 'productPrice': drug.get('productPrice'),
#                 'img': f"https://apteka911.ua{drug.get('dataUrl', '')}{drug.get('productThumbs', {}).get('webpmid', {}).get('file', '')}",
#             }
#     )
#
#
#
# # Запуск
# list_drugs = get_drugs_apteka911_from_sitemap()
# # add_to_database(list_drugs)
# print(f"\n--- ГОТОВО ---")
# print(f"Знайдено унікальних товарів: {len(codes)}")
# print(f"Приклади кодів: {list(codes)[:10]}")
#
# # Збереження у файл для подальшої роботи
# with open("drug_codes.txt", "w") as f:
#     for code in sorted(codes):
#         f.write(code + "\n")

#
# fetch("https://apteka911.ua/ua/shop/search", {
#   "headers": {
#     "accept": "application/json, text/javascript, */*; q=0.01",
#     "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,uk;q=0.6",
#     "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
#     "priority": "u=1, i",
#     "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "x-requested-with": "XMLHttpRequest"
#   },
#   "referrer": "https://apteka911.ua/ua/drugs/glitsin-d803",
#   "body": "pushHistory=true&alias=%2Fdrugs%2Fglitsin-d803",
#   "method": "POST",
#   "mode": "cors",
#   "credentials": "include"
# });

import requests
#
#
# def test_single_request():
#     ua = UserAgent()
#     session = requests.Session()
#     base_url = "https://apteka911.ua/ua/"
#
#     # # Спробуйте саме цей alias, він перевірений
#     # target_alias = "/drugs/glyukozamin-d811"
#     # # target_alias = "/drugs/glitsin-d803"
#
#     session.get(base_url, headers={"User-Agent": ua.random})
#
#     headers = {
#         "accept": "application/json, text/javascript, */*; q=0.01",
#         "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
#         "x-requested-with": "XMLHttpRequest", # КРИТИЧНО: саме це каже серверу віддати JSON
#         # Referer має бути ПОВНИМ URL сторінки препарату
#         "referer": f"https://apteka911.ua/ua",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#     }
#
#     # Спробуйте спочатку БЕЗ куків, якщо не вийде — додайте PHPSESSID з браузера
#     session.cookies.update({
#         'site_version': 'desktop',
#         'wucmf_region': '89',
#         # 'PHPSESSID': '601c139cc7ac20fdcbecfdfd55095eb8'
#     })
#
#     page_number = 1
#     # target_url = f"https://apteka911.ua/ua/shop/lekarstvennyie-preparatyi/ot_boli_v_gorle/page={page_number}"
#     target_url = f'https://apteka911.ua/shop/lekarstvennyie-preparatyi/glyukosat-ot_boli_v_myishtsah_i_sustavah/page={page_number}'
#
#     response = session.get(target_url, headers=headers, timeout=10)
#
#
#     if response.status_code == 200:
#         data_json = response.json()
#         products = data_json['data'].get('ajax_products', [])
#
#         for item in products:
#             name = item.get('productName')
#             price = item.get('productPrice')
#             print(f"Товар: {name} | Ціна: {price} грн")
#         print(f'All pages: {data_json['data']['pages'].get('page')}')
#         print(f'len: {len(products)}')
#
#     else:
#         print(f"Помилка: {response.status_code}")


# test_single_request()

""" зупинилися на https://apteka911.ua/shop/lekarstvennyie-preparatyi/dinorik-beta_blokatoryi/page=1 """

def get_or_create_category(url_category):
    name = url_category.rstrip('/').split('/')[-1]
    category, _ = CategoryApteka911.objects.update_or_create(
        url=url_category,
        defaults={"name": name},
    )
    return category


def is_valid_category(url: str) -> bool:
    slug = url.rstrip('/').split('/')[-1]

    # відсікаємо фільтри
    if slug.count('-') > 0:
        return False

    return True


def get_all_category():
    ua = UserAgent()
    session = requests.Session()

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://apteka911.ua',
    }

    session.cookies.update({
        'site_version': 'desktop',
        'wucmf_region': '89',
    })

    drugs = []
    seen_ids = set()

    sitemap_url = 'https://apteka911.ua/sitemap.xml'

    res = session.get(sitemap_url, headers={'User-Agent': ua.random}, timeout=15)
    root = ET.fromstring(res.content)

    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    for sitemap in root.findall('ns:sitemap/ns:loc', namespace):
        url = sitemap.text

        if 'filters-1' not in url or not url.endswith('.gz'):
            continue

        print(f"[SITEMAP] {url}")

        gz = session.get(url, timeout=20)

        with gzip.GzipFile(fileobj=BytesIO(gz.content)) as f:
            inner_root = ET.fromstring(f.read())

        for loc in inner_root.findall('ns:url/ns:loc', namespace):
            category_url = loc.text
            list_category = []

            # перевірка це категорія чи фільтр
            if not is_valid_category(category_url):
                continue
            else:
                # отримаємо або додамо категорію
                category = get_or_create_category(category_url)
                # list_category.append(category.url)

                headers.update({
                    "referer": "https://apteka911.ua/ua",
                    "user-agent": ua.random,
                })
                category_url_page1 = f'{category_url}/page=1'

                category_drugs = parse_category(session, category, category_url_page1, headers)

                for drug in category_drugs:
                    pid = drug.get('productID')

                    if pid and pid not in seen_ids:
                        seen_ids.add(pid)
                        drugs.append(drug)

                time.sleep(random.uniform(3, 8))

    return drugs


def parse_category(session, category, url_page1, headers):
    """ Парсинг категорії (ключове місце) """
    print(f'url_category: {category.url}')
    drugs = []

    try:
        res = session.get(url_page1, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()

        pages = data.get('data', {}).get('pages', {}).get('npages', 1)

        # ✅ ДОДАЄМО ПЕРШУ СТОРІНКУ
        products = data.get('data', {}).get('ajax_products', [])
        save_drugs(products, category)

        # drugs.extend(products)


        # ✅ ІНШІ СТОРІНКИ
        for page in range(2, pages + 1):
            page_url = f"{category.url}/page={page}"
            page_products = get_drugs_apteka911_by_category(session, page_url, headers)
            # drugs.extend(page_products)
            save_drugs(page_products, category)

        return drugs

    except Exception as e:
        print(f"[ERROR] parse_category: {e}")
        return []


def get_drugs_apteka911_by_category(session, target_url, headers):
    try:
        response = session.get(target_url, headers=headers, timeout=10)
        if response.status_code == 200:
            json_data = response.json()
            return json_data.get('data', {}).get('ajax_products', [])
        else:
            print(f"Помилка: {response.status_code}")
            return []


    except Exception as e:
        print(f"Помилка API: {e}")
        time.sleep(10)
        return []




def save_drugs(drugs, category):
    for drug in drugs:
        try:
            Drug_apteka911.objects.update_or_create(
                productID=drug.get('productID'),
                defaults={
                    'category': category,
                    'productName': drug.get('productName'),
                    'alias': drug.get('alias'),
                    'brandName': drug.get('brandName'),
                    'formName': drug.get('formName'),
                    'productAvail': True if drug.get('productAvail') == 'yes' else False,
                    'productCountry': drug.get('productCountry'),
                    'productForm': drug.get('productForm'),
                    'productMeasure': drug.get('productMeasure'),
                    'productMname': drug.get('productMname'),
                    'productPrice': drug.get('productPrice'),
                    'img': build_image_url(drug),

                    # 'img': f"https://apteka911.ua{drug.get('dataUrl', '')}{drug.get('productThumbs', {}).get('webpmid', {}).get('file', '')}",

                }
            )
        except Exception as e:
            print(f"[DB ERROR]: {e}")


def build_image_url(drug):
    try:
        return (
            "https://apteka911.ua"
            + drug.get('dataUrl', '')
            + drug.get('productThumbs', {}).get('webpmid', {}).get('file', '')
        )
    except:
        try:
            return (
                    "https://apteka911.ua"
                    + drug.get('dataUrl', '')
                    + drug.get('productThumbs', {}).get('mid', {}).get('file', '')
            )
        except:
            return None

from django.utils import timezone


# drugs = get_all_category()
# # save_drugs(drugs)
# today = timezone.now().date()
# print(f'today: {today}')

"""
data:{cart: null, yourpharmacy: null, defaultRegion: null, lastSelectedRegions: null, wish: null,…}
ajax_banner:null
ajax_fdata:null
ajax_products:[{productID: 40347, productName: "Еналозид 25 табл. №30", productForm: "табл. блістер 10мг/25мг",…},…]
0:{productID: 40347, productName: "Еналозид 25 табл. №30", productForm: "табл. блістер 10мг/25мг",…}
alias:"enalozid-25-tabl-30-p40347"
banDescript:null
brandID:9004
brandName:"ЕНАЛОЗИД"
dataUrl:"/content/shop/products/40347/"
drugID:3354
formName:"таблетки для внутрішнього застосування"
groupID:4170
productATC:"C09BA02"
productAnalogs:5
productAvail:"yes"
productBp5:"0.00"
productCode:155981
productCountry:"Україна"
productForm:"табл. блістер 10мг/25мг"
productHasMinPrice:1
productID:40347
productIsAction:0
productIsBest:0
productIsCashback:1
productIsFreeSm:0
productIsNew:0
productIsOld:0
productIsRare:0
productIsSale:0
productIsSets:0
productIsVideo:0
productMeasure:"блістер"
productMname:"ENALAPRILUM"
productMorion:"285116"
productName:"Еналозид 25 табл. №30"
productPack:3
productPrice:"135.00"
productPriceOld:"0.00"
productPromotions:[]
productQntComments:0
productRating:0
"""