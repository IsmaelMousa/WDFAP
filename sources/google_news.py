import os
import json
from datetime import datetime

import asyncio
import aiohttp
import feedparser
import newspaper
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

from utils import get_config

BLUE = "\033[1;34m"
RED = "\033[1;31m"
NORMAL = "\033[0m"


class GoogleNews:
    """
    A class to scrape news articles from Google News RSS feed
    and save them in multiple formats.

    Attributes:
        __base_dir: The base directory to store the scraped articles.
        __json_data: A list to store article data as dictionaries.
    """

    def __init__(self):
        self.__base_dir: str = "./data/google_news/"
        self.__json_data: list = []

    @staticmethod
    async def __fetch_content(url: str) -> str:
        """
        Fetches the content of a news article from the given URL.

        :param url: the URL of the news article.
        :return: the text content of the article.
        """
        retries = 0

        while retries < 3:
            try:
                article = newspaper.Article(url)
                article.download()
                article.parse()

                return article.text

            except Exception:
                retries += 1

        return ""

    async def __fetch_and_process_article(self,
                                          entry: dict,
                                          progress_bar: tqdm) -> None:
        """
        Fetches and processes a single article entry from the RSS feed.

        :param entry: rhe dictionary containing article metadata.
        :param progress_bar: the progress bar to update fetching progress.
        """
        title = entry.get("title", "")

        link = entry.get("link", "")

        published_date = entry.get("published", "")

        summary = entry.get("summary", "")
        summary_text = BeautifulSoup(summary, features="html.parser").get_text()

        published_datetime = datetime.strptime(published_date,
                                               "%a, %d %b %Y %H:%M:%S %Z")

        body = await self.__fetch_content(link)

        data = {
            "Title": title,
            "URL": link,
            "Summary": summary_text,
            "Body": body,
            "Published Date": published_datetime.strftime("%Y-%m-%d %H:%M:%S")}

        self.__json_data.append(data)

        progress_bar.update(1)

    async def scrape(self, num_articles: int) -> None:
        """
        Scrapes the specified number of articles from Google News RSS feed.

        :param num_articles: the number of articles to scrape.
        :return: None
        """
        async with aiohttp.ClientSession() as session:
            if not os.path.exists(self.__base_dir):
                os.makedirs(self.__base_dir)

            csv_file = os.path.join(self.__base_dir, "articles.csv")

            desc = BLUE + "Fetching Google News Articles" + NORMAL
            progress_bar = tqdm(total=num_articles,
                                desc=desc,
                                unit="article")

            google_news_url = get_config().sources.google_news

            async with session.get(google_news_url) as response:
                response.raise_for_status()

                rss_feed = await response.text()
                parsed_feed = feedparser.parse(rss_feed)

                articles = parsed_feed.entries[:num_articles]

                tasks = [self.__fetch_and_process_article(entry, progress_bar)
                         for entry in articles]

                await asyncio.gather(*tasks)

            progress_bar.close()

            data_frame = pd.DataFrame(data=self.__json_data)
            data_frame.to_csv(path_or_buf=csv_file, index=False)

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


async def get_google_news() -> None:
    """
    Prompts the user for the number of articles to scrape
    and starts the scraping process.

    :return: None
    """
    scraper = GoogleNews()

    while True:
        try:
            num_articles = int(input(BLUE + "\nHow Many >> " + NORMAL))

            if num_articles > 0:
                break

            print(RED + "Please enter a positive integer number!" + NORMAL)

        except ValueError:
            print(RED + "Please enter a valid integer number!" + NORMAL)

    await scraper.scrape(num_articles=num_articles)
