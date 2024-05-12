# DFAP (Data Fetcher And Preparer)

Welcome to the **DFAP** project! This tool allows you to fetch articles from **web sources** in various
formats such as `csv`, `json`, `xlsx`, and `parquet`, providing you with a versatile way to access and analyze diverse
sets of data.

## Installation

To get started with the **DFAP**, follow these simple steps:

1. Clone this repository to your local machine:

```zsh
git clone git@github.com:IsmaelMousa/DFAP.git
```

2. Navigate to the **DFAP** directory:

```zsh
cd DFAP
```

3. Setup virtual environment:

```zsh
python3 -m venv .venv
```

4. Activate the virtual environment:

```zsh
source .venv/bin/activate
```

5. Install the required dependencies:

```zsh
make install
```

## Usage

The **DFAP** provides a user-friendly interface for fetching articles. For now you can choose to fetch articles from
**Wikipedia**, **Google News**, or both simultaneously. The fetched data is stored in the `data/` directory in different
formats
for easy access and analysis.

1. Run the **DFAP** to start fetching articles

```zsh
make fetch
```

2. After that, the terminal will ask you:

```

```

## Structure

The **DFAP** files is structured as follows:

- **fetcher.py**: Contains the main logic for fetching articles from **Wikipedia** and **Google News** based on user
  input.
- **google_news.py**: For fetching **Google News** articles asynchronously using aiohttp.
- **wiki.py**: For fetching **Wikipedia** articles asynchronously using aiohttp.
- **fetcher.py**: Entry point of the application, It prompts the user to choose which data to fetch and calls the
  respective functions.
- **Makefile**: Provides commands for installing dependencies and running the application.
- **requirements.txt**: Lists all the required dependencies for the project.
- **data/**: Directory where fetched articles are stored in various formats (`csv`, `json`, `xlsx`, `parquet`).

## Libraries/Dependencies

- **aiohttp**: Used for async **HTTP client/server** for asyncio.
- **asyncio**: Used for async **I/O**.
- **beautifulsoup4**: Used for parsing and extracting structured data from **HTML** content.
- **pandas**: Used for data manipulation.
- **csv**: Used for reading and writing `CSV` files.
- **json**: Used for encoding and decoding `JSON` data.
- **os**: Used for interacting with the operating system.
- **sys**: Used for interacting with the Python interpreter.
- **tqdm**: Used for adding progress bars to loops.
- **feedparser**: Used for parsing RSS and Atom feeds.
- **newspaper**: Used for extracting and curating articles from websites.
- **openpyxl**: Used for reading and writing `Excel` files.
- **pyarrow**: Used for working with Apache Arrow data.
- **fastparquet**: Used for working with `Parquet` files