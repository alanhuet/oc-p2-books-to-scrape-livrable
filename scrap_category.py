import requests
from bs4 import BeautifulSoup
import csv
import os
from slugify import slugify
from scrap_book import extracteur_donnees
from urllib.parse import urljoin 


def scrap_category(url_categorie):
    # Manages the scraping of an entire category, handles pagination and storage.
    toutes_les_donnees = []

    # 1. SCANNING ALL PAGES OF THE CATEGORY
    while url_categorie:
        reponse = requests.get(url_categorie)
        soup = BeautifulSoup(reponse.content, "html.parser")

        # Extracting book links
        titres_livres = soup.find_all("h3")
        for titre in titres_livres:
            lien_livre = titre.find("a")["href"]
            url_livre = urljoin(url_categorie, lien_livre)
            donnees_livre = extracteur_donnees(url_livre)
            toutes_les_donnees.append(donnees_livre)

        # Pagination management (Next button)
        bouton_next = soup.find("li", class_="next")
        if bouton_next:
            lien_next = bouton_next.find("a")["href"]
            url_categorie = urljoin(url_categorie, lien_next)
        else:
            url_categorie = None        

    # 2. STORAGE MANAGEMENT
    if toutes_les_donnees:
        # Define and create folder structure
        nom_cat_brut = toutes_les_donnees[0]["category"]
        nom_cat_propre = slugify(nom_cat_brut)
        print(f"Archivage des données de la catégorie '{nom_cat_propre}'...")

        chemin_dossier = os.path.join("all_books", nom_cat_propre)

        if not os.path.exists(chemin_dossier):
            os.makedirs(chemin_dossier)
            print(f"Dossier créé : {chemin_dossier}")

        # CSV Export
        nom_fichier = f"{nom_cat_propre}_books_info.csv"
        chemin_complet_csv = os.path.join(chemin_dossier, nom_fichier)

        with open(chemin_complet_csv, "w", encoding="utf8", newline="") as csv_file:
            en_tetes = toutes_les_donnees[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=en_tetes)
            writer.writeheader()
            writer.writerows(toutes_les_donnees)

        # Image Download
        for livre in toutes_les_donnees:
            nom_image = f"{slugify(livre['title'])}.jpg"
            chemin_image = os.path.join(chemin_dossier, nom_image)
            img_data = requests.get(livre["image_url"]).content
            with open(chemin_image, "wb") as f:
                f.write(img_data)

        print(f"Indexation de la catégorie '{nom_cat_propre}' terminée : {len(toutes_les_donnees)} livres et images archivés.")

    else:
        print("Erreur : aucune donnée n'a été récupérée.")

        
if __name__ == "__main__":
    scrap_category("https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html")        