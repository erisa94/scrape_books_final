import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urljoin
# list to use in pandas
product_page_url_list = []
universal_product_code_list = []
title_list = []
price_including_tax_list = []
price_excluding_tax_list = []
number_available_list = []
product_description_list = []
category_list_repeated = []
category_list = [] #I need this for the csv files creation
review_rating_list = []
image_src_list = []
# Starting the program
r = requests.get("https://books.toscrape.com/index.html")
base_url = "https://books.toscrape.com/index.html"
soup_obj_principal_pg = BeautifulSoup(r.content, "html.parser")
categories = soup_obj_principal_pg.find("ul", attrs={'class': None})
url_of_pages_list = []
# Get all the links of all the pages in the different categories
for link in categories.find_all('a'):
    href_of_categories_pg1 = link.get('href')
    url_of_pages = (urljoin(base_url, href_of_categories_pg1))
    url_of_pages_l = url_of_pages_list.append(url_of_pages)
    r1 = requests.get(url_of_pages)
    html_soup = BeautifulSoup(r1.content, "html.parser")
    i = 2
    if html_soup.find('ul', {'class': 'pager'}):
        url2 = url_of_pages.replace('index', 'page-2')
        url_of_pages_li = url_of_pages_list.append(url2)
        r2 = requests.get(url2)
        html_soup2 = BeautifulSoup(r2.content, "html.parser")
        if html_soup2.find('li', {'class': 'next'}):
            while True:
                url3 = url_of_pages.replace('index', f'page-{i+1}')
                url_of_pages_li = url_of_pages_list.append(url3)
                r3 = requests.get(url3)
                html_soup3 = BeautifulSoup(r3.content, "html.parser")
                i = i + 1
                if not html_soup3.find('li', {'class': 'next'}):
                    break
    if not html_soup.find('ul', {'class': 'pager'}):
        continue
# To prove everything went ok with the pages
print(url_of_pages_list)
for item in range(len(url_of_pages_list)):
    response = requests.get(url_of_pages_list[item])
    soup_obj_every_pg = BeautifulSoup(response.content, "html.parser")
    books_url = soup_obj_every_pg.find('ol', attrs={'class': 'row'})
    # Used set() to get the information only once
    allLinks = set()
    for book_in_page in books_url.find_all('a'):
        href_of_books = book_in_page.get('href')
        url_of_books = (urljoin(response.url, href_of_books))
        r2 = requests.get(url_of_books)
        # The part I added to get the links once
        if r2.url not in allLinks:
            product_page_url_ = r2.url
            print('product_page_url=', r2.url)
            product_page_url_l = product_page_url_list.append(product_page_url_)
            #
            soup_p3 = BeautifulSoup(r2.content, "html.parser")
            table_gen = soup_p3.find(class_="table table-striped")
            items_gen = table_gen.find_all("td")
            #
            universal_pr_code = [items_gen[0].get_text()][-1]
            print("universal_product_code =", universal_pr_code)
            universal_product_code_l = universal_product_code_list.append(universal_pr_code)
            #
            title_gen = soup_p3.find(["h1"]).string
            print("title =", title_gen)
            title_l = title_list.append(title_gen)

            #
            price_excluding_tax_gen_ = [items_gen[2].get_text()]
            print("price_excluding_tax =", items_gen[2].get_text())
            price_excluding_tax_l = price_excluding_tax_list.append(price_excluding_tax_gen_)
            #
            price_including_tax_gen_ = [items_gen[3].get_text()]
            print("price_including_tax =", items_gen[3].get_text())
            price_including_tax_l = price_including_tax_list.append(price_including_tax_gen_)
            #
            number_available_ = [items_gen[5].get_text()]
            print("number_available =", items_gen[5].get_text())
            number_available_l = number_available_list.append(number_available_)
            # product_description
            description = soup_p3.find_all('p')
            description = description[3].string
            print('description =', description)
            product_description_l = product_description_list.append(description)
            # category
            category = soup_p3.find_all('li')
            category_ = category[2].find('a').string
            print("category =", category_)
            # The list I used in the panda DataFrame
            category_li = category_list_repeated.append(category_)
            # A way to get a list without repetitions to use to create the csv files
            if category_ not in category_list:
                category_l = category_list.append(category_)
            # Ratings
            star_rating = soup_p3.find("p", attrs={'class': 'star-rating'})
            stars_ = star_rating['class']
            stars = stars_[1]
            print('review_rating = ', stars, 'stars')
            review_rating_l = review_rating_list.append(stars)

            # Find image url
            image_gen = soup_p3.find("div", attrs={'class': 'item active'})
            image_source = image_gen.find('img', src=True)
            image_ = image_source["src"][6:]
            image_url_comp = "https://books.toscrape.com/" + image_
            image_src = image_src_list.append(image_url_comp)
            print("image_url_ =", image_url_comp)
            #

        allLinks.add(r2.url)

# Created the file of pages
if not os.path.exists("Photos_books"):
    os.makedirs("Photos_books")
    path = os.path.dirname(__file__)
    for i in range(len(image_src_list)):
        img_name = image_src_list[i].split('/')[-1]
        file_name = path + "/Photos_books/" + img_name
        r = requests.get(image_src_list[i], allow_redirects=True)
        open(file_name, 'wb').write(r.content)
# Created a DataFrame with pandas
book_information = pd.DataFrame({
    'product_page_url': product_page_url_list,
    'universal_product_code': universal_product_code_list,
    'title': title_list,
    'price_including_tax': price_including_tax_list,
    'price_excluding_tax': price_excluding_tax_list,
    'number_available': number_available_list,
    'product_description': product_description_list,
    'category': category_list_repeated,
    'review_rating': review_rating_list,
    'image_url': image_src_list})
# Created the csv files
if not os.path.exists("All_Categories_csv"):
    os.makedirs('All_Categories_csv')
    for i in range(50):
        var_x = book_information[book_information['category'] == category_list[i]]
        var_x.to_csv(f'category_book{i}.csv')

