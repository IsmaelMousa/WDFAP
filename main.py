from time import time

import asyncio

from tools import fetcher


GREEN = "\033[1;32m"

if __name__ == "__main__":
    start_time = time()
    asyncio.run(fetcher.main())
    end_time = time()

    print(GREEN + "\nCompleted Successfully!\nTime Taken:", round(end_time - start_time, 2), GREEN + "s")
