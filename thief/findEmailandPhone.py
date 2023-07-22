import pandas as pd
import time
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wb = load_workbook('combined_creditlist.xlsx')
ws = wb.active

url_email_phone = {}

driver = webdriver.Chrome()
count = 1
for row in ws.iter_rows(min_row=2, max_row=675, values_only=True):
    print("Now in row: ", count)
    count += 1
    url = row[1]
    if url != "无":
        driver.get(url)
        time.sleep(1)

        try:
            # Find the email address
            email_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".index_detail-email__B_1Tq")))
            email = email_element.text if email_element else '无'

            # Find the phone number
            phone_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".index_detail-tel__fgpsE")))
            phone = phone_element.text if phone_element else '无'

            url_email_phone[url] = [email, phone]

        except Exception as e:
            print(f"An error occurred: {e}")
            url_email_phone[url] = ['无', '无']

driver.quit()

# Create a new DataFrame with the URLs, email addresses, and phone numbers
df_contacts = pd.DataFrame.from_dict(url_email_phone, orient='index', columns=['Email', 'Phone'])

# Write the DataFrame to an Excel file
df_contacts.reset_index().rename(columns={'index': 'URL'}).to_excel("company_contacts.xlsx", index=False)
