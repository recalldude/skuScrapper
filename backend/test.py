from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re 

def fetch_page(url):
    driver = webdriver.Safari()

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Attendre que la page se charge
        print("Page fetched successfully.")
        #print(driver.page_source[:500]) 
        return BeautifulSoup(driver.page_source, 'html.parser')
    finally:
        driver.quit()



def get_product_info(soup, type, class_name):
    # title_tag = soup.find('title')
    tag = soup.find(type, class_ = re.compile(fr'\b{class_name}\b'))
    if tag:
        return tag.text.strip()
    else:
        return f"{type} class:{class_name} not found"


    
    
class Product:

    def __init__(self, sku):
        self.sku = sku
        self.name = ''
        self.brand = ''
        self.price = ''
        self.description = ''
    
    def __repr__(self):
        return f'Procuct(name={self.name})'
    
    def get_info(self):
        soup = fetch_page(f'https://fr.louisvuitton.com/fra-fr/produits/{self.sku}')
        self.name = get_product_info(soup, 'h1', 'lv-product__name')
        self.price = get_product_info(soup, 'div', 'lv-price')
        self.brand = 'LV'
        self.description = ''
        return (self.name, self.price, self.brand)
    

 
sac = Product('M01821')
name, price, brand = sac.get_info()
print(name)
print(price)
print(brand)
    
# sku = 'M01821'
# sku = input('sku: ').upper()
# soup = fetch_page(f'https://fr.louisvuitton.com/fra-fr/produits/{sku}')
# rep = get_product_info(soup, 'h1', 'lv-product__name')
# rep = get_product_title(f'https://fr.louisvuitton.com/fra-fr/produits/{sku}')
# print(rep)
# M01821

