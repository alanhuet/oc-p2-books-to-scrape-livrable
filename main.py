import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from slugify import slugify
from scrap_book import extracteur_donnees
from urllib.parse import urljoin 

url_site = "https://books.toscrape.com/index.html"
response_accueil = requests.get(url_site)
soup_accueil = BeautifulSoup(response_accueil.content, "html.parser")

liens_categories = []
menu_categories = soup_accueil.find("div", class_"side_categories").find("ul").find("ul")



toutes_les_donnees = []

while url_categorie:
    reponse = requests.get(url_categorie)
    soup = BeautifulSoup(reponse.content, "html.parser")

    #extraction des liens des livres
    titres_livres = soup.find_all("h3")
    for titre in titres_livres:
        lien_livre = titre.find("a")["href"]
        url_livre = urljoin(url_categorie, lien_livre)
        donnees_livre = extracteur_donnees(url_livre)
        toutes_les_donnees.append(donnees_livre)

    #recherche du bouton next pour changer de page
    bouton_next = soup.find("li", class_="next")
    if bouton_next:
        lien_next = bouton_next.find("a")["href"]
        url_categorie = urljoin(url_categorie, lien_next)
    else:
        url_categorie = None        

if toutes_les_donnees:
    nom_cat = toutes_les_donnees[0]["category"]
    date = datetime.now().strftime("%Y-%m-%d")
    nom_fichier = f"{slugify(nom_cat)}_category_extract_{date}.csv"

    with open(nom_fichier, "w", encoding="utf8", newline="") as csv_file:
        en_tetes = toutes_les_donnees[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=en_tetes)
        writer.writeheader()
        writer.writerows(toutes_les_donnees)

    print(f"Extraction treminée : {len(toutes_les_donnees)} livres sauvegardés dans {nom_fichier}") 

else:
    print("Erreur : aucune donnée n'a été récupérée.")