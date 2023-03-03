# This module pulls the MPEP day from the internet
# Saves each chapter as a separate document

import requests
from bs4 import BeautifulSoup
import os
import markdownify
from tqdm import tqdm

chapter_numbers = list(range(100,3000,100))

for chapter in tqdm(chapter_numbers, desc=" outer", position=0):
    URL = f"https://www.uspto.gov/web/offices/pac/mpep/mpep-{chapter:04}.html" #cast into four digits
    page = requests.get(URL)
    os.mkdir(f"data/{chapter:04}")
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find("div", {"id": "article"})
    sections = div.find_all("li")
    for section in tqdm(sections, desc=" inner loop", position=1, leave=False):
        section_number = section.find('a')['href']
        URL = f"https://www.uspto.gov/web/offices/pac/mpep/{section_number}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        div = soup.find_all("div", class_="Section")

        h = markdownify.markdownify(str(div), heading_style="ATX")
        
        filename = f"data/{chapter:04}/{section_number}.txt"
        with open(filename, "w") as file:
            file.write(h)




