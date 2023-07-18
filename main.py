from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from env_var import email_id, password
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument("--disable-plugins-discovery")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("user_agent=DN")

driver = uc.Chrome(options=chrome_options)
driver.delete_all_cookies()


def googleLogin():
    driver.get("https://mail.google.com")
    email_id_input_field = driver.find_element(by=By.TAG_NAME, value="input")
    email_id_input_field.send_keys(email_id)
    email_id_input_field.send_keys(Keys.ENTER)
    time.sleep(2)
    password_input_field = driver.find_element(by=By.NAME, value="Passwd")
    time.sleep(2)
    password_input_field.send_keys(password)
    password_input_field.send_keys(Keys.ENTER)


googleLogin()
time.sleep(600)


def manageMails():
    pass


driver.quit()
