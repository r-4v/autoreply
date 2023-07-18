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
exclude_list = [
    "LinkedIn Job Alerts",
    "Google",
    "Dice Job Alert",
    "Your Indeed Job Feed",
    "Stack Overflow",
    "LinkedIn",
    "Indeed",
    "Dice",
    "Your",
]
read_status = {"zF": "Unread", "yP": "Read"}


def google_login():
    driver.get("https://mail.google.com")
    email_id_input_field = driver.find_element(by=By.TAG_NAME, value="input")
    email_id_input_field.send_keys(email_id)
    email_id_input_field.send_keys(Keys.ENTER)
    driver.implicitly_wait(6)
    password_input_field = driver.find_element(by=By.NAME, value="Passwd")
    password_input_field.send_keys(password)
    password_input_field.send_keys(Keys.ENTER)


google_login()
time.sleep(4)


def analyse_mail():
    pass


def compose_mail():
    pass


def reply_to_mail(row, mail_open_status):
    if read_status[mail_open_status] == "Unread":
        row.click()
        driver.implicitly_wait(5)
        back_button_field = driver.find_element(
            by=By.XPATH,
            value="/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div",
        )
        back_button_field.click()
        time.sleep(2)
        return


def get_and_reply_next_unread_mail():
    driver.implicitly_wait(100)
    primary_mails_table = driver.find_element(
        by=By.CSS_SELECTOR,
        value="#\\:22 > tbody",
    )
    rows = primary_mails_table.find_elements(by=By.XPATH, value=".//tr")
    for row in rows:
        sender_span_class = row.find_element(
            by=By.XPATH,
            value=".//td[4]//div[2]//span",
        )
        inner_span_element = sender_span_class.find_element(
            by=By.TAG_NAME, value="span"
        )
        sender_name = inner_span_element.get_attribute("name")
        mail_open_status = inner_span_element.get_attribute("class")
        if (
            read_status[mail_open_status] == "Unread"
            and sender_name not in exclude_list
        ):
            reply_to_mail(row, mail_open_status=mail_open_status)
            return True
    return False


def manage_mails():
    is_there_an_unread_mail = get_and_reply_next_unread_mail()
    print(is_there_an_unread_mail)
    if is_there_an_unread_mail == False:
        return
    manage_mails()


manage_mails()
driver.quit()
