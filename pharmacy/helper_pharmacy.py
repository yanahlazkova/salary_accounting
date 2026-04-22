import gzip
import json
import os
import django

import random
import time
import xml.etree.ElementTree as ET
from io import BytesIO
import requests
from fake_useragent import UserAgent

from pharmacy.models import Drug_apteka911, CategoryApteka911

import requests
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salary_accounting.settings')
django.setup()




"""
архіви у sitemap (apteka911):
https://apteka911.ua/content/sitemap/sitemap-products-0.xml.gz - дуже важкий (містить посилання на фото)
https://apteka911.ua/content/sitemap/sitemap-groups-0.xml.gz - по групам (за основним компонентом)
https://apteka911.ua/content/sitemap/sitemap-promotions-0.xml - акції
https://apteka911.ua/content/sitemap/sitemap-medical-uses-group-0.xml.gz - симптоми та захворювання
https://apteka911.ua/content/sitemap/sitemap-drugs-manual-0.xml.gz - /drugs/k*** (інструкції)
https://apteka911.ua/content/sitemap/sitemap-drugs-items-0.xml.gz - довідник ліків
https://apteka911.ua/content/sitemap/sitemap-tns-0.xml.gz - препарати
https://apteka911.ua/content/sitemap/sitemap-filters-1.xml.gz

"""

