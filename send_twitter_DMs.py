from audioop import add
from email import message
from pickle import FALSE
from select import select
import time
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import db_actions
db = db_actions
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://twitter.com/messages/compose")
# create action chain object
action = ActionChains(driver)
def login(file = "twitter_Send/the_gitonga.csv"):
    try:
        from csv import DictReader
        with open(file, encoding= 'utf-8-sig') as f:
            dict_reader = DictReader(f)
            list_of_dicts = list(dict_reader)
        for i in list_of_dicts:
            driver.add_cookie(i)
    except Exception as error:
        print(error)
    finally:
        driver.refresh()
        if (driver.current_url != "https://twitter.com/messages/compose"): driver.get("https://twitter.com/messages/compose")

login()
def get_contacts():
    return db.select("target_pool", "username")
def add_contacts():
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,"//input[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-xyw6el r-13rk5gd r-1dz5y72 r-fdjqy7 r-13qz1uu']")))
        contacts = get_contacts()
        index = 0
        for contact in contacts:
            try: 
                search_box = driver.find_element(By.XPATH, "//input[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-xyw6el r-13rk5gd r-1dz5y72 r-fdjqy7 r-13qz1uu']")
                search_box.send_keys(Keys.CONTROL+"a")
                search_box.send_keys(Keys.DELETE)
                search_box.send_keys("@"+contact[0])
                #WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-1dbjc4n r-172uzmj r-1pi2tsx r-1ny4l3l r-13qz1uu']")))
                time.sleep(5)
                search_box.send_keys(Keys.ARROW_DOWN)
                search_box.send_keys(Keys.ENTER)
                index +=1
            finally:
                update_db(contact[0])
                send_message(message,contact[0])
                if index >= 100: break
                else: continue
    except Exception as error:
        print(error)
    #finally:
        #driver.quit()
def send_message(message,name):
    try:
        next = driver.find_element(By.XPATH, "//div[@class='css-18t94o4 css-1dbjc4n r-42olwf r-sdzlij r-1phboty r-rs99b7 r-19u6a5r r-15ysp7h r-4wgw6l r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr']").click()
        time.sleep(5)#wait for next page to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-1dbjc4n r-xoduu5 r-xyw6el r-oyd9sg r-13qz1uu']")))
        message_box = driver.find_element(By.XPATH, "//div[@class='css-1dbjc4n r-xoduu5 r-xyw6el r-oyd9sg r-13qz1uu']")
        message_box.click()
        for paragraph in message:
            if paragraph == message[0]: paragraph = "@" + name + ", "+ paragraph
            action.send_keys(paragraph).perform()
            action.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

        action. send_keys(Keys.ENTER)
        action.perform()
        time.sleep(2)
    except Exception as error:
        print(error)
    finally:
            if (driver.current_url != "https://twitter.com/messages/compose"): driver.get("https://twitter.com/messages/compose")
            time.sleep(5)
def update_db(username):
    username = "'"+ username + "'"
    try:
        mysql, cursor = db.connect()
        sql = "UPDATE target_pool SET contacted = 'DONE' WHERE username = {}".format(username)
        cursor.execute(sql)
        mysql.commit()
    except Exception as error:
        print(error)
message = ["I Need Your Advice.","I noticed that you are a university student: congrats BTW","Are you tired of never-ending, challenging assignments that don’t make sense? You are not alone: in this season of online classes, information seems to get in one ear and out another.","The solution to this is to hire a writer. I write professionally for both students and bloggers. I guarantee below 10 percent on Turnitin for each task. Furthermore, I will write your task with 24hrs.","The best part is that I will let you choose your price according to your budget.","I needed advice on whether you think it is a good idea for us to chat (here in this DM) to negotiate."]
add_contacts()
time.sleep(60)
