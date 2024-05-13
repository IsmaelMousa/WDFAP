import asyncio
import time
from tools import fetcher

COLOR_GREEN = "\033[1;32m"

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(fetcher.main())
    print(COLOR_GREEN + "\nCompleted Successfully!\nTime Taken:", round(time.time() - start_time, 2), COLOR_GREEN + "s")
