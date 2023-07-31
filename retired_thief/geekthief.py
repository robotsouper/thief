from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook
import time

def scroll_to_end(driver):
    old_position = 0
    new_position = None

    while new_position != old_position:
        old_position = driver.execute_script(
            ("return (window.pageYOffset !== undefined) ?"
             " window.pageYOffset : (document.documentElement ||"
             " document.body.parentNode || document.body);"))
        time.sleep(1)
        new_position = driver.execute_script(
            ("return (window.pageYOffset !== undefined) ?"
             " window.pageYOffset : (document.documentElement ||"
             " document.body.parentNode || document.body);"))

def main():
    wb = load_workbook('放假的帅哥.xlsx')
    ws = wb.active

    unique_links = set()


    # Base URL
    base_url = "https://web.okjike.com/topic/5cebe59010f1330017971fd9"

    # Start the WebDriver
    driver = webdriver.Chrome()
    driver.get("https://web.okjike.com/login")
    time.sleep(30)

    driver.get(base_url)

    while True:
        try:
            scroll_to_end(driver)
            users = driver.find_elements(By.XPATH, '//a[starts-with(@href, "/u")]')

            for user in users:
                # wait until the username is loaded
                WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, '.'), '', user))
                username = user.text
                link = 'https://web.okjike.com' + user.get_attribute('href')

                if link not in unique_links:
                    ws.append([username, link])
                    unique_links.add(link)

            wb.save('放假的帅哥1.xlsx')

        except Exception as e:
            print(f'An error occurred: {e}')
            # save last unique link
            print(f'Last unique link: {list(unique_links)[-1] if unique_links else "No links"}')
            wb.save('放假的帅哥1.xlsx')
            break

    driver.quit()

if __name__ == "__main__":
    main()
