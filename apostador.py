from selenium import webdriver
from time import sleep

driver = webdriver.Chrome(r'C:\Users\User\Downloads\chromedriver.exe')
driver.get('https://blaze.com/pt/games/double?modal=auth&tab=login')

# Login
driver.find_element_by_name('username').send_keys('minuano95@gmail.com')
driver.find_element_by_name('password').send_keys('Minuano95')
driver.find_element_by_css_selector('#auth-modal > div.body > form > div.input-footer > button').click()

# Apostar Primeira tentativa
sleep(2)
driver.find_element_by_css_selector(
    '#roulette-controller > div.body > div.inputs-wrapper > div.bet-input-row > div > div.input-field-wrapper > input').send_keys(2)

# Apostar primeira gale


# Apostar segunda gale


sleep(30)
driver.close()
