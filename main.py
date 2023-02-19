from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import pandas as pd
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import date, datetime
import json
# import progressbar

load_dotenv()



USERNAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
PROFILE_URL = os.getenv('PROFILE_URL')
links_list = []
Scraping_data_array = []


chromedriver = Service(ChromeDriverManager().install())

# chromeOptions = webdriver.ChromeOptions()
chromeOptions = uc.ChromeOptions()

prefs = {
    "safebrowsing.enabled": True,
    "profile.default_content_setting_values.notifications": 2,
    "credentials_enable_service": False,
     "profile.password_manager_enabled": False
}
chromeOptions.add_experimental_option("prefs", prefs)
# chromeOptions.add_argument("--headless")
# chromeOptions.add_argument('--no-sandbox')
# chromeOptions.add_argument('--incognito')
# chromeOptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
chromeOptions.add_argument('--disable-save-password-bubble')
chromeOptions.add_argument("--disable-popup-blocking")
chromeOptions.add_argument("--disable-web-security")
chromeOptions.add_argument("--disable-dev-shm-usage")
chromeOptions.add_argument("--disable-gpu")
chromeOptions.add_argument("--no-first-run")
chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
chromeOptions.add_argument('--disable-infobars')
chromeOptions.add_argument('--disable-notifications')
chromeOptions.add_argument('--ignore-certificate-errors')
chromeOptions.add_argument('--mute-audio')
chromeOptions.add_argument('--no-sandbox')
chromeOptions.add_argument('--start-maximized')
chromeOptions.add_argument('--disable-extensions')
chromeOptions.add_argument('--disable-gpu')
chromeOptions.add_argument('--disable-default-apps')
chromeOptions.add_argument('--disable-translate')
chromeOptions.add_argument('--disable-logging')
chromeOptions.add_argument('--no-first-run')
chromeOptions.add_argument('--log-level=3')
chromeOptions.add_argument('--remote-debugging-port=0')
chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
chromeOptions.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=chromedriver, options=chromeOptions)
# driver = uc.Chrome(options=chromeOptions)
driver.maximize_window()
action = ActionChains(driver)

logging.info('Process Started...')



driver.get("https://www.instagram.com/")
time.sleep(5)

username = driver.find_element("name", "username")
password = driver.find_element("name", "password")

username.send_keys(USERNAME)
password.send_keys(PASSWORD)

login_btn = driver.find_element(
    By.XPATH, "//div[contains(text(),'Log in')]")

login_btn.click()

time.sleep(10)

driver.get(PROFILE_URL)
following_btn = WebDriverWait(driver, 35).until(EC.presence_of_element_located(
    (By.XPATH, "//div[contains(text(),'following')]")))
driver.execute_script("arguments[0].click();", following_btn)
time.sleep(15)

count = 0
while True:
    try:
        count += 1
        see_more = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._aanq")))    
        driver.execute_script("arguments[0].scrollIntoView();", see_more)
        time.sleep(10)
        if count == 1:
            break
        continue
    except:
        print("No see more")
        break
    
time.sleep(15)
listoflinks = driver.find_elements(By.XPATH, "//a/span/div")

for index,links in enumerate(listoflinks):
    print('p_url',links.text)
    p_username_text = links.text.split("\n")[0]
    links_list.append(f'https://www.instagram.com/{p_username_text}/')

    
print('links_list',links_list)

for index, v_link in enumerate(links_list):
    time.sleep(5)
    driver.get(v_link)
    time.sleep(10)
    try:
        v_profile_username = driver.find_element(By.XPATH, "//h2").text
    except:
        v_profile_username = ''
    try:
        v_profile_name = driver.find_element(By.XPATH, '//div[@class="_aa_c"]/span').text
    except:
        v_profile_name = ''
    try:
        v_profile_company = driver.find_element(By.XPATH, '//div[@class="_aa_c"]/div/div').text
    except:
        v_profile_company = ''
    try:
        v_profile_discrption = driver.find_element(By.XPATH, '//div[@class="_aa_c"]/h1').text
    except:
        v_profile_discrption = ''
    try:
        try:
            v_profile_img = driver.find_element(By.XPATH, "//div[@class='_aarf']//span/img").get_attribute("src")
        except:
            v_profile_img = driver.find_element(By.XPATH, "//div[@class='_aarf _aarg']//span/img").get_attribute("src")
    except:
        v_profile_img = ''
    Scraping_data_array.append(
                            {"v_profile_username": v_profile_username, 
                             "Url": v_link, 
                             "v_profile_name": v_profile_name, 
                             "v_profile_company": v_profile_company, 
                             "v_profile_discrption": v_profile_discrption,
                             "img_url": v_profile_img
                             })
output_data_log = 'D:/upwork/Instagram-Automation/output.xlsx'
writer1 = pd.ExcelWriter(
                        output_data_log, engine='xlsxwriter')
df = pd.DataFrame.from_dict(Scraping_data_array)
df.to_excel(writer1, index=False)
writer1.save()
driver.quit()
print("END")