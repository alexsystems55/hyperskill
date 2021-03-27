from bs4 import BeautifulSoup
import requests
from string import punctuation
from os import mkdir
import re


def get_page(url: str) -> bytes:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"HTTP error {response.status_code}!")
        exit(-1)
    return response.content


BASE_URL = "https://www.nature.com"
translation_table = {pm: "" for pm in punctuation}
translation_table[" "] = "_"

pages_number = int(input())
type_filter = input()

for page in range(1, pages_number + 1):
    dir_name = f"Page_{page}"
    print(f"Saving to dir {dir_name}")
    try:
        mkdir(dir_name)
    except FileExistsError:
        pass

    pages_url = f"?page={page}" if page > 1 else ""
    idx_page = get_page(f"{BASE_URL}/nature/articles{pages_url}")
    soup = BeautifulSoup(idx_page, "lxml")

    for article in soup.find_all("article"):
        article_type = article.find(attrs={"data-test": "article.type"}).span.string
        if article_type == type_filter:
            file_name = dir_name + "\\"
            file_name += str(article.h3.a.string).translate(
                str.maketrans(translation_table)
            )
            file_name += ".txt"
            print(f"\tSaving file: {file_name}")

            article_link = article.h3.a.get("href")
            article_content = get_page(f"{BASE_URL}{article_link}")
            article_soup = BeautifulSoup(article_content, "lxml")
            article_text = article_soup.find(
                "div", class_=re.compile(r"article\S*__body")
            )
            if article_text:
                with open(file_name, "wb") as article_file:
                    article_file.write(article_text.get_text().strip().encode())
