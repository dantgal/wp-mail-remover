# -*- coding: utf-8 -*-

import re
import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

wp_login = raw_input('WP.PL login do poczty: ')
wp_pass = raw_input('WP.PL hasło do poczty: ')
# wp_login = ""
# wp_pass = ""

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 50)
driver.get("https://profil.wp.pl/login/login.html")

inputBoxLogin = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='login']")))
inputBoxLogin.send_keys(wp_login)

inputBoxPasswd = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']")))
inputBoxPasswd.send_keys(wp_pass)

loginButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Zaloguj się')]")))
loginButton.click()

time.sleep(3)

leftMessages = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='folder-1']//div[3]")))
leftMessagesCountStr = driver.find_element_by_xpath("//div[@id='folder-1']//div[3]").text
leftMessagesCount = int(re.search(r"\d+$", leftMessagesCountStr).group())

while leftMessagesCount > 0:

    selectAllButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//nh-checkbox[@aria-label='Zaznacz wiadomości']//div[@role='button']")))
    selectAllButton.click()

    deleteMessages = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='topActionBar-left flex grow-1 shrink-0']//button[@type='button'][contains(text(),'usuń')]")))
    deleteMessages.click()

    time.sleep(3)

    leftMessages = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='folder-1']//div[3]")))
    leftMessagesCountStr = driver.find_element_by_xpath("//div[@id='folder-1']//div[3]").text
    leftMessagesCount = int(re.search(r"\d+$", leftMessagesCountStr).group())

    if leftMessagesCount == 0:
        break

time.sleep(3)

try:
    driver.find_element_by_xpath("//span[@role='button']")
    flushSpam = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@role='button']")))
    flushSpam.click()
    flushSpamConfirm = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "Button--cta")))
    flushSpamConfirm.click()
except NoSuchElementException:
    print("Kosz był pusty")

try:
    driver.find_element_by_xpath("//span[contains(text(),'usuń')]")
    flushSpam = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'usuń')]")))
    flushSpam.click()
    flushSpamConfirm = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "Button--cta")))
    flushSpamConfirm.click()
except NoSuchElementException:
    print("Spam był pusty")

driver.close()
