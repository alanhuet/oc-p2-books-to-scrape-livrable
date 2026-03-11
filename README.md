# Book Scraper

This program allows the user to scrape books from the website [Books to Scrape](https://www.books.toscrape.com)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Book Scraper.

```bash
pip install -r requirements.txt
```

## Usage

To launch the full extraction process (50 categories, ~1000 books), run the main script:

```bash
python main.py
```

The program will:

- Scan all book categories.

- Extract technical data (UPC, prices, descriptions, ratings).

- Download cover images.

- Organize everything into structured folders in **all_books/**.

## Project Structure

**main.py**: Main orchestrator of the scraping process.

**scrap_category.py**: Handles category-level logic and file storage.

**scrap_book.py**: Extracts detailed data from individual book pages.