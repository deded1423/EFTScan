import json
import os
import sys
import logging
from datetime import datetime, timedelta
import time
import requests
import urllib.parse

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

if __name__ == '__main__':
    items = loadJson("data/items.en.json")
    url_wiki = "https://escapefromtarkov.fandom.com/wiki/"

    i = 0

    for _, item in items.items():
        logger.info(i)
        i = i + 1
        id, name, short_name = item.values()
        fixed_name = name.replace(' ','_')
        full_url = url_wiki + fixed_name
        r = requests.get(url_wiki+fixed_name)
        if (r.status_code != 200):
            logger.error("ERROR: "+str(r.status_code)+" - "+str(item) + " - "+full_url)
            continue
        fixed_name = urllib.parse.quote_plus(fixed_name.replace('/','%5'))
        f = open("data/html/"+fixed_name+".html", "w", encoding="utf-8")
        f.write(r.text)
        f.close()
        r.close()
        #time.sleep(0.1)




























