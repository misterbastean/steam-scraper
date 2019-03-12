from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from mongoengine import *
from datetime import datetime
from config import config

baseUrl = "https://store.steampowered.com/search/?specials=1&page="

# Connect to MongoDB
db = connect('steam-scrape', host=f'mongodb://{config["username"]}:{config["password"]}@ds145039.mlab.com', port=45039)

# Create connection, read raw html, close connection
uClient = uReq(baseUrl + "1")
page_html = uClient.read()
uClient.close()

# Parse the html
page_soup = soup(page_html, "html.parser")

# Grabs list of products
search_results = page_soup.findAll("a", {"class": "search_result_row"})

for i, product in enumerate(search_results):
    try:
        name = product.find("span", "title").text.strip()
        original_price = int(str(product.find("strike")).replace("<strike>", "").replace("</strike>", "").replace("$", "").replace(".", ""))
        sale_price = int(str(product.find("div", "search_price").contents[3]).replace("$", "").replace(".", "").strip())

        # Parse platforms
        platforms = []
        platforms_raw = product.findAll("span", "platform_img")
        for span in platforms_raw:
            if "win" in str(span):
                platforms.append("win")
            if "mac" in str(span):
                platforms.append("mac")
            if "linux" in str(span):
                platforms.append("linux")

        game_data = {
                "gameName": name,
                "platform": platforms,
                "originalPrice": original_price,
                "discountedPrice": [{
                    "date": datetime.now(),
                    "price": sale_price
                }],
            }

        print(game_data)
    except Exception as e:
        print("**********Problem with iteration " + str(i) + "**********")
        print(e)

# Close DB connection
db.close()
