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

from pharmacy.models import Drug


# from your_app.models import Drug # Переконайтеся, що модель імпортована

def get_drugs_apteka911_from_sitemap():
    # 1. Ініціалізація генератора юзер-агентів
    ua = UserAgent()
    session = requests.Session()

    sitemap_url = 'https://apteka911.ua/sitemap.xml'
    api_url = "https://apteka911.ua/ua/shop/search"

    headers_base = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://apteka911.ua'
    }

    unique_codes = set()

    print(f"--- Підготовка: Завантаження існуючих кодів з БД ---")
    # 2. ОПТИМІЗАЦІЯ БД: Отримуємо всі існуючі коди одним запитом
    # values_list('code', flat=True) повертає плоский список, який ми конвертуємо в set для миттєвого пошуку O(1)
    existing_codes = set(Drug.objects.values_list('code', flat=True))
    print(f"У базі вже є {len(existing_codes)} записів.")

    print(f"--- Завантаження головного sitemap ---")

    processed_count = 0  # 1. Ініціалізуємо лічильник перед початком циклів

    try:
        # 3. Додано timeout для безпеки
        response = session.get(sitemap_url, headers={'User-Agent': ua.random}, timeout=15)
        response.raise_for_status()  # Перевірка на помилки 404, 500

        root = ET.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        sitemaps = root.findall('ns:sitemap/ns:loc', namespace)

        for sitemap_tag in sitemaps:
            url_text = sitemap_tag.text

            if 'cities' in url_text and url_text.endswith('gz'):
                print(f"Відкриваємо архів: {url_text}")

                try:
                    # Додано timeout для архіву
                    gz_response = session.get(url_text, headers={'User-Agent': ua.random}, timeout=20)
                    gz_response.raise_for_status()

                    # Безпечне розпакування у пам'яті
                    with gzip.GzipFile(fileobj=BytesIO(gz_response.content)) as f:
                        inner_root = ET.fromstring(f.read())

                    random_count = random.randint(80, 120)

                    for url_tag in inner_root.findall('ns:url/ns:loc', namespace):


                        full_url = url_tag.text

                        if 'borispol' in full_url:
                            alias = "/" + "/".join(full_url.split("/")[3:-1])
                            drug_code = alias.split('-')[-1].strip('/')

                            # 4. Наповнюємо нашу множину
                            unique_codes.add(drug_code)

                            # Швидка перевірка в оперативній пам'яті без смикання Django
                            if drug_code in existing_codes:
                                continue

                            headers = headers_base.copy()
                            headers['User-Agent'] = ua.random
                            headers['referer'] = full_url

                            payload = {
                                'pushHistory': 'true',
                                'alias': alias
                            }

                            try:
                                res = session.post(api_url, headers=headers, data=payload, timeout=10)
                                if res.status_code == 200:
                                    json_data = res.json()

                                    history = json_data.get('data', {}).get('history', [])
                                    if history:
                                        # Тут можна додати перевірку на наявність ціни, якщо вона приходить у цьому API
                                        item_data = history[0]
                                        real_name = item_data.get('name')
                                        price = item_data.get('price', 0)  # Приклад витягування ціни

                                        Drug.objects.update_or_create(
                                            code=drug_code,
                                            defaults={
                                                'name': real_name,
                                                'alias': alias,
                                                'price': price # Якщо ви додасте це поле в модель
                                            }
                                        )
                                        # Обов'язково додаємо новий код до нашого in-memory сету
                                        existing_codes.add(drug_code)
                                        print(f"Збережено: {real_name} ({drug_code})")

                                        processed_count += 1
                                        print(f"[{processed_count}] Збережено: {real_name}")

                                        # 3. ПЕРЕВІРКА: кожні 100 препаратів
                                        if processed_count % random_count == 0:
                                            random_count = random.randint(80, 120)
                                            long_wait = random.uniform(30, 60)  # Пауза на 30-60 секунд
                                            print(
                                                f"--- Оброблено {processed_count} товарів. Велика пауза: {long_wait:.1f} сек. ---")
                                            time.sleep(long_wait)
                                        else:
                                            # Звичайна пауза між запитами
                                            time.sleep(random.uniform(5, 15))

                            except Exception as e:
                                print(f"Помилка API на {alias}: {e}")
                                time.sleep(10)

                except Exception as e:
                    print(f"Помилка завантаження/розпакування архіву {url_text}: {e}")

        print("--- Синхронізація успішно завершена! ---")

    except Exception as e:
        print(f"Критична помилка під час виконання: {e}")

    return unique_codes

# Запуск
codes = get_drugs_apteka911_from_sitemap()
print(f"\n--- ГОТОВО ---")
print(f"Знайдено унікальних товарів: {len(codes)}")
print(f"Приклади кодів: {list(codes)[:10]}")

# Збереження у файл для подальшої роботи
with open("drug_codes.txt", "w") as f:
    for code in sorted(codes):
        f.write(code + "\n")