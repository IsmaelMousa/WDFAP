import os
import csv
import json
import pandas as pd
import aiohttp
import asyncio
from typing import Any
import feedparser
import newspaper
from bs4 import BeautifulSoup
from datetime import datetime
import random
from tqdm import tqdm

from utils import get_config

COLOR_BLUE = "\033[1;34m"
COLOR_RED = "\033[1;31m"
COLOR_RESET = "\033[0m"


async def fetch_google_news_articles(session: aiohttp.ClientSession,
                                     json_data: list[dict[str, Any]], csv_writer: csv.writer,
                                     progress_bar: tqdm, num_articles: int) -> None:
    """
        Fetch Google News articles asynchronously.

        :param session: Aiohttp client session
        :param json_data: List to store JSON data
        :param csv_writer: CSV writer object
        :param progress_bar: Progress bar object
        :param num_articles: Number of articles to fetch
        :return: None
    """
    try:
        sources = get_config().sources
        google_news_url = sources.google_news

        async with session.get(google_news_url) as response:
            response.raise_for_status()
            rss_feed = await response.text()

            parsed_feed = feedparser.parse(rss_feed)

            articles = parsed_feed.entries
            random.shuffle(articles)

            article_id = 1
            for entry in articles[:num_articles]:
                title = entry.get("title", "")

                link = entry.get("link", "")

                summary = entry.get("summary", "")

                published_date = entry.get("published", "")

                summary_text = BeautifulSoup(summary, features="html.parser").get_text()

                published_datetime = datetime.strptime(published_date, "%a, %d %b %Y %H:%M:%S %Z")

                content = await fetch_article_content(link)

                data = {
                    "ID": article_id,
                    "Title": title,
                    "URL": link,
                    "Summary": summary_text,
                    "Content": content,
                    "Published Date": published_datetime.strftime("%Y-%m-%d %H:%M:%S")
                }
                json_data.append(data)

                csv_writer.writerow([
                    article_id,
                    title,
                    link,
                    summary_text,
                    content,
                    published_datetime.strftime("%Y-%m-%d %H:%M:%S")
                ])

                progress_bar.update(1)
                article_id += 1

    except aiohttp.ClientError as e:
        print(COLOR_RED + f"Error fetching articles: {e}" + COLOR_RESET)


async def main_google_news() -> None:
    """
        Asynchronous function to fetch Google News articles and store them in various formats.

        This function prompts the user to input the number of Google News articles to fetch.
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
        base_dir = "./data/google_news/"
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
                "Summary",
                "Content",
                "Published Date"
            ])

            progress_bar = tqdm(total=num_articles, desc=COLOR_BLUE + "Fetching Google News Articles" + COLOR_RESET,
                                unit="article")

            await fetch_google_news_articles(session, json_data, csv_writer, progress_bar, num_articles)

            progress_bar.close()

        json_filename = os.path.join(base_dir, "articles.json")
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        df = pd.DataFrame(json_data)
        excel_filename = os.path.join(base_dir, "articles.xlsx")
        df.to_excel(excel_filename, index=False)

        parquet_filename = os.path.join(base_dir, "articles.parquet")
        df.to_parquet(parquet_filename, index=False)


async def fetch_article_content(url: str, max_retries: int = 3, retry_delay: float = 5.0) -> str:
    """
        Fetch the content of an article from the provided URL asynchronously.

        :param url: The URL of the article
        :param max_retries: Maximum number of retries in case of failure (default is 3)
        :param retry_delay: Delay between retries in seconds (default is 5.0)
        :return: The text content of the article
    """
    retries = 0
    while retries < max_retries:
        try:
            article = newspaper.Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            print(COLOR_RED + f"Error fetching article content: {e}" + COLOR_RESET)
            retries += 1
            if retries < max_retries:
                print(COLOR_RED + f"Retrying in {retry_delay} seconds..." + COLOR_RESET)
                await asyncio.sleep(retry_delay)
            else:
                print(COLOR_RED + "Max retries exceeded. Skipping article." + COLOR_RESET)
                return ""
