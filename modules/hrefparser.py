import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re

def href_parser(array):
    ua = UserAgent()
    tmp_array = {}
    regexp = re.compile('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
    for i in range(len(array)):
        header = {'user_agent':ua.random}
        response = requests.get(array[i], headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        descriptions = soup.find(class_='TextBlock')
        if not regexp.findall(str(descriptions.text)):
            pass
        else:
            tmp_array[array[i]] = regexp.findall(str(descriptions.text))[0]
    return tmp_array