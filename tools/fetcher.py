import asyncio
import sys

from sources import main_google_news, main_wikipedia

COLOR_BLUE = "\033[1;34m"
COLOR_GREEN = "\033[1;32m"
COLOR_RED = "\033[1;31m"
COLOR_RESET = "\033[0m"


async def main():
    while True:
        print(COLOR_BLUE + "Which data would you like to fetch?" + COLOR_RESET + "\n")
        print(COLOR_GREEN + ">> 1. Wikipedia Articles" + COLOR_RESET)
        print(COLOR_GREEN + ">> 2. Google News Articles" + COLOR_RESET)
        print(COLOR_GREEN + ">> 3. Both" + COLOR_RESET)
        print(COLOR_RED + ">> 4. Cancel" + COLOR_RESET)

        choice = input("\nEnter Your Choice >> " + COLOR_BLUE)

        match choice:
            case "1":
                print(COLOR_BLUE + "Fetching Wikipedia Articles..." + COLOR_RESET)
                await main_wikipedia()
                break
            case "2":
                print(COLOR_BLUE + "Fetching Google News Articles..." + COLOR_RESET)
                await main_google_news()
                break
            case "3":
                print(COLOR_BLUE + "Fetching Both Wikipedia and Google News Articles..." + COLOR_RESET)
                await asyncio.gather(main_wikipedia(), main_google_news())
                break
            case "4":
                print(COLOR_RED + "Operation Canceled. Goodbye!" + COLOR_RESET)
                sys.exit()
            case _:
                print(COLOR_RED + "Invalid choice. Please try again." + COLOR_RESET)
