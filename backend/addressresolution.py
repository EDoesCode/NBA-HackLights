#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import sys
import re

fire_options = webdriver.FirefoxOptions()
fire_options.headless = True
driver = webdriver.Firefox(options = fire_options)
url = sys.argv[1]
driver.get(url)

driver.implicitly_wait(5)

vid = driver.find_element_by_xpath('//*[@id="block-league-content"]/game-detail/div[1]/nav/ul/span[1]/li/button')
driver.execute_script("arguments[0].scrollIntoView();", vid)
vid.click()

driver.implicitly_wait(5)

vid = driver.find_element_by_xpath('//*[@id="video-list"]/video-thumbnail[2]/div')
driver.execute_script("arguments[0].scrollIntoView();", vid)
vid.click()

time.sleep(30)

js = "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"

har = str(driver.execute_script(js))

with open("harfile", "w") as harfile:
    harfile.write(json.dumps(har))

har.replace(" ","\n")

#for a in har:
    #if(re.search("[^]master\.m3u8", a)):
    #st = a
    #print(st)


driver.quit()