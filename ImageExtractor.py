import json
import os
import sys
import html
import logging
from datetime import datetime, timedelta
import time
import requests
import urllib.parse
from bs4 import BeautifulSoup, Tag

try:
    os.mkdir("logs")
except:
    pass

# Logger
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("__name__")
fh = logging.FileHandler("logs/" + str(datetime.now().strftime("%Y%m%d_%H_%M_%S")) + '.log')

# create console handler with a higher log level
ch = logging.StreamHandler()

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger

if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(ch)
logger.addHandler(fh)

execution_path = os.getcwd()


def loadJson(filepath):
    f = open(filepath, "r", encoding="utf-8")
    j = json.load(f)
    return j


def get_filenames(path):
    return next(os.walk(path), (None, None, []))[2]  # [] if no file


if __name__ == '__main__':
    items = loadJson("data/items.en.json")
    filenames = get_filenames("data/html")
    data = []
    for filename in filenames:
        filename_no_extension = filename.replace('.html', '')
        fixed_filename = urllib.parse.unquote_plus(filename.replace('%5', '/')).replace('_', ' ').replace('.html', '')
        f = open("data/html/" + filename, encoding="utf-8")

        soup = BeautifulSoup(f.read())
        mydivs = soup.find_all("div", {"class": "va-infobox-icon-cont"})
        category = soup.find_all("div", {"class": "page-header__categories"})

        if len(mydivs) > 1:
            #logger.error("Incorrect div found" + str(len(mydivs)) + " - " + fixed_filename)
            continue
        if len(mydivs) == 0 and (len(category) == 0 or "Weapons" not in category[0].text):
            continue
        if len(mydivs) == 0:
            #logger.error("0 div found" + " - " + fixed_filename)
            continue

        mainimage = list(soup.find_all("td", {"class": "va-infobox-mainimage-image"})[0].children)[0]
        icon = list(soup.find_all("td", {"class": "va-infobox-icon"})[0].children)[0]

        url_image = mainimage.attrs["href"]
        url_icon = icon.attrs["href"]

        filename_image = "data/images/" + filename_no_extension + ".png"
        urllib.request.urlretrieve(url_image, filename_image)

        filename_icon = "data/icons/" + filename_no_extension + ".png"
        urllib.request.urlretrieve(url_icon, filename_icon)

        data.append({"name": fixed_filename, "image": filename_image, "icon": filename_icon})

    f = open("data/items_data.json", "w")
    json.dump(data, f, indent=0)
    f.close()
