from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from login_credentials import email_id, password
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import re

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


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


def get_name():
    name_span_element = driver.find_element(
        by=By.CSS_SELECTOR,
        value="div.gs > div.gE.iv.gt > table > tbody > tr:nth-child(1) > td.gF.gK > table > tbody > tr > td > h3 > span > span.gD > span",
    )
    name = name_span_element.text
    return name


def process_name(name):
    processed_name = ""
    just_saw_comma = False
    for alphabet in name:
        if alphabet == " " and just_saw_comma == True:
            just_saw_comma == False
            processed_name = ""
            continue
        if alphabet == " ":
            return processed_name
        if alphabet == ",":
            just_saw_comma = True
            processed_name = ""
        processed_name += alphabet
    return processed_name


def process_email_body():
    text_content_div = driver.find_element(
        by=By.CSS_SELECTOR, value="div.gs > div:nth-child(3)"
    )
    div_innerhtml = text_content_div.get_attribute("innerHTML")
    soup = BeautifulSoup(div_innerhtml, "html.parser")
    raw_text = soup.get_text().lower()
    print(raw_text)
    return raw_text


def process_text(raw_text):
    # Tokenize the text
    text = raw_text
    tokens = word_tokenize(text)

    # Perform POS tagging
    tagged_tokens = pos_tag(tokens)

    # Define pattern for tech stack keywords
    tech_stack_patterns = [
        "c++",
        "java",
        "python",
        "django",
        "react",
        "angular",
        "sql",
        "nosql",
        "javascript",
        "express",
        "flask",
        "nodejs",
    ]

    # Match tech stack keywords and extract relevant information
    tech_stack = [token for token, _ in tagged_tokens if token in tech_stack_patterns]
    # find years of experience tags
    experience_pattern = r"\b(\d+)\s*\+?\s*(?:years|y(?:rs)?|y)\b"
    years_of_experience = re.findall(experience_pattern, text)
    print("Tech Stack:", tech_stack)
    print("Years of Experience:", years_of_experience)

    return [tech_stack, years_of_experience]


def analyse_mail():
    name = get_name()
    processed_name = process_name(name)
    print(processed_name)
    raw_text = process_email_body()
    tech_stack, years_of_experience = process_text(raw_text)


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
        analyse_mail()
        time.sleep(3)
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
    time.sleep(3)
    manage_mails()


manage_mails()
driver.quit()
