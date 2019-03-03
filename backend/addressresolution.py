#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
import json
import time
import sys
import re
import os 
import subprocess

fire_options = webdriver.FirefoxOptions()
fire_options.headless = True
driver = webdriver.Firefox(options = fire_options)
#driver.install_addon(cwd+"/ublock.xpi")
url = sys.argv[1]
name = sys.argv[2]
driver.get(url)

time.sleep(5)

vid = driver.find_element_by_css_selector('.detail_tabs > span:nth-child(1)')
driver.execute_script("arguments[0].scrollIntoView();", vid)
AC(driver).move_to_element(vid)
vid.click()

time.sleep(5)

vid = driver.find_element_by_css_selector('video-thumbnail.small-12:nth-child(2) > div:nth-child(1) > div:nth-child(1) > img:nth-child(1)')
driver.execute_script("arguments[0].scrollIntoView();", vid)
AC(driver).move_to_element(vid)
vid.click()

time.sleep(30)

js = "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"

har = driver.execute_script(js)

driver.quit()

with open("harfile", "w") as harfile:
    harfile.write(json.dumps(har))

st = " "
with open('harfile') as fp:
        h = json.load(fp)
        for i in h:
            if (i["name"]).find("master.m3u8") >= 0:
                st = (i["name"])
                
os.system("ffmpeg -i \""+st+"\" -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 "+name+".mp4")

