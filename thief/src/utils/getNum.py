import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'


def extract_numbers(img_path):
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    pattern = re.compile(r'(\d{11}|\d{3}-\d{4}-\d{4})')
    matches = pattern.findall(text)

    return matches


def get_links_from_homepage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=True)
             if link.get('href').startswith('https://shop.epwk.com')]
    unique_links = list(set(links))

    return unique_links


def get_png_links_from_page(url):
    url = url.rstrip('/') + '/records.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    png_links = [img.get('src') for img in soup.find_all('img', src=True)
                 if img.get('src').startswith('https://img11.weikeimg.com/data/uploads')]
    unique_links = list(set(png_links))  # Convert to set to remove duplicates, then convert back to list

    return unique_links


def download_image(image_url, folder):
    response = requests.get(image_url)
    image_name = os.path.split(image_url)[1]  # Get the last part of the url (like 'example.png')
    image_path = os.path.join(folder, image_name)
    with open(image_path, 'wb') as file:  # Open the file in write-binary mode
        file.write(response.content)

    return image_path


def main():
    results = {}
    folder = "images"
    os.makedirs(folder, exist_ok=True)
    file_name = '电话.xlsx'

    # Check if the file exists. If it does, load the data into a DataFrame. Otherwise, create a new DataFrame.
    if os.path.exists(file_name):
        df = pd.read_excel(file_name)
    else:
        df = pd.DataFrame(columns=['URL', 'Number'])

    for page_number in range(50, 80):
        home_url = f"https://talent.epwk.com/wuxian/page{page_number}.html"
        shop_links = get_links_from_homepage(home_url)
        print("Now in page: ", page_number)
        for link in shop_links:
            png_links = get_png_links_from_page(link)
            for png_link in png_links:
                image_path = download_image(png_link, folder)
                numbers = extract_numbers(image_path)
                if numbers:
                    url_without_records = link.replace('/records.html', '')
                    results[url_without_records] = ",".join(numbers)

    # Convert dictionary to DataFrame and append to the existing DataFrame
    new_data = pd.DataFrame(list(results.items()), columns=['URL', 'Number'])
    df = df.append(new_data, ignore_index=True)
    df.to_excel(file_name, engine='openpyxl', index=False)


if __name__ == '__main__':
    main()
