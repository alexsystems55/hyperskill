from bs4 import BeautifulSoup
import re
import requests


def show_error() -> None:
    print("Invalid movie page!")
    exit(-1)


# URL input and validation
url = input("Input the URL: ")
rx_url = re.compile(r"https://www.imdb.com/title/[a-z0-9]+/")
if not rx_url.match(url):
    show_error()

# Get the page
headers = {'Accept-Language': 'en-US,en;q=0.5'}  # Forcing to return English version of the page
response = requests.get(url, headers=headers)
if response.status_code != 200:
    show_error()

# Parse the page
soup = BeautifulSoup(response.content, "html.parser")
movie_data = {}

# Find the title
rx_title = re.compile(r"(?P<title>.+?) \(\d+\) - IMDb")
title = soup.find("title").text
match = rx_title.match(title)
if not match:
    show_error()
movie_data["title"] = match.group("title")

# Find the description
description = soup.find("div", class_="summary_text").text
movie_data["description"] = description.strip()

# Output the result
print()
print(movie_data)
