from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random

class Scraper:
    def __init__(self, start_url):
        self.driver = webdriver.Chrome()
        self.start_url = start_url
        self.data = []

    def get_links_from_homepage(self):
        self.driver.get(self.start_url)
        elements = self.driver.find_elements(By.XPATH, '//a[starts-with(@href, "https://shop.epwk.com")]')
        return [el.get_attribute('href') for el in elements]

    def scrape_about_page(self, url):
        self.driver.get(url + '/about.html')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'information')))
        labels = ['手机', '邮箱', 'QQ', '微信']
        data = {}
        for label in labels:
            try:
                value = self.driver.find_element(By.XPATH, f'//li[contains(text(), "{label}：")]').text.replace(f'{label}：', '')
                data[label] = value
            except Exception:
                pass
        return data

    def run(self):
        urls = self.get_links_from_homepage()
        for url in urls:
            data = self.scrape_about_page(url)
            if data:
                self.data.append(data)
            time.sleep(abs(random.gauss(2, 0.5)))

        df = pd.DataFrame(self.data)
        df.to_excel('data.xlsx', index=False)

if __name__ == "__main__":
    start_url = "https://talent.epwk.com/wuxian/"
    scraper = Scraper(start_url)
    scraper.run()
