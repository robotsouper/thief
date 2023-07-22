import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

from thief.util import process_file


def get_shop_name(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    shop_name_element = soup.find('li', class_='shopname')
    if shop_name_element:
        return shop_name_element.get('title')
    return None


def get_links_from_homepage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=True)
             if link.get('href').startswith('https://shop.epwk.com')]
    return list(set(links))


def main():
    file_name = '总1.xlsx'

    # Check if the file exists. If it does, load the data into a DataFrame. Otherwise, create a new DataFrame.
    if os.path.exists(file_name):
        df = pd.read_excel(file_name)
    else:
        df = pd.DataFrame(columns=['URL', 'Shop Name'])

    for page_number in range(150, 225):
        home_url = f"https://talent.epwk.com/wuxian/page{page_number}.html"
        print("Now getting into page: ", page_number)
        links = get_links_from_homepage(home_url)
        for link in links:
            shop_name = get_shop_name(link)
            new_df = pd.DataFrame({'URL': [link], 'Shop Name': [shop_name]})
            df = pd.concat([df, new_df], ignore_index=True)
            print(f"Processed shop: {shop_name} at {link}")

    # Save the DataFrame
    df.to_excel(file_name, index=False)


if __name__ == '__main__':
    main()
    process_file("总1.xlsx")
