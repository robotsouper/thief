import requests
from bs4 import BeautifulSoup
import os


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
    unique_links = list(set(png_links))
    return unique_links


def download_image(image_url, folder):
    response = requests.get(image_url)
    image_name = os.path.split(image_url)[1]
    with open(os.path.join(folder, image_name), 'wb') as file:
        file.write(response.content)


folder = "images"
os.makedirs(folder, exist_ok=True)  # Ensure the folder exists

for page_number in range(54, 225):
    home_url = f"https://talent.epwk.com/wuxian/page{page_number}.html"
    shop_links = get_links_from_homepage(home_url)
    print("Now in page: ", page_number)
    for link in shop_links:
        png_links = get_png_links_from_page(link)
        for png_link in png_links:
            download_image(png_link, folder)
