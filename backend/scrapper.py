import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        response.raise_for_status()

def scrape_nike(soup):
    try:
        product_name = soup.find('h1', class_='product-title').text.strip()
        product_price = soup.find('span', class_='product-price').text.strip()
        product_description = soup.find('div', class_='product-description').text.strip()
        return {
            'name': product_name,
            'price': product_price,
            'description': product_description
        }
    except AttributeError:
        print("Failed to parse Nike page. Check the selectors.")
        return None

def scrape_lv(soup):
    try:
        product_name = soup.find('h1', class_=re.compile(r'lv-product__name')).text.strip()
        # product_price = soup.find('span', class_='lv-price').text.strip()
        # product_description = soup.find('div', class_='description').text.strip()
        return {
            'name': product_name,
            # 'price': product_price,
            # 'description': product_description
        }
    except AttributeError:
        print("Failed to parse Louis Vuitton page. Check the selectors.")
        return None

def scrape_adidas(soup):
    try:
        product_name = soup.find('h1', class_='gl-heading').text.strip()
        product_price = soup.find('div', class_='gl-price').text.strip()
        product_description = soup.find('div', class_='gl-description').text.strip()
        return {
            'name': product_name,
            'price': product_price,
            'description': product_description
        }
    except AttributeError:
        print("Failed to parse Adidas page. Check the selectors.")
        return None

def get_product_info(url):
    soup = fetch_page(url)
    if 'nike.com' in url:
        return scrape_nike(soup)
    elif 'louisvuitton.com' in url:
        return scrape_lv(soup)
    elif 'adidas.com' in url:
        return scrape_adidas(soup)
    else:
        print("Unsupported site.")
        return None

# Demander le SKU et le site à l'utilisateur
sku = input("Entrez le SKU du produit : ")
site = input("Entrez le site (nike, louisvuitton, adidas) : ").lower()

# Déterminer l'URL en fonction du site
if site == 'nike':
    url = f"https://www.nike.com/product/{sku}"
elif site == 'louisvuitton':
    url = "https://fr.louisvuitton.com/fra-fr/produits/porte-cles-et-bijou-de-sac-vivienne-dragonne-s00-nvprod5370055v/M01821"
    # url = f"https://fr.louisvuitton.com/fra-fr/produits/{sku}"
elif site == 'adidas':
    url = f"https://www.adidas.com/product/{sku}"
else:
    url = None
    print("Site non pris en charge.")

if url:
    product_info = get_product_info(url)
    if product_info:
        print(product_info)
    else:
        print("Informations du produit introuvables.")
