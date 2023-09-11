from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
import pandas as pd
import re

driver = webdriver.Chrome()

# Adjust the path for 'trust' directory to be inside 'work_flow_io'
if not os.path.exists('../work_flow_io/trust'):
    os.makedirs('../work_flow_io/trust')

# Load the workbook from work_flow_io folder
print("here 1")
df = pd.read_excel('../work_flow_io/shopname.xlsx')
print("here2")
urls = df.iloc[:, 0].tolist()  # Assuming URLs are in the first column

# Create a DataFrame to store URLs and corresponding image filenames
image_df = pd.DataFrame(columns=['URL', 'Image_File'])

for idx, url in enumerate(urls):

    shop_name = url.split("https://shop.epwk.com/")[1]
    shop_name = re.sub(r'[\\/:"*?<>|]+', '', shop_name)  # add any other characters that you want to remove
    url += 'about.html'

    driver.get(url)
    time.sleep(2)

    print("Processing URL number: ", idx + 1)

    images = driver.find_elements(By.TAG_NAME, 'img')

    image_found = False
    for image in images:
        img_url = image.get_attribute('src')
        if img_url and img_url.startswith('https://img11.weikeimg.com/licence/'):

            img_url = img_url.split('?')[0]

            response = requests.get(img_url)
            img_data = response.content
            # Adjust the path to save the image inside 'work_flow_io/trust' directory
            filename = f'../work_flow_io/trust/img_{idx + 1}_{shop_name}.png'
            with open(filename, 'wb') as handler:
                handler.write(img_data)

            # Append the URL and filename to the DataFrame
            new_row = pd.DataFrame({'URL': [url], 'Image_File': [filename]})
            image_df = pd.concat([image_df, new_row], ignore_index=True)

            image_found = True
            break

    # If no image was found for this URL, append None as the image file
    if not image_found:
        new_row = pd.DataFrame({'URL': [url], 'Image_File': [None]})
        image_df = pd.concat([image_df, new_row], ignore_index=True)

driver.quit()

# Save the results to the work_flow_io folder
image_df.to_excel('../work_flow_io/image_records.xlsx', index=False)
