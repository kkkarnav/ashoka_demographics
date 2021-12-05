from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import os
from dotenv import load_dotenv
from time import sleep
import json


def setup():
    load_dotenv()
    # needs a geckodriver.exe in the same folder as a script,
    # as well as a firefox exe in the specified location
    options = Options()
    options.binary_location = (
        "C:\\Users\\KARNAV\\AppData\\Local\\Firefox Developer Edition\\firefox.exe"
    )

    driver_object = webdriver.Firefox(options=options)
    driver_object.implicitly_wait(0.5)

    # for convenience, runs fine in headless too
    driver_object.maximize_window()
    return driver_object


# engine function to submit text to an input field
def fill_text(driver, findby_criteria, find_parameter, fill_parameter):
    text_area = driver.find_element(findby_criteria, find_parameter)
    text_area.send_keys(fill_parameter)
    text_area.send_keys(Keys.RETURN)
    sleep(2)


# logs into the ashoka website with your email and password
def get_past_login(driver, USERNAME, PASSWORD):
    fill_text(driver, By.ID, "identifierId", USERNAME)
    fill_text(driver, By.NAME, "password", PASSWORD)
    sleep(10)


# starting from the home page, locates the specified menu and submenu and clicks on it
def navigate_to_page(driver, menu_number, submenu_name):
    link = driver.find_elements(By.CLASS_NAME, "dropdown-toggle")[menu_number]

    open_menu = ActionChains(driver)
    open_menu.move_to_element(link).perform()

    click_submenu = wait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, submenu_name))
    )
    click_submenu.click()
    sleep(2)


# intended for the Major Minor Report page
# this function is prone to failing because the page arbitrarily async loads
# clicks the get button, then switches pagesize to all to get all the data
def grab_data(driver):
    get_button = driver.find_element(By.CLASS_NAME, "blue")
    click_get = wait(driver, 10).until(EC.element_to_be_clickable(get_button))
    click_get.click()

    select = Select(driver.find_element(By.CLASS_NAME, "pagesize"))
    click_select = wait(driver, 30).until(
        EC.element_to_be_clickable((By.TAG_NAME, "option"))
    )
    sleep(5)
    select.select_by_index(5)

    sleep(1)
    return driver.page_source


def scrape(driver):

    driver.get("https://ams.ashoka.edu.in/")

    USERNAME = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')
    get_past_login(driver, USERNAME, PASSWORD)

    navigate_to_page(driver, 8, "Major Minor Report")

    html_data = grab_data(driver)

    html_data = html_data.split(
        "TableAdvanceSearch pagerDisabled tablesorter tablesorter-bootstrap "
        "table table-bordered table-striped hasFilters"
    )[1]
    html_data = html_data.split("1 - 7283 / 7283 (7283)")[0]
    html_data = html_data.split("tbody")[1]

    with open("./new.txt", "w") as f:
        f.write(html_data)

    return html_data


def process_html(raw_data):

    raw_data = raw_data.split("<tbody")[1]
    row_count = len(raw_data.split("</tr>"))
    data = [[[None] for column in range(6)] for row in range(row_count - 1)]

    for i in range(row_count - 1):
        start_location = raw_data.find("<tr")
        end_location = raw_data.find("</tr>")
        one_row = raw_data[start_location:end_location]

        for j in range(6):
            cell_start = one_row.find("<td")
            cell_end = one_row.find("</td>")
            data[i][j] = (
                one_row[cell_start:cell_end]
                .replace("<br>", " ")
                .split(">")[1]
                .split("<")[0]
            )
            one_row = one_row.split("</td>", 1)[1]
        raw_data = raw_data.split("</tr>", 1)[1]

    # with open('./new.json', 'w') as f:
    #    json.dump(data, f, indent=4)

    return data


def main():

    # get the data from source
    driver = setup()
    copy = scrape(driver)

    # OR use pre retrieved data
    # with open("./new.txt", "r") as f:
    #    copy = f.read()

    dataset = process_html(copy)
    return dataset


if __name__ == "__main__":
    main()
