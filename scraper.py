import requests
from bs4 import BeautifulSoup


headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
  "Accept-Encoding": "*"
}

def req_source(url):
    return requests.get(url, headers=headers)


def get_best_sellers_list():
    source = req_source("https://www.amazon.in/gp/bestsellers/")
    soup = BeautifulSoup(source.text, "lxml")

    best_sellers = {}

    for carousel_cont in soup.select("#zg_left_col1 > .celwidget[data-csa-c-painter='p13n-zg-list-carousel-desktop-cards'] div.a-carousel-container"):
        main_title = carousel_cont.select("h2.a-carousel-heading")[0].text
        best_seller_items = []

        for carousel_item in carousel_cont.select(".a-carousel > li.a-carousel-card .p13n-sc-uncoverable-faceout"):
            a = carousel_item.select(".a-link-normal")

            redirect_link = f"https://www.amazon.in/{a[0]['href']}"
            image_src = a[0].select("img.a-dynamic-image")[0]["src"]
            name = a[1].select("span > div")[0].text

            a_row = carousel_item.select(".a-row:not(.a-size-small)")

            stars = a_row[0].select("span.a-icon-alt")[0].text
            reviews_count = a_row[0].select("span.a-size-small")[0].text
            price = a_row[1].select("span.a-size-base")[0].text if len(a_row) > 1 else "NA"

            best_seller_items.append({"name": name, "image_src": image_src, "stars": stars, "reviews_count": reviews_count, "price": price, "redirect_link": redirect_link})

        best_sellers[main_title] = best_seller_items
    
    return best_sellers