import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# connect to server
driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.get('https://mail.ru')
login = driver.find_element_by_id('mailbox:login-input')
login.send_keys('study.ai_172@mail.ru')
button = driver.find_element_by_id('mailbox:submit-button')
button.click()
password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mailbox:password-input'))
        )
password.send_keys('NextPassword172')
password.send_keys(Keys.ENTER)

# find first letter
first_letter = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-letter-list-item'))
        )
driver.get(first_letter.get_attribute('href'))

# find other letters
al_letters = []
while True:
    time.sleep(2)
    letter_info = {}
    date = driver.find_element_by_class_name('letter__date')
#        WebDriverWait(driver, 10).until(
#            EC.presence_of_element_located((By.CLASS_NAME, 'letter__date'))
#        )
    letter_info['date'] = date.text
    contact = driver.find_element_by_class_name('letter-contact')
#        WebDriverWait(driver, 10).until(
#            EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))
#        )
    letter_info['contact'] = contact.get_attribute('title')
    title = driver.find_element_by_xpath('.//h2')
#        WebDriverWait(driver, 10).until(
#            EC.presence_of_element_located((By.XPATH, './/h2'))
#        )
    letter_info['title'] = title.text
    body = driver.find_element_by_class_name('letter-body')
#        WebDriverWait(driver, 10).until(
#            EC.presence_of_element_located((By.CLASS_NAME, 'letter-body'))
#        )
    letter_info['body'] = body.text
    al_letters.append(letter_info)
    try:
        next_letter = driver.find_element_by_class_name('portal-menu-element_next')
        i = i + 1
        next_letter.click()
    except Exception as e:
        print(e)
        break

client = MongoClient('127.0.0.1', 27017)
db = client['letters']
letter_mail = db.mail
letter_mail.insert_many(al_letters)
