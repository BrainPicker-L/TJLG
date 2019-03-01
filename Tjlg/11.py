import requests
from PIL import Image
import pytesseract
from lxml import etree
from bs4 import BeautifulSoup
import re
import json
import os


imgry= Image.open("gray-checkcode1.gif")
text = pytesseract.image_to_string(imgry,lang='fontyp')
print(text)