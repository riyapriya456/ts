import os
import asyncio
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyrogram import Client, filters
from plugins.messages import caption

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN", '/usr/bin/google-chrome-stable')
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")

driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH", '/usr/local/bin/chromedriver'), chrome_options=options)
driver.maximize_window()

@Client.on_message(filters.regex("index\.php\?/forum/topic"))
async def link_regex(c, m):
    try:
        link = str(m.text)
        txt = await m.reply_text("Scrapping magnet link, Please Wait")
        driver.get(link)
        p = driver.find_element(By.CLASS_NAME, "ipsImage_thumbnailed").get_attribute("src")
        magnet_link = driver.find_elements(By.CLASS_NAME, "ipsAttachLink_block")
        try:
            title = driver.find_element(By.XPATH, '//h1').text
        except NoSuchElementException:
            title = ""
        heading = f"**{title}**\n\n"
        msg = ""
        for link in magnet_link:
            tor = link.get_attribute("href")
            text = link.text
            msg += f"**Name : {text}**\n**Link:** {tor}\n\n-\n\n"
        if msg == "":
            await m.send_message(-1001847917098, "No Magnet links Found")
            await m.message.delete()
        elif msg != "":
            reply_text = f"{msg}"
            await c.send_photo(-1001847917098, p, caption=heading)
            await c.send_message(-1001847917098, reply_text)
            await txt.delete()

    except Exception as e:
        print(e)
        await c.send_message(-1001847917098, 'Some error occurred')
        await txt.delete()

async def send_screenshot(c):
    channel = -1001847917098
    while True:
        txt = await c.send_message(channel, "Getting screenshot of latest movies of 1TamilMv")
        N = 7
        name = ''.join(random.choices(string.ascii_uppercase +
                                      string.digits, k=N))
        driver.get("https://www.1tamilmv.bond/")
        photo = name + ".png"
        driver.save_screenshot(photo)

        N = 7
        name = ''.join(random.choices(string.ascii_uppercase +
                                      string.digits, k=N))
        driver.get("https://www.tamilblasters.guru/")
        await txt.edit(text="Got Screenshot of 1TamilMv.autos. Now Getting screenshot of latest movies of TamilBlasters")
        photo1 = name + ".png"
        driver.save_screenshot(photo1)
        await txt.delete()

        await c.send_photo(channel, photo, caption="**Screenshot of latest movies of 1TamilMV.autos**")
        await c.send_photo(channel, photo1, caption="**Screenshot of latest movies of TamilBlasters.kim**")

        os.remove(photo)
        os.remove(photo1)
        await asyncio.sleep(1800)  # sleep for 30 minutes
