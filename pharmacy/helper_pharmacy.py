import requests
from fake_useragent import UserAgent

def search_drugs_apteka911(search_term):
    ua = UserAgent()
    session = requests.Session()

    headers = {
        "User-Agent": ua.random
    }

    # 1. зайти на сайт (отримати cookies)
    session.get("https://apteka911.ua/ua/", headers=headers)

    # 2. подивитись що отримали
    print(session.cookies.get_dict())

    url = "https://apteka911.ua/ua/shop/search"


    headers.update({
        'x-requested-with': 'XMLHttpRequest',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://apteka911.ua',
        'referrer': 'https://apteka911.ua',
    })

    payload = {
        "q": search_term,
    }

    response = session.post(url, headers=headers, data=payload, timeout=15)

    print(f"Status: {response.status_code}")
    data = response.json()

    results = data.get("data", {}).get("results", [])

    list_alias = [
        item['alias']
        for item in results
        if item['alias'].startswith('/drugs/')
    ]

    return {
        'table_rows': [
            get_products_from_alias(session, headers.copy(), alias)
            for alias in list_alias[:3]  # обмеж для тесту
        ]
    }


def get_products_from_alias(session, headers, alias):
    headers.update({
        'x-requested-with': 'XMLHttpRequest',
        'content-type': 'application/json',
        'origin': 'https://apteka911.ua',
        'referer': 'https://apteka911.ua',
    })

    cookies = session.cookies.copy()
    cookies.update({
        'wucmf_region': '89'
    })

    # витягуємо slug
    category = alias.split("/")[-1]

    url = "https://apteka911.ua/shop/api/catalog/search"

    payload = {
        "url": alias,  # 🔥 ключовий момент
        # "page": 1
    }

    response = session.post(url, json=payload, headers=headers, cookies=cookies, timeout=15)

    print(response.status_code)
    print(response.text)
    return response.json()

""" 
fetch("https://apteka911.ua/ua/shop/search", {
  "headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,uk;q=0.6",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
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
"""