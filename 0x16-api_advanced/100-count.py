#!/usr/bin/python3
"""Function to count words in all hot posts of a given Reddit subreddit."""
import requests


def count_words(subreddit, word_list):
    # Base case: subreddit is invalid or no word_list provided
    if subreddit is None or len(word_list) == 0:
        return

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}  # Set a User-Agent header to avoid being blocked

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request was not successful
        data = response.json()

        # Check if the response contains any posts
        if "data" in data and "children" in data["data"]:
            posts = data["data"]["children"]
            word_counts = {}

            # Iterate over the posts and count the occurrences of each word
            for post in posts:
                if "data" in post and "title" in post["data"]:
                    title = post["data"]["title"]
                    for word in word_list:
                        word = word.lower()
                        count = title.lower().split().count(word)
                        if count > 0:
                            if word in word_counts:
                                word_counts[word] += count
                            else:
                                word_counts[word] = count

            # Sort the word counts by count (descending) and word (ascending)
            sorted_counts = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))

            # Print the sorted counts
            for word, count in sorted_counts:
                print(f"{word}: {count}")

    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)

    # Recursive call with next page
    if "data" in data and "after" in data["data"]:
        after = data["data"]["after"]
        count_words(subreddit, word_list, after)


count_words("python", ["python", "javascript", "java"])

