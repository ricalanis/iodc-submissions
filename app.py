import os
import time

from selenium import webdriver

import pandas as pd

def login(driver):
    driver.get('http://easychair.org/account/signin.cgi')
    time.sleep(3)
    user_input = driver.find_elements_by_name("name")[0]
    pass_input = driver.find_elements_by_name("password")[0]
    user_input.send_keys(os.environ["easychair_user"])
    pass_input.send_keys(os.environ["easychair_password"])
    button = driver.find_elements_by_name("Log in")[0]
    button.click()
    return True


def go_submissions(driver):
    time.sleep(5)
    submissions_button = driver.find_element_by_id("menu1")
    submissions_button.click()
    return True


def get_submissions(driver):
    time.sleep(1)
    sub_input = driver.find_elements_by_tag_name("table")[5]
    a = sub_input.find_elements_by_tag_name("a")
    links = []
    for link in a:
        text = link.get_attribute("href")
        if type(text)==str:
            if "https" in text:
                links.append(text)
    return links


def conference_data(driver):
    time.sleep(1)
    abstract_data = driver.find_elements_by_tag_name("table")[6]
    row_dict = {}
    table_rows = abstract_data.find_elements_by_tag_name("tr")
    table_rows.pop(0)
    for row in table_rows:
        row_data = row.find_elements_by_tag_name("td")
        field_name = row_data[0].text
        field_content = row_data[1].text
        row_dict[field_name] = field_content
    return(row_dict)

def author_data(driver):
    time.sleep(1)
    people_data = driver.find_elements_by_tag_name("table")[7]
    table_rows = people_data.find_elements_by_tag_name("tr")
    titles = table_rows[0].find_elements_by_tag_name("td")
    data = table_rows[1].find_elements_by_tag_name("td")
    author_data = {}
    i = 0
    for i in range(0,len(titles)):
        author_data[titles[i].text]=data[i].text
    return author_data


def main():
    driver = webdriver.Chrome()
    login(driver)
    go_submissions(driver)
    submissions_links = get_submissions(driver)
    submissions = []
    authors = []
    for link in submissions_links:
        driver.get(link)
        authors.append(conference_data(driver))
        submissions.append(author_data(driver))
    authors_df = pd.DataFrame(authors)
    submissions_df  = pd.DataFrame(submissions)
    authors_df.to_csv("authors.csv", index_col = False)
    submissions_df.to_csv("submissions.csv", index_col = False)
    return "Great success!"

if __name__ == '__main__':
    main()
