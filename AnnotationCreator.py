import json
import os
import shutil
import sys
import html
import logging
from datetime import datetime, timedelta
import time
import requests
import urllib.parse

from PIL import Image
from bs4 import BeautifulSoup, Tag
from shutil import copyfile

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
    dataset = loadJson("data/items_data.json")
    i = 0
    for item in dataset:
        name, filename_image, filename_icon = item.values()
        file_icon = filename_icon.split("/")[2].replace(".png","")

        shutil.copy(filename_icon, "data/dataset/images/")
        img = Image.open(filename_icon)
        logger.info(img.format)
        img.save("data/dataset/images/"+file_icon+".png", format="png")

        f = open("data/dataset/labels/"+file_icon+".txt","w", encoding="utf-8")
        f.write(str(i)+" 0.5 0.5 1 1")
        f.close()
        i = i+1

    f = open("data/dataset/data.yaml","w", encoding="utf-8")
    f.write("train: ../data/dataset/images\n")
    f.write("val: ../data/dataset/images\n")
    f.write("\n")
    f.write("nc: "+str(i)+"\n")
    s = ""

    for item in dataset:
        name, filename_image, filename_icon = item.values()
        s = s + "\'"+name.replace("\'","")+ "\', "

    f.write("names: ["+s+"]")
    f.close()