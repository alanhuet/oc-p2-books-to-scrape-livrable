import requests
from bs4 import BeautifulSoup
from scrap_category import scrap_category
from urllib.parse import urljoin 

url_site = "https://books.toscrape.com/index.html"

def programme():
    # Main function to launch the full site scraping process.
    reponse_accueil = requests.get(url_site)
    soup_accueil = BeautifulSoup(reponse_accueil.content, "html.parser")

    # Target the category menu
    menu_categories = soup_accueil.find("div", class_="side_categories").find("ul").find("ul")
    liens_a = menu_categories.find_all("a")

    # Generate full URLs list
    urls_categories = [urljoin(url_site, a["href"]) for a in liens_a]
    nbre_categories = len(urls_categories)

    # Launch scraping for each category
    for url in urls_categories:
        scrap_category(url)

    print(f"Opération terminée : {nbre_categories} catégories ont été extraites")    

if __name__ == "__main__":
    programme()