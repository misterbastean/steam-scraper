from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from mongoengine import *
from datetime import datetime
from config import config

baseUrl = "https://store.steampowered.com/search/?specials=1&page="

# Connect to MongoDB
db = connect('steam-scrape', host=f'mongodb://ds145039.mlab.com', port=45039, username=config['username'], password=config['password'])


# ===========================
# Schema Class Definitions
# ===========================
class Games(Document):
    gameName = StringField(required=True)
    platform = ListField(StringField())
    originalPrice = IntField(required=True)
    discountedPrice = ListField(DictField(), required=True)


# ===========================
# Secondary Functions
# ===========================
def parsePlatforms(product):
    platforms = []
    platforms_raw = product.findAll("span", "platform_img")
    for span in platforms_raw:
        if "win" in str(span):
            platforms.append("win")
        if "mac" in str(span):
            platforms.append("mac")
        if "linux" in str(span):
            platforms.append("linux")
    return platforms


# ===========================
# Main Function
# ===========================
def main():
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
            platforms = parsePlatforms(product)

            game_data = {
                    "gameName": name,
                    "platform": platforms,
                    "originalPrice": original_price,
                    "discountedPrice": [{
                        "date": datetime.now(),
                        "price": sale_price
                    }],
                }

            if Games.objects(gameName=game_data['gameName']):  # If there's already a db entry for the game title...
                # Push new price data
                updatedObject = (
                    Games.objects(gameName=game_data['gameName'])
                    .modify(push__discountedPrice=game_data["discountedPrice"][0])
                )
                print("Updated")
            else:
                # Create Games document and write to DB
                game = Games(gameName=game_data['gameName'])
                game.platform = game_data['platform']
                game.originalPrice = game_data['originalPrice']
                game.discountedPrice = game_data['discountedPrice']
                game.save()
                print("New game added to db")

        except Exception as e:
            print("**********Problem with iteration " + str(i) + "**********")
            print(e)

    # Close DB connection
    db.close()


if __name__ == "__main__":
    main()