"""
1. get_category_urls()
2. parse_category()
3. save_to_db()
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_categories_whith_page_cite_apteka911():
    driver = webdriver.Chrome()
    driver.get("https://apteka911.ua/ua/")

    time.sleep(3)

    # знайти кнопку меню
    # menu_btn = driver.find_element(By.XPATH, "//div[contains(., 'Каталог')]")
    # menu_btn = driver.find_element(By.CSS_SELECTOR, "div.menu-catalog__button")
    menu_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".menu-nav span"))
    )

    menu_btn.click()

    # навести / клікнути
    # ActionChains(driver).move_to_element(menu_btn).perform()
    #
    # time.sleep(3)

    html = driver.page_source


    soup = BeautifulSoup(html, "html.parser")
    categories = []
    seen_urls = set()

    items = driver.find_elements(By.CSS_SELECTOR, "ul.menu-catalog__list > li")

    for item in items:
        try:
            name = item.find_element(By.CSS_SELECTOR, "meta[itemprop='name']").get_attribute("content")
            url = item.find_element(By.CSS_SELECTOR, "a[itemprop='url']").get_attribute("href")

            if url and url in seen_urls:
                continue
            else:
                seen_urls.add(url)

                categories.append({
                    "name": name,
                    "url": url
                })
                category_tree = check_category_tree_html(url)
        except:
            continue

    # записати у файл json
    with open('categories.json', 'w') as f:
        json.dump(categories, f, indent=4)

    return categories


def check_category_tree_html(url: str):
    ua = UserAgent()
    session = requests.Session()

    response = session.get('https://apteka911.ua/ua', headers={"User-Agent": ua.random})

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",  # КРИТИЧНО: саме це каже серверу віддати JSON
        # Referer має бути ПОВНИМ URL сторінки препарату
        "referer": f"https://apteka911.ua/ua",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    session.cookies.update({
        'site_version': 'desktop',
        'wucmf_region': '89',
        # 'PHPSESSID': '601c139cc7ac20fdcbecfdfd55095eb8'
    })
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '').lower()

        if 'application/json' in content_type:
            # data = response.json()
            print("Це JSON")
            return None

        elif 'text/html' in content_type:
            html = response.text
            categories_tree = get_categories_tree_with_html(html)
            print("Це HTML")
            return categories_tree

        else:
            print(f"Невідомий тип: {content_type}")
            return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return None


def get_categories_tree_with_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    root = soup.select_one('ul.block-medications')
    categories = []

    def walk(node, parent=None):
        for li in node.find_all('li', recursive=False):
            a = li.find('a', recursive=False)

            if not a:
                continue

            name = a.get_text(strip=True)
            url = a.get('href')

            category = {
                'name': name,
                'url': url,
                'parent': parent
            }
            categories.append(category)

            # шукаємо вкладений список
            sub_ul = li.find('ul', class_='block-medications')
            if sub_ul:
                walk(sub_ul, parent=url)

    walk(root)

    return categories


def update_categories_db(categories):
    """ оновлення категорій в БД """
    for c in categories:
        obj_category, _ = CategoryApteka911.objects.update_or_create(
            url=c['url'],
            defaults={"name": c['name']},
        )
        print(obj_category)






def is_valid_category(url: str, categories: list) -> bool:
    print(f'categories: {url}')

    for category in categories:
        if url.find(category['url']) == -1:
            continue
        else:
            slug = url.rstrip('/').split('/')[-1]

            # відсікаємо фільтри
            if slug.count('-') > 0:
                return False
            else:
                return True

    return False

def get_or_create_category(url_category):
    name = url_category.rstrip('/').split('/')[-1]
    category, _ = CategoryApteka911.objects.update_or_create(
        url=url_category,
        defaults={"name": name},
    )
    return category


def update_category(categories):
    cats = []
    # відкриваємо файл json та перебираємо категорії
    with open('categories.json', 'r') as f:
        file_content = f.read()
        cats = json.loads(file_content)

    ua = UserAgent()
    session = requests.Session()
    base_url = "https://apteka911.ua/ua/"

    session.get(base_url, headers={"User-Agent": ua.random})

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://apteka911.ua',
    }

    session.cookies.update({
        'site_version': 'desktop',
        'wucmf_region': '89',
    })




def get_categories_with_sitemap(categories):
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

        if 'filters' not in url or not url.endswith('.gz'):
            continue

        print(f"[SITEMAP] {url}")

        gz = session.get(url, timeout=20)

        with gzip.GzipFile(fileobj=BytesIO(gz.content)) as f:
            inner_root = ET.fromstring(f.read())

        for loc in inner_root.findall('ns:url/ns:loc', namespace):
            category_url = loc.text

            # перевірка чи співпадає категорія із отриманою з сайту
            # перевірка це категорія чи фільтр
            if not is_valid_category(category_url, categories):
                continue
            else:
                # отримаємо або додамо категорію
                category = get_or_create_category(category_url)

            # headers.update({
            #     "referer": "https://apteka911.ua/ua",
            #     "user-agent": ui.random,
            # })
            # category_url_page1 = f'{category_url}/page=1'

            # category_drugs = parse_category(session, category, category_url_page1, headers)

            # for drug in category_drugs:
            #     pid = drug.get('productID')
            #
            #     if pid and pid not in seen_ids:
            #         seen_ids.add(pid)
            #         drugs.append(drug)

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
        drugs.extend(products)

        # ✅ ІНШІ СТОРІНКИ
        # for page in range(2, pages + 1):
        #     page_url = f"{url}/page={page}"
        #     page_products = get_drugs_apteka911_by_category(session, page_url, headers)
        #     drugs.extend(page_products)
        #
        # return drugs

    except Exception as e:
        print(f"[ERROR] parse_category: {e}")
        return []


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
#
#
#
#
#
# def save_drugs(drugs):
#     for drug in drugs:
#         try:
#             Drug_apteka911.objects.update_or_create(
#                 productID=drug.get('productID'),
#                 defaults={
#                     'productName': drug.get('productName'),
#                     'alias': drug.get('alias'),
#                     'brandName': drug.get('brandName'),
#                     'formName': drug.get('formName'),
#                     'productAvail': True if drug.get('productAvail') == 'yes' else False,
#                     'productCountry': drug.get('productCountry'),
#                     'productForm': drug.get('productForm'),
#                     'productMeasure': drug.get('productMeasure'),
#                     'productMname': drug.get('productMname'),
#                     'productPrice': drug.get('productPrice'),
#                     'img': build_image_url(drug),
#
#                     # 'img': f"https://apteka911.ua{drug.get('dataUrl', '')}{drug.get('productThumbs', {}).get('webpmid', {}).get('file', '')}",
#
#                 }
#             )
#         except Exception as e:
#             print(f"[DB ERROR]: {e}")
#
#
# def build_image_url(drug):
#     try:
#         return (
#             "https://apteka911.ua"
#             + drug.get('dataUrl', '')
#             + drug.get('productThumbs', {}).get('webpmid', {}).get('file', '')
#         )
#     except:
#         try:
#             return (
#                     "https://apteka911.ua"
#                     + drug.get('dataUrl', '')
#                     + drug.get('productThumbs', {}).get('mid', {}).get('file', '')
#             )
#         except:
#             return None





# drugs = get_all_drugs()
# save_drugs(drugs)
# today = timezone.now().date()
# print(f'today: {today}')
""" 
fetch("https://apteka911.ua/ua/shop/search", {
  "headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,uk;q=0.6",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "priority": "u=1, i",
    "sec-ch-ui": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
    "sec-ch-ui-mobile": "?0",
    "sec-ch-ui-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
  },
  "referrer": "https://apteka911.ua/ua/shop/panadol-p383/borispol",
  "body": "q=%D0%BB%D0%B5%D0%B2%D0%BE%D0%BC%D1%96&limit=9&timestamp=1775810421276&hint=1&indexes=1&products=1",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});

