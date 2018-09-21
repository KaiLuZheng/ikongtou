#!/usr/bin/python3


import logging
#logging.basicConfig(level = logging.DEBUG)


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as bs
import re

import sys
import time 

# headless
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# failed on centos , so add this
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")

# not api , because the params can not be gained easily

translator_baidu_urlhost = 'https://fanyi.baidu.com/?aldtype=85#en/zh/'


# how to use one chrome ?
class baiduTranslator:
    def translateWord(self, word):
        # check the word
        simple_meanning = self.translateWord_xsimple(self.requestor_page(word))

        return simple_meanning

       
    def translateWord_xsimple(self, html):
        '''
        the_word pronunciation 
        '''
        soup = bs(html, 'html.parser')
        dict_output = soup.find_all(class_ = 'dictionary-output')

        title = dict_output[0].find_all(class_ = 'dictionary-title')[0]

        the_word = title.h3.text

        #the_pronunciation = 
        spelldiv = str(title.find_all(class_ = 'dictionary-spell')[0])
        spelllist = re.findall(r'<span>.*?</b>', spelldiv)
        spell = []
        for i in spelllist:
            tmp = []
            tmp.append(re.search(r'<span>(.*?)</span>', i).group(1))
            tmp.append(re.search(r'<b>(.*?)</b>', i).group(1))
            spell.append(tmp)


        trans_left = str(dict_output[0].find_all(class_ = 'dictionary-comment')[0]).replace('&amp;', ' &')
        means = []
        for i in re.findall(r'<p>(.*?)</p>', trans_left):
            tmp = []
            character = re.search(r'<b>(.*?)</b>', i).group(1)
            tmp.append(character)
            for j in re.findall(r'<span>(.*?)</span>', i):
                tmp.append(j)
            means.append(tmp)


        dict_result = {}
        dict_result['word'] = the_word
        dict_result['spell'] = spell
        dict_result['means'] = means
        return dict_result

 
    def requestor_page(self, word): # return a html
        url = translator_baidu_urlhost + word
        

        locator = (By.CLASS_NAME, 'strong')

        return self.requestor(url = url, locator = locator, seconds_wait = 5, frequency_seconds = 0.5)


    def requestor(self, url, locator, seconds_wait, frequency_seconds): # return a html
        opener = webdriver.Chrome(chrome_options = chrome_options)
        opener.get(url)
        
        #logging.debug('url: %s'%url)

        #print(opener.page_source)
        self.webdriverwait_all_elements(opener, seconds_wait, frequency_seconds, locator)
        #WebDriverWait(opener, 20, 0.5).until(EC.presence_of_all_elements_located(locator))
        
        html = opener.page_source
            
        opener.close()
        opener.quit()

        return html


    def webdriverwait_all_elements(self, opener, seconds_wait, frequency_seconds, locator):
        WebDriverWait( opener, seconds_wait, frequency_seconds ).until( EC.presence_of_all_elements_located(locator) )



         
        
if __name__ == '__main__':
    print('start')
    baiduTranslator().translateWord('fuck')
    print('end')
