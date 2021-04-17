import requests
from bs4 import BeautifulSoup
import lxml
import os
import openpyxl
import csv


domen = "http://ogorodsad.com.ua/shop/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344"
}
if not os.path.exists("source"):
        os.mkdir("source")
if not os.path.exists("data"):
        os.mkdir("data")


req = requests.get(url=domen, headers=headers)
src = req.text



with open("source/index.html", "w", encoding="UTF-8") as file:
    file.write(src)

try:


    with open("source/index.html", "r", encoding='UTF-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    products_hrefs = soup.find("div", class_="products").find_all("a")

    products_urls = []
    for href in products_hrefs:
        products_url = href.get("href")
        print(products_url)
        products_urls.append(products_url)
    print(products_urls)

    n = 0
    for i in products_urls:

        req = requests.get(url=i, headers=headers)
        src = req.text


        b = i.split("/")
        with open(f"source/{n}_{b[4]}.html", "w", encoding="UTF-8") as file:
            file.write(src)

    with open("source/0_semena-ovoschey.html", "r", encoding="UTF-8") as file:
        src = file.read()

    folder_name = "source/0_semena-ovoschey"

    nazvaniya = os.listdir("source")
    print(nazvaniya)
    for papka in nazvaniya:
        with open(f"source/{papka}/{papka}.html", "r", encoding="UTF-8") as file:
            src = file.read()
            soup = BeautifulSoup(src, "lxml")
            product_hrefs = soup.find_all("div", class_="product-category")
            product_hrefs_list = []
            for product_href in product_hrefs:
                href = product_href.find("a").get("href")
                product_hrefs_list.append(href)
                product_name = href.split("/")[5]
                # print(product_hrefs_list)
                folder_name = f"source/{papka}/{product_name}"
                if os.path.exists(folder_name):
                    print("Папка уже существует")
                else:
                    os.mkdir(folder_name)

                print(f"{product_name} успешно сохранен")
                for i in product_hrefs_list:
                    req = requests.get(url=i, headers=headers)
                    src = req.text
                    with open(f"source/{papka}/{product_name}/{product_name}.html", "w", encoding="UTF-8") as file:
                        file.write(src)

    with open("ogorod.csv", "w", newline='', encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Название",
                "Описание",
                "Вес",
                "Цена",
                "Категория",
                "Ссылка на фото"
            )
        )

    nazvaniya = os.listdir("source")
    # print(nazvaniya)
    for i in nazvaniya:    # папки с видами семян (0,1,2,3...)
        nazvanie = os.listdir(f"source/{i}")
        for n in nazvanie:     # арбузы, баклажаны, базилик html-ки
            with open(f"source/{i}/{n}/{n}.html", "r", encoding="UTF-8") as file:
                src = file.read()
                soup = BeautifulSoup(src, "lxml")

                product_hrefs = soup.find("div", class_="products").find_all("a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")
                product_hrefs_list = []
                for product_href in product_hrefs:
                    href = product_href.get("href")
                    product_hrefs_list.append(href)
                print(len(product_hrefs_list))
                for nj in product_hrefs_list:
                    print(nj)   # ссылки на сами семена (кавун астраханский, хуянский)
                    req = requests.get(url=nj, headers=headers)
                    src = req.text
                    soup = BeautifulSoup(src, "lxml")


                    try:
                        name_ves = soup.find("h1", class_="product_title entry-title").text
                    except:
                        name_ves = "-"

                    try:
                        cathegory = soup.find("a", rel="tag").text
                    except:
                        cathegory = "-"

                    try:
                        description = soup.find("div", id="tab-description").find("p").text.strip()
                        description = description.replace(" ", "")
                        description = description.replace("​", "")
                    except:
                        description = "-"

                    try:
                        price = soup.find("p", class_="price").text
                        price = price.replace(" ","")
                    except:
                        price = "-"

                    name_ves = name_ves.split("(")
                    name = name_ves[0]
                    print(228)
                    ves = "-"
                    print(1228)
                    pic_url = soup.find("div", class_="woocommerce-product-gallery__image").find("a").get("href")



                    with open("ogorod.csv", "a", newline='', encoding="UTF-8") as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            (
                                name,
                                description,
                                ves,
                                price,
                                cathegory,
                                pic_url
                            )
                        )







except Exception as ex:
    print(ex)