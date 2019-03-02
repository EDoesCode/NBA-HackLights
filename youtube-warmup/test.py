from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
import json
import time
import os.path as path

options = Options()
#options.headless = True
driver = webdriver.Firefox(options=options)
driver.get('http://google.com/')

if path.isfile('my_json.txt'):
    with open('my_json.txt') as fp:
        h = json.load(fp)
        for i in h:
            driver.add_cookie(i)

driver.find_element_by_name("q").send_keys("Youtube")
driver.execute_script("arguments[0].click();", driver.find_element_by_name("btnK"))
print('Headless Firefox Initialized')
c = driver.get_cookies()
time.sleep(2)
with open('my_json.txt', 'w') as fp:
    json.dump(c, fp)

results = driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[1]/a/h3")
results.click()
#site = driver.find_element_by_xpath('//*[@id="search"]')
#site.click()
wait = Wait(driver, 10)
#search = driver.find_element_by_xpath("/html/body")
#search.click()
driver.implicitly_wait(2)
youtube_search = driver.find_element_by_xpath('//*[@id="container"]')
driver.execute_script("arguments[0].scrollIntoView();", youtube_search)
driver.implicitly_wait(2)
AC(driver).move_to_element(youtube_search)
driver.implicitly_wait(2)
AC(driver).click()
driver.implicitly_wait(2)
AC(driver).perform()
youtube_search.click()
time.sleep(2)
#youtube_search.send_keys("Never Gonna Give You Up")
AC(driver).send_keys("Never Gonna Give You Up" + Keys.RETURN).perform()
time.sleep(2)
vid = driver.find_element_by_css_selector('ytd-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > ytd-thumbnail:nth-child(1) > a:nth-child(1) > yt-img-shadow:nth-child(1) > img:nth-child(1)')
driver.implicitly_wait(10)
driver.execute_script("arguments[0].scrollIntoView();", vid)
driver.implicitly_wait(10)
AC(driver).move_to_element(vid).perform()
AC(driver).click()
driver.implicitly_wait(2)
AC(driver).perform()
time.sleep(2)
vid.click()

print("The Video is playing")
time.sleep(100)
driver.quit()