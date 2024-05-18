from sys import exit

import asyncio

from sources import get_google_news, get_wiki

BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
NORMAL = "\033[0m"


async def main():
    while True:
        print(BLUE + "Which data would you like to fetch?" + NORMAL + "\n")
        print(GREEN + ">> 1. Wikipedia Articles" + NORMAL)
        print(GREEN + ">> 2. Google News Articles" + NORMAL)
        print(GREEN + ">> 3. Both" + NORMAL)
        print(RED + ">> 4. Cancel" + NORMAL)

        choice = input("\nEnter Your Choice >> " + BLUE)

        match choice:
            case "1":
                print(BLUE + "Fetching Wikipedia Articles..." + NORMAL)
                await get_wiki()
                break
            case "2":
                print(BLUE + "Fetching Google News Articles..." + NORMAL)
                await get_google_news()
                break
            case "3":
                print(BLUE + "Fetching Both Wikipedia and Google News Articles..." + NORMAL)
                await asyncio.gather(get_wiki(), get_google_news())
                break
            case "4":
                print(RED + "Operation Canceled. Goodbye!" + NORMAL)
                exit()
            case _:
                print(RED + "Invalid choice. Please try again." + NORMAL)
