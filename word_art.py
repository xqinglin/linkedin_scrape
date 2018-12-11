import json
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import sqlite3 as sqlite
## import the data we collected
def get_all_skills():
    res = []
    conn = sqlite.connect('../linkedin.sqlite')
    cur = conn.cursor()
    data = cur.execute('SELECT * from Skill order by Frequency Desc').fetchall()
    for i in data:
        res.append(i[1])
    conn.close()
    return res


## import the preprocessed data and display it with art words
def run_art_word(skills_all_str):
    driver = webdriver.Chrome(executable_path='/Users/lin/Desktop/SI507/FinalProject/chromedriver')
    driver.get("https://wordart.com/create")
    try:
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "words-import"))
        )
    finally:
        import_button = driver.find_element_by_class_name('words-import')
        import_button.click()
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'form-control'))
        )
          # driver.find_element_by_class_name('form-control').send_keys('HI Hi')
        text = driver.find_elements_by_class_name('form-control')[4].send_keys(skills_all_str)
        driver.find_element_by_class_name('words-import-options-csv-format').click()
        driver.find_elements_by_class_name('modal-footer')[0].find_elements_by_tag_name('button')[0].click()
        time.sleep(2)
        actions = ActionChains(driver)
        next_button=driver.find_element_by_class_name('btn-danger')
        actions.move_to_element(next_button).click(next_button).perform()
    ##document.getElementsByClassName('modal-footer')[0].getElementsByTagName('button')[0].click()
    dif_fomr = input('Enter quit to exit or any other key to see a different form: ')
    while dif_fomr != 'quit':
        actions = ActionChains(driver)
        next_button = driver.find_element_by_class_name('btn-danger')
        actions.move_to_element(next_button).click(next_button).perform()
        dif_fomr = input('Enter quit to exit or any other key to see a different form:')
    print('Done...')
    driver.quit()
def Main(num):
    # skills_all = get_all_skills()
    conn = sqlite.connect('linkedin.sqlite')
    cur = conn.cursor()
    statement = '''
             SELECT Name from Skill ORDER BY Frequency Desc Limit ?;
         '''
    res_sql = cur.execute(statement, (num, )).fetchall()
    skills_all_str=[]
    for i in res_sql:
        skills_all_str.append(i[0])
    skills_all_str = '\n'.join(skills_all_str)
    run_art_word(skills_all_str)
