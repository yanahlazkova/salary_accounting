# https://apteka911.ua/robots.txt
# https://www.add.ua/robots.txt - аптека доброго дня
# https://1sa.com.ua/robots.txt

""" sitemap.xml — це файл для пошукових роботів (Google),
який містить посилання на всі сторінки сайту"""

pharmacy = {
    'apteka911': 'https://apteka911.ua/sitemap.xml',
    'add': 'https://1sa.com.ua/sitemap.xml',
    '1sa': 'https://www.add.ua/sitemap.xml',
}

city = {
        'apteka911': 'borispol',
    }

# Нижче наведено скрипт на Python, який автоматично:
# Завантажує головний sitemap.xml.
# Знаходить у ньому всі посилання на архіви товарів (.xml.gz). (для apteka911)
# Розпаковує їх «на льоту» (без збереження на диск, щоб економити місце).
# Витягує унікальні коди товарів за допомогою регулярних виразів.

import requests
import gzip
import xml.etree.ElementTree as ET
import re
from io import BytesIO
from fake_useragent import UserAgent

ua = UserAgent()


def get_unique_drug_codes_apteka911():
    main_sitemap_url = pharmacy['apteka911']
    headers = {
        'User-Agent': ua.random, # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Набір (set) автоматично видаляє дублікати
    unique_codes = set()

    # Регулярний вираз для пошуку коду типу "p12181" або "d1099" у URL
    # Шукаємо частину, що йде після назви ліків (наприклад, -p12181 або -d1099)
    code_pattern = re.compile(r'-([pd]\d+)')

    print(f"--- Завантаження головного sitemap ---")
    try:
        response = requests.get(main_sitemap_url, headers=headers)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Шукаємо всі посилання на вкладені карти (sitemaps)
        sitemaps = root.findall('ns:sitemap/ns:loc', namespace)

        for sitemap_url in sitemaps:
            url_text = sitemap_url.text

            # Нас цікавлять лише архіви з ліками (drugs-manual)
            # if 'drugs-manual' in url_text and url_text.endswith('.gz'):
            if 'cities' in url_text and url_text.endswith('gz'):
                print(f"Обробка архіву: {url_text.split('/')[-1]}")

                gz_response = requests.get(url_text, headers=headers)

                # Розпаковуємо GZIP у пам'яті
                with gzip.GzipFile(fileobj=BytesIO(gz_response.content)) as f:
                    gz_xml_content = f.read()
                    inner_root = ET.fromstring(gz_xml_content)

                    for url_tag in inner_root.findall('ns:url/ns:loc', namespace):
                        full_url = url_tag.text
                        print(f'==: {full_url.split("/")[-1]}: {city['apteka911']}')

                        if city['apteka911'] in full_url:
                            print(f'==?: {full_url.split("/")[-1] == city["apteka911"]}')

                            # Витягуємо код із URL (наприклад, з /asparkam-p12181/ беремо p12181)
                            match = code_pattern.search(full_url)
                            if match:
                                unique_codes.add(match.group(1))

    except Exception as e:
        print(f"Помилка під час виконання: {e}")

    return unique_codes


# Запуск
codes = get_unique_drug_codes_apteka911()
print(f"\n--- ГОТОВО ---")
print(f"Знайдено унікальних товарів: {len(codes)}")
print(f"Приклади кодів: {list(codes)[:10]}")

# Збереження у файл для подальшої роботи
with open("drug_codes.txt", "w") as f:
    for code in sorted(codes):
        f.write(code + "\n")