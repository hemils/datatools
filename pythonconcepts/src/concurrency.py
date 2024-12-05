import time
import random
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_post(post_id: int) -> dict:
    # Value check - Posts on the API only go up to ID of 100
    if post_id > 100:
        raise ValueError("Parameter `post_id` must be less than or equal to 100")

    # API URL
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

    # Sleep to imitate a long-running process
    time_to_sleep = random.randint(1, 10)
    time.sleep(time_to_sleep)

    # Fetch the data and return it
    r = requests.get(url)
    r.raise_for_status()
    result = r.json()
    # To indicate how much time fetching took
    result["fetch_time"] = time_to_sleep
    # Remove the longest key-value pair for formatting reasons
    del result["body"]
    return result


if __name__ == "__main__":
    time_start = datetime.now()
    print("Starting to fetch posts...\n")

    # Simple iteration
    with ThreadPoolExecutor() as tpe:
        futures = [tpe.submit(get_post, id) for id in range(1,101)]
        for future in as_completed(futures):
            result = future.result()
            print(result)
    
    # Print total duration
    time_end = datetime.now()
    print(f"\nAll posts fetched! Took: {(time_end - time_start).seconds} seconds.")
