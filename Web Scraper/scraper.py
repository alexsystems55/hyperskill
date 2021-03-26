from bs4 import BeautifulSoup
import requests
from string import punctuation


def get_page(url: str) -> bytes:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"HTTP error {response.status_code}!")
        exit(-1)
    return response.content


BASE_URL = "https://www.nature.com"

page = get_page(f"{BASE_URL}/nature/articles")
soup = BeautifulSoup(page, "lxml")
translation_table = {pm: "" for pm in punctuation}
translation_table[" "] = "_"

for article in soup.find_all("article"):
    article_type = article.find(attrs={"data-test": "article.type"}).span.string
    if article_type == "News":
        file_name = str(article.h3.a.string).translate(str.maketrans(translation_table))
        file_name += ".txt"
        article_link = article.h3.a.get("href")
        article_content = get_page(f"{BASE_URL}{article_link}")
        article_soup = BeautifulSoup(article_content, "lxml")
        article_text = article_soup.find(
            "div", class_="article__body cleared"
        ).get_text()
        with open(file_name, "wb") as article_file:
            article_file.write(bytes(article_text.strip(), "utf-8"))
