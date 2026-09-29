import requests
import json
import os
import time
from datetime import datetime

# HackerNews API endpoints
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required request header
headers = {
    "User-Agent": "TrendPulse/1.0"
}

# Keywords used to identify each category
categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}


def fetch_top_story_ids():
    """Fetch the first 500 top story IDs from HackerNews."""
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers, timeout=10)
        response.raise_for_status()

        story_ids = response.json()
        return story_ids[:500]

    except requests.RequestException as error:
        print("Failed to fetch top stories:", error)
        return []


def fetch_story(story_id):
    """Fetch details for one HackerNews story."""
    try:
        url = ITEM_URL.format(story_id)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        return None


def find_category(title):
    """Return the first category whose keyword appears in the title."""
    title_lower = title.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category

    return None


def main():

    # Step 1: Get the top 500 story IDs
    story_ids = fetch_top_story_ids()

    if not story_ids:
        print("No story IDs were collected.")
        return

    print(f"Found {len(story_ids)} top stories.")

    # Fetch story details only once and keep successful results
    stories = []

    for story_id in story_ids:
        story = fetch_story(story_id)

        if story is not None and story.get("title"):
            stories.append(story)

    print(f"Successfully fetched {len(stories)} stories.")

    # Store up to 25 stories in each category
    categorized_stories = []

    for category, keywords in categories.items():

        category_count = 0

        for story in stories:

            # Stop after collecting 25 stories for this category
            if category_count >= 25:
                break

            title = story.get("title", "")
            matched_category = find_category(title)

            if matched_category == category:

                collected_story = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", ""),
                    "collected_at": datetime.now().isoformat()
                }

                categorized_stories.append(collected_story)
                category_count += 1

        # Required 2-second wait between category loops
        time.sleep(2)

        print(f"{category}: {category_count} stories collected.")

    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Create today's filename
    date_string = datetime.now().strftime("%Y%m%d")
    output_file = f"data/trends_{date_string}.json"

    # Save the collected stories
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(categorized_stories, file, indent=4, ensure_ascii=False)

    print(f"Collected {len(categorized_stories)} stories.")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()
