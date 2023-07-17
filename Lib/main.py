from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import imaplib
from bs4 import BeautifulSoup

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

with open('mail_pass.txt') as f:
    lines_mail = [line.rstrip('\n') for line in f]

with open('wallets.txt') as f:
    lines_wallet = [line.rstrip('\n') for line in f]


def do_work(mail, wallet):
    email = mail.split(':')[0]
    email_password = mail.split(':')[1]
    MNEMONIC = wallet.split(' ')
    PASSWORD = '11111111'
    print(email)
    print(MNEMONIC)

    chrome_options = Options()
    chrome_options.add_extension('MetaMask.crx')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)

    driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/ul/li[2]/button').click() # import
    time.sleep(0.5)
    driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div/button[2]').click() # no thanks
    time.sleep(0.5)
    for i in range(3): driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.TAB) # locate mnemonic box
    for word in MNEMONIC:
        driver.switch_to.active_element.send_keys(word) # input each mnemonic to current textbox
        for i in range(2): driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.TAB) # switch to next textbox
        # time.sleep(0.5)
    time.sleep(0.5)
    driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/button').click() # confirm
    time.sleep(0.5)
    driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input').send_keys(PASSWORD) # enter password
    driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input').send_keys(PASSWORD) # enter password twice
    time.sleep(0.5)
    driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input').click() # I understand
    driver.find_element('xpath', '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button').click() # import my wallet
    driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click() # got it
    driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click() # next page
    driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click() # done
    time.sleep(1)
    driver.find_element('xpath', '/html/body/div[2]/div/div/section/div[2]/div/button/span').click() # close
    driver.find_element('xpath', '//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/div/div/div/button').click()
    meta_window = driver.current_window_handle

    print('import complete')

    driver.switch_to.window(driver.window_handles[0])
    driver.get('https://sl.xter.io/yLsbe4')
    driver.find_element('xpath', '//*[@id="login"]').click()
    driver.find_element('xpath', '//*[@id="global_layout"]/section/div[2]/div/div/div/div[1]/div[5]/span').click()

    driver.find_element('xpath', '//*[@id="global_layout"]/section/div[2]/div/div/div/div[1]/div[1]/div[1]/div/input').send_keys(email)
    driver.find_element('xpath', '//*[@id="global_layout"]/section/div[2]/div/div/div/div[1]/div[2]/div[1]/div/input').send_keys(email_password)
    driver.find_element('xpath', '//*[@id="global_layout"]/section/div[2]/div/div/div/div[1]/div[3]/div[1]/div/input').send_keys(email_password)

    driver.find_element('xpath', '//*[@id="global_layout"]/section/div[2]/div/div/div/div[1]/button').click()
    #нужен код с почты

    time.sleep(20)

    mail = imaplib.IMAP4_SSL('imap.rambler.ru')
    mail.login(email, email_password)
    mail.list()
    mail.select("inbox")

    result, data = mail.search(None, "ALL")

    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]

    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')

    soup = BeautifulSoup(raw_email_string, 'lxml')
    mydivs = soup.find("div", {"class": '3D"code"'})
    clear_mydivs = mydivs.text.strip()
    print(clear_mydivs)

    driver.find_element('xpath', '//*[@id="global_layout"]/section/div[2]/div/div/div/div[1]/div/div[1]/div/input').send_keys(clear_mydivs)
    driver.find_element('xpath', '//*[@id="global_layout"]/section/div[2]/div/div/div/div[1]/button').click()

    time.sleep(4)

    driver.find_element('xpath', '//*[@id="global_layout"]/section/div[2]/div/div/div/div/div[2]').click()
    time.sleep(0.5)
    driver.find_element('xpath', '//*[@id="wallet_connect"]').click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//div[3]/div/section/div/div/div/div/div/div[2]").click()
    time.sleep(4)
    driver.switch_to.window(driver.window_handles[1])
    driver.refresh()
    driver.find_element('xpath', '//*[@id="app-content"]/div/div/div/div[3]/div[2]/button[2]').click()
    time.sleep(0.5)
    driver.find_element('xpath', '//*[@id="app-content"]/div/div/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
    driver.find_element('xpath', '//*[@id="wallet_pair"]').click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    driver.refresh()
    driver.find_element('xpath', '//*[@id="app-content"]/div/div[3]/div/div[4]/footer/button[2]').click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)

for q, w in zip(lines_mail, lines_wallet):
    do_work(q, w)
