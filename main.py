import re
from selenium import webdriver
import time
import pickle
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from CONFIG import PAGES
from modules.hrefparser import href_parser
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class YaParser(object):
    def __init__(self):
        self.array = {}
        self.current_page = 0
        chrome_options = Options()
        chrome_options.add_argument(r"user-data-dir=C:\Users\decision.marketing\AppData\Local\Google\Chrome\User Data\Default")
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='chrome\chromedriver.exe')
        self.main()


    def _check_login(self):
        check = self.driver.execute_script('''
var email = document.getElementsByClassName('button__text');
return email[0].textContent;
''')
        try:
            if re.search('Войти', str(check)).group() == "Войти":
                self._load_cookie()
        except AttributeError:
            return False

    def __load_script(self, name):
        if name == 'href_script':
            with open('modules\scripts\href_script.js', 'r') as js_script_:
                js_script = js_script_.read()
                return js_script

    def authorization(self):
        from CONFIG import LOGIN as login
        from CONFIG import PASSWORD as password
        from CONFIG import ATTEMPS as attemps
        self.driver.get('https://passport.yandex.ru/')

        for i in range(attemps):
            try:
                elem_login = self.driver.find_element_by_id('passp-field-login')
                elem_login.send_keys(login, Keys.RETURN)
                break
            except NoSuchElementException:
                time.sleep(0.5)

        for i in range(attemps):
            try:
                elem_login = self.driver.find_element_by_id('passp-field-passwd')
                elem_login.send_keys(password, Keys.RETURN)
                break
            except NoSuchElementException:
                time.sleep(0.5)

    def _save_cookie(self):
        cookie = self.driver.get_cookies()
        with open('cookie_parser.pickle', 'wb') as f:
            pickle.dump(cookie, f)

    def _load_cookie(self):
        try:
            with open('cookie_parser.pickle', 'rb') as f:
                pass
        except FileNotFoundError:
            with open('cookie_parser.pickle', 'wb') as f:
                pass

        with open('cookie_parser.pickle', 'rb') as f:
            try:
                cookies = pickle.load(f)
                if len(cookies) > 1:
                    for cookie in cookies:
                        if 'expiry' in cookie:
                            del cookie['expiry']
                        self.driver.add_cookie(cookie)
                # else:
                #     print('No cookie')
                #     return False
            except EOFError:
                self.authorization()

    def main_array(self, array):
        for key in array:
            self.array[key] = array[key]

    def go_next_page(self):
        if self.current_page == 0:
            self.current_page += 1
            return 'https://yandex.ru/uslugi/cab/orders?rubric=%2Fkomp_utery-i-it%2Fdrugoe&rubric=%2Fkomp_utery-i-it%2Fsajty-pod-kluc'
        if self.current_page > 0:
            url =  'https://yandex.ru/uslugi/cab/orders?p={}&rubric=%2Fkomp_utery-i-it%2Fdrugoe&rubric=%2Fkomp_utery-i-it%2Fsajty-pod-kluc'.format(self.current_page)
            self.current_page += 1
            return url


    def _close(self, time_=0):
        time.sleep(time_)
        self.driver.close()

    def main(self):
        self.driver.get('https://yandex.ru')
        self._check_login()
        for attempting in range(PAGES):
            self.driver.get(self.go_next_page())
            array = self.driver.execute_script(self.__load_script(name='href_script'))
            phones = href_parser(array)
            if len(phones) > 0:
                self.main_array(phones)
            print(self.array)
        self._save_cookie()
        self._close(time_=2)



if __name__ == "__main__":
    start = time.time()
    parser = YaParser()
    finish = round(time.time() - start)
    print('All time: ', finish)
    print('For one page: ', round(finish/PAGES))