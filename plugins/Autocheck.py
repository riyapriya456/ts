import requests
from bs4 import BeautifulSoup
import json
import time

# The URLs of the websites to be checked
urls = ["https://www.1tamilmv.tips/", "https://tamiblasters.social/"]

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

        # Check if there is new content on the website
        if url not in page_contents or new_content != page_contents[url]:
            # If there is new content, send a notification to the user via Telegram bot
            message = f"New content is available on {title}:\n{url}"
            payload = {
                "chat_id": chat_id,
                "text": message
            }
            response = requests.post(bot_api_url, data=payload)

            # Update the page contents
            page_contents[url] = new_content

    # Wait for some time before checking again
    time.sleep(300) # 5 minutes delay
