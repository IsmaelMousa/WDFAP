import aiohttp
import asyncio
import os
import csv
import json
import pandas as pd
from typing import Any
from tqdm import tqdm
from bs4 import BeautifulSoup

from utils import get_config

COLOR_BLUE = "\033[1;34m"
COLOR_RED = "\033[1;31m"
COLOR_RESET = "\033[0m"


async def fetch_wikipedia(session: aiohttp.ClientSession, article_number: int,
                          json_data: list[dict[str, Any]], csv_writer: csv.writer,
                          progress_bar: tqdm) -> None:
    """
        Fetch Wikipedia article asynchronously.

        :param session: Aiohttp client session
        :param article_number: The article number
        :param json_data: List to store JSON data
        :param csv_writer: CSV writer object
        :param progress_bar: Progress bar object
        :return: None
    """
    try:
        sources = get_config().sources
        wiki_url = sources.wiki
        async with session.get(wiki_url) as response:
            response.raise_for_status()

            html = await response.text()

            wiki = BeautifulSoup(markup=html, features="html.parser")

            title = wiki.find("h1").text.strip()

            url = str(response.url)

            intro_summary = wiki.find("p").text.strip()

            content = wiki.find(name="div", class_="mw-parser-output").text.strip()

            sections = [section.text.strip() for section in wiki.find_all("h2")]

            references = [ref["href"] for ref in
                          wiki.select(".references a[href^='http'], .references a[href^='https']")]

            categories = [cat.text.strip() for cat in wiki.select(".mw-normal-catlinks ul li")]

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

            data = {
                "ID": article_number,
                "Title": title,
                "URL": url,
                "Introduction/Summary": intro_summary,
                "Content": content,
                "Sections/Headings": sections,
                "References": references,
                "Categories": categories,
                "Infobox": infobox
            }

            json_data.append(data)

            csv_writer.writerow([
                article_number,
                title,
                url,
                intro_summary,
                sections,
                references,
                categories,
                infobox
            ])

            progress_bar.update(1)

    except aiohttp.ClientError as e:
        print(COLOR_RED + f"Error fetching Wikipedia article {article_number}: {e}" + COLOR_RESET)


async def main_wikipedia() -> None:
    """
        Asynchronous function to fetch Wikipedia articles and store them in various formats.

        This function prompts the user to input the number of Wikipedia articles to fetch.
        It then asynchronously fetches the articles using aiohttp, stores the data in CSV, JSON,
        Excel, and Parquet formats, and saves them in the specified output directory.

        :return: None
    """
    while True:
        try:
            num_articles = int(input("\n" + "Enter The Number of Articles to Fetch >> " + COLOR_BLUE))
            if num_articles > 0:
                break
            else:
                print(COLOR_RED + "Please enter a positive integer number!" + COLOR_RESET)
        except ValueError:
            print(COLOR_RED + "Please enter a valid integer number!" + COLOR_RESET)

    async with aiohttp.ClientSession() as session:
        base_dir = "./data/wiki/"
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        json_data = []
        csv_filename = os.path.join(base_dir, "articles.csv")
        with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                "ID",
                "Title",
                "URL",
                "Introduction/Summary",
                "Sections/Headings",
                "References",
                "Categories",
                "Infobox"
            ])

            progress_bar = tqdm(total=num_articles, desc=COLOR_BLUE + "Fetching Wikipedia Articles" + COLOR_RESET,
                                unit="article")

            tasks = []
            for i in range(1, num_articles + 1):
                tasks.append(fetch_wikipedia(session, i, json_data, csv_writer, progress_bar))
                if i % 30 == 0:
                    await asyncio.sleep(1)
                if i % 10 == 0:
                    await asyncio.gather(*tasks)
                    tasks = []
            await asyncio.gather(*tasks)

            progress_bar.close()

        json_filename = os.path.join(base_dir, "articles.json")
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        df = pd.DataFrame(json_data)
        excel_filename = os.path.join(base_dir, "articles.xlsx")
        df.to_excel(excel_filename, index=False)

        parquet_filename = os.path.join(base_dir, "articles.parquet")
        df.to_parquet(parquet_filename, index=False)
