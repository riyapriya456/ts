import requests
from bs4 import BeautifulSoup
import json
import time

# The URLs of the websites to be checked
urls = ["https://www.1tamilmv.tips/", "https://tamilblasters.social/"]

# The initial page contents
page_contents = {}

# The Telegram bot API token and chat ID
bot_token = "5986546397:AAFH7xjmimXAKOY9Xttfr58w_vv11bEYDBE"
chat_id = "5493968060"

# The Telegram bot API endpoint for sending messages
bot_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

while True:
    # Loop through the websites to be checked
    for url in urls:
        # Retrieve the HTML content of the website
        response = requests.get(url)
        content = response.content

        # Parse the HTML content
        soup = BeautifulSoup(content, "html.parser")
        # Get the title of the website
        title = soup.find("title").get_text()

        # Get the new content from the website
        new_content = str(soup)

        # If there is new content, update the page_contents dictionary
        if url not in page_contents or new_content != page_contents[url]:
            page_contents[url] = new_content

    # Wait for some time before checking again
    time.sleep(300) # 5 minutes delay
