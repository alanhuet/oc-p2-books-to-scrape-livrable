import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extracteur_donnees(url_livre):
    #Extracts all data for a single book from its detail page.
    

    #1.ACQUISITION
    reponse = requests.get(url_livre)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")

    #2. DATA EXTRACTION
    infos_livre = {}
    tableau = soup.find("table")
    image = soup.find("img")
    url_image = urljoin(url_livre, image["src"])
    categorie = soup.find("ul", class_="breadcrumb").find_all("a")[2].string
    repere = soup.find("div", id="product_description")
    if repere:
        description_tag = repere.find_next_sibling("p")
        description = description_tag.get_text() if description_tag else "Pas de description."
    else:    
        description = "Pas de description."

    #Rating conversion
    conversion_notes = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    note_livre = soup.find("p", class_="star-rating")["class"][1]
    note_chiffre = conversion_notes.get(note_livre)

    #Extract data from the book table and add to the dictionary
    for ligne in tableau.find_all("tr"):
        cle = ligne.find("th").string
        valeur = ligne.find("td").string
        infos_livre[cle] = valeur

    #3. FINAL DATA STRUCTURE
    dict_final = {
        "product_page_url": url_livre,
        "universal_product_code (upc)": infos_livre["UPC"],
        "title": soup.find("h1").string,
        "price_including_tax": infos_livre["Price (incl. tax)"],
        "price_excluding_tax": infos_livre["Price (excl. tax)"],
        "number_available": infos_livre["Availability"],
        "product_description": description,
        "category": categorie,
        "review_rating": note_chiffre,
        "image_url": url_image

    }

    return dict_final    