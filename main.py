from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json

chrome_driver_path = "chromedriver.exe"

chrome_options = Options()

chrome_options.add_argument(r"--user-data-dir=C:\Users\Mohammad\AppData\Local\Google\Chrome\User Data")

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:

    hrefs = []

    driver.get("https://divar.ir/s/tehran/vehicles")

    wait = WebDriverWait(driver, 10)
    while True:
        starting_div = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-id='virtuoso-item-list']")))

        divs = starting_div.find_elements(By.XPATH, ".//div")

        for div in divs:
            try:
                links = starting_div.find_elements(By.XPATH, ".//div//a")

                hrefs.extend(driver.execute_script(
                    "return Array.from(arguments[0]).map(link => link.href);",
                    links
                ))

            except Exception as e:
                print(e)
                continue

        driver.execute_script("window.scrollBy(0, 700);")
        time.sleep(0.01)

        new_scroll_height = driver.execute_script("return document.body.scrollHeight")
        if new_scroll_height <= driver.execute_script("return window.scrollY + window.innerHeight"):
            break

    json_file_name = "links.json"

    with open(json_file_name, "w", encoding="utf-8") as json_file:
        json.dump(hrefs, json_file, ensure_ascii=False, indent=4)

    # file_name = "links.txt"
    #
    # with open(file_name, "w", encoding="utf-8") as file:
    #
    #     for href in hrefs:
    #         file.write(href + "\n")

    time.sleep(10)

except Exception as e:
    print(e)

finally:
    driver.quit()
