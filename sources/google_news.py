import os
import csv
import json
from datetime import datetime

from bs4 import BeautifulSoup
from tqdm import tqdm
import aiohttp
import asyncio
import feedparser
import newspaper
import pandas as pd

from utils import get_config

BLUE = "\033[1;34m"
RED = "\033[1;31m"
NORMAL = "\033[0m"


class GoogleNews:
    """
    A class to scrape Google News articles asynchronously and store them in various formats.

    Attributes:
        __base_dir (str): The base directory to save scraped data.
        __json_data (list): A list to store JSON data for scraped articles.
    """

    def __init__(self):
        self.__json_data = []
        self.__base_dir = "./data/google_news/"

    async def __fetch_content(self, url: str, max_retries: int = 3, retry_delay: float = 5.0) -> str:
        """
        Fetch the content of an article from the provided URL asynchronously.

        :param url: The URL of the article.
        :param max_retries: Maximum number of retries in case of failure (default is 3).
        :param retry_delay: Delay between retries in seconds (default is 5.0).
        :return: The text content of the article.
        """
        retries = 0
        while retries < max_retries:
            try:
                article = newspaper.Article(url)
                article.download()
                article.parse()
                return article.text
            except Exception:
                retries += 1
                print(BLUE + "Retrying to fetch content..." + NORMAL)
                await asyncio.sleep(retry_delay)
        return ""

    async def __fetch_and_process_article(self, session: aiohttp.ClientSession, csv_writer: csv.writer,
                                          progress_bar: tqdm, entry: dict) -> None:
        """
        Fetch and process a single Google News article asynchronously.

        :param session: Aiohttp client session.
        :param csv_writer: CSV writer object.
        :param progress_bar: Progress bar object.
        :param entry: Dictionary containing article information.
        :return: None
        """
        title = entry.get("title", "")
        link = entry.get("link", "")
        summary = entry.get("summary", "")
        published_date = entry.get("published", "")
        summary_text = BeautifulSoup(summary, features="html.parser").get_text()
        published_datetime = datetime.strptime(published_date, "%a, %d %b %Y %H:%M:%S %Z")

        body = await self.__fetch_content(link)

        data = {
            "Title": title,
            "URL": link,
            "Summary": summary_text,
            "Body": body,
            "Published Date": published_datetime.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.__json_data.append(data)

        csv_writer.writerow([
            title,
            link,
            summary_text,
            body,
            published_datetime.strftime("%Y-%m-%d %H:%M:%S")
        ])

        progress_bar.update(1)

    async def scrape(self, num_articles: int) -> None:
        """
        Scrapes Google News articles asynchronously and stores them in various formats.

        :param num_articles: The number of articles to fetch.
        :return: None
        """
        async with aiohttp.ClientSession() as session:
            if not os.path.exists(self.__base_dir):
                os.makedirs(self.__base_dir)

            csv_filename = os.path.join(self.__base_dir, "articles.csv")
            with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([
                    "Title",
                    "URL",
                    "Summary",
                    "Body",
                    "Published Date"
                ])

                progress_bar = tqdm(total=num_articles, desc=BLUE + "Fetching Google News Articles" + NORMAL,
                                    unit="article")

                sources = get_config().sources
                google_news_url = sources.google_news
                async with session.get(google_news_url) as response:
                    response.raise_for_status()
                    rss_feed = await response.text()

                    parsed_feed = feedparser.parse(rss_feed)

                    articles = parsed_feed.entries[:num_articles]

                    tasks = []
                    for entry in articles:
                        task = self.__fetch_and_process_article(session, csv_writer, progress_bar, entry)
                        tasks.append(task)

                    await asyncio.gather(*tasks)

                progress_bar.close()

            json_filename = os.path.join(self.__base_dir, "articles.json")
            with open(json_filename, "w", encoding="utf-8") as json_file:
                json.dump(self.__json_data, json_file, ensure_ascii=False, indent=4)

            df = pd.DataFrame(self.__json_data)
            excel_filename = os.path.join(self.__base_dir, "articles.xlsx")
            df.to_excel(excel_filename, index=False)

            parquet_filename = os.path.join(self.__base_dir, "articles.parquet")
            df.to_parquet(parquet_filename, index=False)


async def get_google_news() -> None:
    """
    The main function of the Google News scraper.

    Prompts the user to enter the number of articles to fetch, then starts the scraping process.

    :return: None
    """
    scraper = GoogleNews()
    while True:
        try:
            num_articles = int(input("\n" + "Enter The Number of Articles to Fetch >> " + BLUE))
            if num_articles > 0:
                break
            else:
                print(RED + "Please enter a positive integer number!" + NORMAL)
        except ValueError:
            print(RED + "Please enter a valid integer number!" + NORMAL)
    await scraper.scrape(num_articles)
