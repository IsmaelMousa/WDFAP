import sys
import asyncio

from sources import get_google_news, get_wiki

BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
NORMAL = "\033[0m"


async def main():
    while True:
        print(BLUE + "Choose Your Data Source Option" + NORMAL + "\n")
        print(NORMAL + ">> 1. " + GREEN + "Wikipedia" + NORMAL)
        print(NORMAL + ">> 2. " + GREEN + "Google News" + NORMAL)
        print(NORMAL + ">> 3. " + GREEN + "Both" + NORMAL)
        print(NORMAL + ">> 4. " + RED + "Cancel" + NORMAL)

        choice = input(BLUE + "\nEnter Your Choice >> " + NORMAL)

        match choice:
            case "1":
                print(GREEN + "\nWikipedia Articles" + NORMAL)
                await get_wiki()
                break
            case "2":
                print(GREEN + "\nGoogle News Articles" + NORMAL)
                await get_google_news()
                break
            case "3":
                print(GREEN + "\nBoth Wiki & Google News Articles" + NORMAL)
                await asyncio.gather(get_wiki(), get_google_news())
                break
            case "4":
                print(RED + "\nOperation Canceled. Goodbye!" + NORMAL)
                sys.exit()
            case _:
                print(RED + "\nInvalid choice. Please try again." + NORMAL)
