import json
import os

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

from utils import get_config

BLUE = "\033[1;34m"
RED = "\033[1;31m"
NORMAL = "\033[0m"


class Wiki:
    """
    A class to scrape Wikipedia articles asynchronously
    and store them in various formats.

    Attributes:
        __json_data: a list to store JSON data for scraped articles.
        __base_dir: the base directory to save scraped data.
    """

    def __init__(self):
        self.__base_dir: str = "./data/wiki/"
        self.__json_data: list = []

        if not os.path.exists(self.__base_dir):
            os.makedirs(self.__base_dir)

    async def __fetch(self,
                      session: aiohttp.ClientSession,
                      article_number: int,
                      progress_bar: tqdm) -> None:
        """
        Fetches a Wikipedia article asynchronously.

        :param session: the aiohttp client session.
        :param article_number: the article number.
        :param progress_bar: the tqdm progress bar object to track progress.

        :return: None
        """
        try:
            wiki_url = get_config().sources.wiki

            async with session.get(wiki_url) as response:
                response.raise_for_status()

                html = await response.text()

                wiki = BeautifulSoup(markup=html, features="html.parser")

                title = wiki.find("h1").text.strip()

                url = str(response.url)

                intro_summary = wiki.find("p").text.strip()

                body = wiki.find(name="div",
                                 class_="mw-parser-output").text.strip()

                sections = [section.text.strip() for section
                            in wiki.find_all("h2")]

                references = [ref["href"] for ref in
                              wiki.select(".references a[href^='http'],"
                                          " .references a[href^='https']")]

                categories = [cat.text.strip() for cat
                              in wiki.select(".mw-normal-catlinks ul li")]

                infobox = {}
                infobox_table = wiki.find(name="table", class_="infobox")

                if infobox_table:
                    rows = infobox_table.find_all("tr")

                    for row in rows:
                        cells = row.find_all(["th", "td"])

                        if len(cells) == 2:
                            key = cells[0].text.strip()
                            value = cells[1].text.strip()

                            infobox[key] = value

                data = {"ID": article_number,
                        "Title": title,
                        "URL": url,
                        "Introduction/Summary": intro_summary,
                        "Body": body,
                        "Sections/Headings": sections,
                        "References": references,
                        "Categories": categories,
                        "Infobox": infobox}

                self.__json_data.append(data)

                progress_bar.update(1)

        except aiohttp.ClientError as err:
            print(RED + f"Fetch Wiki Article {article_number}: {err}" + NORMAL)

    async def scrape(self, num_articles: int) -> None:
        """
        Scrapes Wikipedia articles asynchronously
        and stores them in various formats.

        :param num_articles: The number of articles to fetch.
        :return: None
        """
        async with aiohttp.ClientSession() as session:
            desc = BLUE + "Fetching Wikipedia Articles" + NORMAL

            progress_bar = tqdm(total=num_articles,
                                desc=desc,
                                unit="article")

            tasks = []
            for i in range(1, num_articles + 1):
                tasks.append(self.__fetch(session, i, progress_bar))
                if i % 30 == 0:
                    await asyncio.sleep(1)
                if i % 10 == 0:
                    await asyncio.gather(*tasks)
                    tasks = []

            await asyncio.gather(*tasks)

            progress_bar.close()

            data_frame = pd.DataFrame(self.__json_data)

            csv_file = os.path.join(self.__base_dir, "articles.csv")
            data_frame.to_csv(csv_file, index=False, encoding="utf-8")

            json_file = os.path.join(self.__base_dir, "articles.json")

            with open(file=json_file, mode="w", encoding="utf-8") as json_file:
                json.dump(obj=self.__json_data,
                          fp=json_file,
                          ensure_ascii=False,
                          indent=4)

            excel_file = os.path.join(self.__base_dir, "articles.xlsx")
            data_frame.to_excel(excel_file, index=False)

            parquet_file = os.path.join(self.__base_dir, "articles.parquet")
            data_frame.to_parquet(parquet_file, index=False)


async def get_wiki() -> None:
    """
    The main function of the Wikipedia scraper.

    :return: None
    """
    scraper = Wiki()

    while True:
        try:
            num_articles = int(input(BLUE + "\nHow Many >> " + NORMAL))

            if num_articles > 0:
                break

            print(RED + "Please enter a positive integer number!" + NORMAL)

        except ValueError:
            print(RED + "Please enter a valid integer number!" + NORMAL)

    await scraper.scrape(num_articles=num_articles)
