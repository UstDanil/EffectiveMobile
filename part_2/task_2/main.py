import os
import time
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from service import save_data_from_link

load_dotenv()


def get_webdriver():
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


if __name__ == "__main__":
    driver = get_webdriver()
    driver.get(os.getenv('SPIMEX_URL'))
    time.sleep(1)
    try:
        user_agreement = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, '//input[@value="Согласен"]')))
        driver.execute_script("arguments[0].scrollIntoView(true);", user_agreement)
        driver.execute_script("arguments[0].click();", user_agreement)
    except TimeoutException:
        pass

    date_break_flag = False
    while not date_break_flag:
        file_links = driver.find_elements(
            By.XPATH, "//a[contains(@href,'/upload/reports/oil_xls/')]")
        for file_link in file_links:
            href_from_link = file_link.get_attribute('href')
            if '2022' in href_from_link:
                date_break_flag = True
                break
            save_data_from_link(href_from_link)
        next_page_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(),'Вперед')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", next_page_btn)
        driver.execute_script("arguments[0].click();", next_page_btn)
        time.sleep(1)
