import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from slugify import slugify

def extracteur_donnees(url_livre):

    #1.CONFIGURATION ET INITIALISATION
    maintenant = datetime.now()
    date_formatee = maintenant.strftime("%Y-%m-%d")

    #2.ACQUISITION DU CONTENU HTML
    reponse = requests.get(url_livre)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")

    #3.EXTRACTION DES DONNÉES DU TABLEAU
    #création du dictionnaire avec le titre du livre 
    infos_livre = {}

    #création de la variable qui stocke les informations du tableau
    tableau = soup.find("table")
    image = soup.find("img")
    url_image = "https://books.toscrape.com/" + image["src"].replace("../../", "")
    categorie = soup.find("ul", class_="breadcrumb").find_all("a")[2].string
    repere = soup.find("div", id="product_description")
    description = repere.find_next_sibling("p").get_text()

    #conversion des notes des livres en entiers avec un dictionnaire
    conversion_notes = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    #création de la variable pour stocker la note du livre
    note_livre = soup.find("p", class_="star-rating")["class"][1]
    note_chiffre = conversion_notes.get(note_livre)

    #récupération des données du tableau du livre et ajout des données dans le dictionnaire
    for ligne in tableau.find_all("tr"):
        cle = ligne.find("th").string
        valeur = ligne.find("td").string
        infos_livre[cle] = valeur

    #4.CRÉATION DU DICTIONNAIRE FINAL QUI SERVIRA A LA CRÉATION DU FICHIER CSV
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
    #5.CRÉATION DU FICHIER CSV  

    #titre_clean = slugify(dict_final["title"])
    #NomFichier = f"{titre_clean}_extract_{date_formatee}.csv"

    #with open(NomFichier, "w", encoding="utf8", newline="") as csv_file:
        #writer = csv.DictWriter(csv_file, fieldnames=dict_final.keys())
        #writer.writeheader()
        #writer.writerow(dict_final)

    return dict_final    