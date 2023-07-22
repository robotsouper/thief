import pandas as pd
import time
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse

wb = load_workbook('shopname.xlsx')
ws = wb.active

# Initialize dictionary to hold company names and their URLs
company_info = {}

# Base URL
base_url = "https://www.tianyancha.com/search?key="

# Start the WebDriver
driver = webdriver.Chrome()

for row in ws.iter_rows(min_row=2, max_row=2765, min_col=2, max_col=2):
    name = row[0].value
    if name:
        driver.get(base_url + urllib.parse.quote(name))
        time.sleep(3)

        try:
            # Find the first search result link
            search_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".index_alink__zcia5.link-click")))
            company_url = search_result.get_attribute('href')
            company_name = search_result.text

            if company_url and name == company_name:
                company_info[name] = company_url
            else:
                company_info[name] = '无'

        except Exception as e:
            print(f"An error occurred: {e}")
            company_info[name] = '无'

driver.quit()

# Create a new DataFrame with the company names and URLs
df_urls = pd.DataFrame(list(company_info.items()), columns=['CompanyName', 'CompanyURL'])

# Write the DataFrame to an Excel file
df_urls.to_excel("company_urls(exact).xlsx", index=False)
