from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import io
import re
import time
import requests
import os
import pandas as pd
from openpyxl import Workbook

pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'
driver = webdriver.Chrome()

# Create directory for storing images if it doesn't exist
if not os.path.exists('trust'):
    os.makedirs('trust')

# Create a workbook
wb = Workbook()
ws = wb.active

df = pd.read_excel('shopname.xlsx')
urls = df.iloc[:, 0].tolist()  # Assuming URLs are in the first column
urls = urls[:2]

for idx, url in enumerate(urls):
    # Append "about.html" to the URL
    url += 'about.html'

    # Visit the page
    driver.get(url)
    time.sleep(5)  # Allow time for JavaScript to load and execute

    # Check for images
    images = driver.find_elements(By.TAG_NAME, 'img')
    for image in images:
        img_url = image.get_attribute('src')
        if img_url and img_url.startswith('https://img11.weikeimg.com/licence/'):
            print("We get the item! Let's leave!")

            img_url = img_url.split('?')[0]

            response = requests.get(img_url)
            img_data = response.content
            with open(f'trust/img_{idx}.png', 'wb') as handler:
                handler.write(img_data)


            img = Image.open(io.BytesIO(img_data))

            text = pytesseract.image_to_string(img, lang='chi_sim+eng', config='--psm 6')
            print(text)
            pattern = r'([A-Z0-9]{18})'
            match = re.search(pattern, text, re.MULTILINE)
# ...

            if match:
                print("18-digit string found: ", match.group())

                # Write the URL and the 18-digit string to the Excel file
                ws.append([url, match.group()])

            else:
                print("18-digit string not found.")

            break

# Save the workbook
wb.save("results.xlsx")

driver.quit()