curl 'https://apteka911.ua/ua/shop/lekarstvennyie-preparatyi/ot_boli_v_gorle/page=2' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: ru,uk;q=0.9,en-US;q=0.8,en;q=0.7' \
  -b 'PHPSESSID=601c139cc7ac20fdcbecfdfd55095eb8; 
      PHPSESSID=601c139cc7ac20fdcbecfdfd55095eb8; 
      site_version=desktop; 
      traffic_source={"gclid":null,"utm_source":"google","utm_medium":"organic","utm_campaign":"none","utm_term":"none","utm_content":"none"}; 
      userStatusSession=1776153117309; 
      user_type=new; 
      _gcl_au=1.1.2124508941.1776153119; 
      _hjSession_6368290=eyJpZCI6IjI2YmQzYzdlLTYyNzItNDg0Mi1hYzVkLTUxNDNhMzBlNjRiMiIsImMiOjE3NzYxNTMxMTg4MzgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; 
      _fbp=fb.1.1776153118884.481103544605656094; 
      cookie_chat_id=b826c2f75f334163a5c0a84b257fef51; 
      am-uid-f=e91df7ee-d51d-44e4-96d3-eb42ce37e2d0; 
      sc=1056581F-6060-F377-73F5-74534F7AD3CE; 
      cookie_consent=1; 
      noshowban_9f873692e73d8f6b5e04ae3ede770015=1; 
      _hjSessionUser_6368290=eyJpZCI6IjIwZThmYTU2LTA4M2QtNWZiYS1hMjA2LWZmYmE2YTYwZDBlYyIsImNyZWF0ZWQiOjE3NzYxNTMxMTg4MzYsImV4aXN0aW5nIjp0cnVlfQ==; 
      _gid=GA1.2.1252109726.1776153273; 
      _ga=GA1.1.1513671076.1776153119; 
      1776153117309=1776153472773; 
      _ga_VRYFSBB3XF=GS2.1.s1776153119$o1$g1$t1776153491$j37$l0$h0' \
  -H 'priority: u=1, i' \
  -H 'referer: https://apteka911.ua/ua/shop/lekarstvennyie-preparatyi/ot_boli_v_gorle' \
  -H 'sec-ch-ui: "Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"' \
  -H 'sec-ch-ui-mobile: ?0' \
  -H 'sec-ch-ui-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest'
  
"""