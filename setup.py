import json
from pathlib import Path

from setuptools import setup, find_packages

with open(file="requirements.txt", mode="r") as f:
    requirements = f.read().splitlines()

DESCRIPTION = ("Python tool for asynchronously fetching and storing"
               " articles from web sources in various formats"
               " such as csv, json, xlsx, and parquet.")

with open(file="README.md", mode="r") as f:
    long_description = f.read()

version_file = Path(__file__).parent / "version.json"

with open(file=version_file, mode="r") as f:
    version = json.load(f)

__version__ = f"{version['major']}.{version['minor']}.{version['patch']}"

dependency_links = ["https://pypi.org/project/HTMLParser/0.0.2/",
                    "https://pypi.org/project/beautifulsoup4/4.12.3/",
                    "https://pypi.org/project/requests/2.32.3/",
                    "https://pypi.org/project/aiohttp/3.9.5/",
                    "https://pypi.org/project/openpyxl/3.1.2/",
                    "https://pypi.org/project/pandas/2.2.2/",
                    "https://pypi.org/project/tqdm/4.66.4/",
                    "https://pypi.org/project/feedparser/6.0.11/",
                    "https://pypi.org/project/newspaper3k/0.2.8/",
                    "https://pypi.org/project/lxml-html-clean/0.1.1/",
                    "https://pypi.org/project/praw/7.7.1/",
                    "https://pypi.org/project/pyarrow/16.0.0/",
                    "https://pypi.org/project/fastparquet/2024.2.0/",
                    "https://pypi.org/project/PyYAML/6.0.1/"]

setup(
    name="WDFAP",
    version=__version__,
    packages=find_packages(),
    dependency_links=dependency_links,
    author="Ismael Mousa",
    author_email="ismaelramzimousa@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IsmaelMousa/WDFAP",
    install_requires=requirements,
    python_requires=">=3.10",
    license="MIT", )
