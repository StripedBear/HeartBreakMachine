import random
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


options = Options()
# prefs = {"profile.managed_default_content_settings.images": 2}
# options.add_experimental_option("prefs", prefs)
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('user-data-dir=browser_data')
options.add_argument("--headless")
options.add_argument("window-size=1800x900")
options.add_argument('--profile-directory=Profile_1')
options.add_argument("--disable-blink-features=AutomationControlled")
s = Service('action_part/driver/chromedriver')
browser = webdriver.Chrome(service=s, options=options)


def check():
    browser.get("https://grustnogram.ru/dashboard/")
    time.sleep(2)
    return browser.current_url


def auth(username, password):
    try:
        browser.execute("get", {'url': 'https://grustnogram.ru/login'})
        username_input = browser.find_element(By.XPATH,
                                              '/html/body/div[1]/div/div/div/section/'
                                              'div/div/div/div[1]/form/div[2]/div/input')
        username_input.clear()
        username_input.send_keys(username)
        password_input = browser.find_element(By.XPATH,
                                              '/html/body/div[1]/div/div/div/section/'
                                              'div/div/div/div[1]/form/div[3]/div/input')
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)
        browser.execute("get", {'url': 'https://grustnogram.ru/'})
        if browser.current_url == 'https://grustnogram.ru/dashboard/':
            return 'ok'
        else:
            return 'not ok'
    except Exception as e:
        print(f'WOW!, {e}')


def prs_posts_kw(target):
    posts = []
    try:
        browser.get(f'https://grustnogram.ru/search/keyword?q={target}')
        time.sleep(10)
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)
        hrefs = browser.find_elements(By.CLASS_NAME, "publish-card__picture-link")
        [posts.append(item.get_attribute('href').replace('https://grustnogram.ru/p/', '')) for item in hrefs]
    except Exception as e:
        return e
    return posts


def subscriber_by_base(target):
    try:
        browser.get(f'https://grustnogram.ru/u/{target}')
        time.sleep(1)
        browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/section/"
                                        "div/div/div/div[1]/div[3]/button[2]").click()
        return target
    except Exception as e:
        return f"\r{e}"


def liking(item):
    try:
        browser.get(f"https://grustnogram.ru/p/{item}")
        time.sleep(5)
        browser.find_elements(By.CLASS_NAME, 'action-btn')[2].click()
    except Exception as e:
        return e


def parsing_followers(target):
    followers = []
    browser.get(f'https://grustnogram.ru/u/{target}')
    time.sleep(5)
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/section/'
                                    'div/div/div/div[1]/div[4]/div/div[3]/div').click()
    time.sleep(random.randint(3, 6))
    scroll = browser.find_element(By.CLASS_NAME, "el-dialog__body")
    try:
        while browser.find_element(By.CSS_SELECTOR,
                                 '#site > div.site__main > section > div > div > div > '
                                 'div.profile-card.feed__profile-card > div.profile-card__info > '
                                'div.el-dialog__wrapper.modal-user-list > div > div.el-dialog__body > '
                                 'div > div.infinite-loading-container'):
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)
    except Exception as e:
        pass
    finally:
        hrefs = browser.find_elements(By.CLASS_NAME, "events-card__login")
        for href in hrefs:
            followers.append(href.get_attribute('href').replace('https://grustnogram.ru/u/', ''))
    return followers


def parsing_likers(target):
    likers = []
    browser.get(f'https://grustnogram.ru/p/{target}')
    time.sleep(6)
    try:
        first_liker = browser.find_element(By.XPATH,
                                           '/html/body/div[1]/div/div/div/div[1]/'
                                           'section/div/div/div/div/article/div[4]/div/a').get_attribute('href')
        likers.append(first_liker.replace('https://grustnogram.ru/u/', ''))
        browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/"
                                       "section/div/div/div/div/article/div[4]/div/span").click()
        time.sleep(5)
        scroll = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/'
                                                'section/div/div/div/div/div/div/div[2]')
        try:
            while True:
                browser.find_element(By.CLASS_NAME, 'infinite-loading-container')
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)
        except Exception as e:
            pass
        finally:
            hrefs = browser.find_elements(By.CLASS_NAME, "events-card__login")
            for href in hrefs:
                likers.append(href.get_attribute('href').replace('https://grustnogram.ru/u/', ''))
    except Exception as e:
            return e
    return likers


def program_end():
    browser.close()
    browser.quit()
