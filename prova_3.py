import requests
from bs4 import BeautifulSoup
#import pandas as pd
from urllib.parse import urljoin
# This part maybe will be useful for the csv  part
list_pages = ['index', 'page-2', 'page-3', 'page-4']
product_page_url_list = []
universal_product_code_list = []
title_list = []
price_including_tax_list = []
price_excluding_tax_list = []
number_available_list = []
product_description_list = []
category_list = []
review_rating_list = []
image_src_list = []
#
# print the links of the principal page
r = requests.get("https://books.toscrape.com/index.html")
base_url = "https://books.toscrape.com/index.html"
soup_obj_principal_pg = BeautifulSoup(r.content, "html.parser")
categories = soup_obj_principal_pg.find("ul", attrs={'class': None})
# List with the names of the categories
list_names_category = []
for item_n in categories.find_all('a'):
    category_name_text = item_n.get_text().strip()
    list_names_adding = list_names_category.append(category_name_text)
##############
url_of_pages_list = []
# Here is the part that I get all the information for all the books in all the categories
for link in categories.find_all('a'):
    href_of_categories_pg1 = link.get('href')
    url_of_pages = (urljoin(base_url, href_of_categories_pg1))
    url_of_pages_l = url_of_pages_list.append(url_of_pages)
    r1 = requests.get(url_of_pages)
    soup_obj_catg_pg = BeautifulSoup(r1.content, "html.parser")
    if soup_obj_catg_pg.find('ul', {'class': 'pager'}):
        page = soup_obj_catg_pg.find('ul', {'class': 'pager'})
        if page.find('li', {'class': 'next'}):
            page2 = page.find('li', {'class': 'next'})
            resp = page2.find('a')
            req = resp.get('href')
            url_of_pages2 = url_of_pages.replace('index.html', req)
            url_of_pages_li = url_of_pages_list.append(url_of_pages2)
            r2 = requests.get(url_of_pages2)
            soup_new = BeautifulSoup(r2.content, 'html.parser')
        if not page.find('li', {'class': 'next'}):
            url_of_pages3 = base_url + '/catalogue/category/books/' + str(
                page.find('li', {'class': 'current'}).find('a')['href'])
            url_of_pages_lis = url_of_pages_list.append(url_of_pages3)
            req2 = requests.get(url_of_pages3)
            soup_new = BeautifulSoup(req2.text, 'html.parser')

print(url_of_pages_list)

    # books_next_pg_url = soup_obj_catg_pg.find('li', attrs={'class': 'next'})
    # books_urls = soup_obj_catg_pg.find('ol', attrs={'class': 'row'})