import argparse, os, time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import word_art
import json
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from secret import email, password
import setup_db
import map_plot
import secret

class Company(object):
    """docstring for People"""
    def __init__(self, name='None', web='None', location='None', found_year='None', specialties='None'):        
        self.name = name.lower()
        self.web = web
        self.location = location
        self.found_year = found_year
        self.specialties = specialties
        self.employee = []

    def add_employee(self, person):
        self.employee.append(person)
        
class Person(object):
        """docstring for Company"""
        def __init__(self, name='None', title='None', location='None', skills=[], school='None'):
            self.name = name
            self.title = title
            self.location = location
            self.location = location
            self.skills = skills
            self.school = school           

                       
def get_people_in_company(browser,job_title,company_name):
    ## enter the information for searching(company name and the job title we are interested in)
    ## Get people's profile link from list
    ## Enter keyword for searching and handle exception
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, "input"))
        )
    finally:
        search_bar = browser.find_element_by_tag_name('input')
        search_content = job_title + ' ' + company_name
        search_bar.send_keys(search_content)
        search_bar.send_keys(Keys.ENTER)
    time.sleep(3)
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "search-vertical-filter__filter-item-button"))
        )
        browser.find_elements_by_class_name('search-vertical-filter__filter-item-button')[0].click()
    except:
        return
    ## Get the url of people's profile 
    num_people = input('How many people you want to collect?')
    num_people = int(num_people)
    count_people = 0
    list_people_url = []
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "search-result__result-link"))
        )
    finally:
        list_people = browser.find_elements_by_class_name('search-result__result-link')
    while count_people < num_people:
        for i in list_people:
            if count_people >= num_people:
                break
            try:
                anchor = i.get_attribute('href')
            except:
                anchor = None
            if anchor not in list_people_url and anchor is not None:
                list_people_url.append(anchor)
                print(count_people)
                count_people += 1
        try:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(browser, 10).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "next"))
            )
        finally:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            next_button = browser.find_elements_by_class_name('next')[0]
            actions = ActionChains(browser)
            actions.move_to_element(next_button).click(next_button).perform()
        try:
            WebDriverWait(browser, 10).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "search-result__result-link"))
            )
        finally:

            list_people = browser.find_elements_by_class_name('search-result__result-link')
    return list_people_url

def info_scrapping(browser, list_people_url, current_company):
    ## Scrape each person's information from profile
    try:
        CACHE_FNAME = 'people_cache.json'
        cache_file = open(CACHE_FNAME,'r')
        cache_content = cache_file.read()
        dic_data = json.loads(cache_content)
        cache_file.close()
        if current_company.name in dic_data:
            dic_this = dic_data[current_company.name]
        elif current_company.name.title() in dic_data:
            dic_this = dic_data[current_company.name.title()]
        else:
            dic_data[current_company.name] ={}
            dic_this = {}
    except:
        dic_data ={}
        dic_data[current_company.name] = {}
    cur_dic = dic_data[current_company.name]
    for i in range(len(list_people_url)):
        url_cur = list_people_url[i]
        if url_cur in dic_this:
            print('Already had it in cache...')
            c_p = dic_this[url_cur]
            person = Person(name=c_p['name'], title=c_p['title'], location=c_p['location'], skills=c_p['skills'], school=c_p['school_recent'])
            current_company.add_employee(person)
        else:
            browser.get(url_cur)
            try:
                WebDriverWait(browser, 10).until(
                    expected_conditions.presence_of_element_located((By.TAG_NAME, "h1"))
                )
            finally:
                name = browser.find_element_by_tag_name('h1').text
                job_title = browser.find_element_by_tag_name('h2').text
                location = browser.find_element_by_tag_name('h3').text
                browser.execute_script("window.scrollTo(0, 0.5*document.body.scrollHeight);")
                time.sleep(2)
            try:
                WebDriverWait(browser, 10).until(
                    expected_conditions.presence_of_element_located((By.CLASS_NAME, "pv-profile-section__card-action-bar"))
                )
                showmore_button = browser.find_element_by_class_name('pv-profile-section__card-action-bar')
                actions = ActionChains(browser)
                actions.move_to_element(showmore_button).perform()
                time.sleep(2)
                actions.click(showmore_button).perform()
            except:
                print('No skill found')
            finally:
            # showmore_button.click()
                skills = browser.find_elements_by_class_name('pv-skill-category-entity__name')
            skills_list = []
            for skill in skills:
                skills_list.append(skill.text)
            try:
                school = browser.find_elements_by_class_name('pv-entity__school-name')[0].text
            except:
                school = ''
            cur_dic[url_cur] = {
                'name':name,
                'title':job_title,
                'location':location,
                'skills':skills_list,
                'school_recent':school
            }
            person = Person(name=name, title=job_title, location=location, skills=skills_list, school=school)
            current_company.add_employee(person)
    ## Save the data in json file
    cache_file = open(CACHE_FNAME, 'w')
    dic_data[current_company.name] = cur_dic
    cache_file.write(json.dumps(dic_data))
    cache_file.close()
    return current_company

def get_company_info(browser, target_company):
    ## Get the information of Company 
    try:
        CACHE_FNAME = 'company_cache.json'
        cache_file = open(CACHE_FNAME, 'r')
        cache_content = cache_file.read()
        dic_data = json.loads(cache_content)
        cache_file.close()
    except:
        dic_data = {}
    if target_company not in dic_data and target_company.title() not in dic_data:
        try:
            base_url = 'https://www.linkedin.com/company/{}/'.format(target_company)
            browser.get(base_url)
            print('Getting the information of this Company...')
            WebDriverWait(browser, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, "org-about-company-module__show-details-icon"))
            )
            time.sleep(4)
            showmore_button = browser.find_element_by_class_name("org-about-company-module__show-details-icon")
            ActionChains(browser).move_to_element(showmore_button).click().perform()
            browser.execute_script("window.scrollTo(0, 500);")
            name = browser.find_element_by_tag_name('h1').text
            website = browser.find_elements_by_class_name('org-about-company-module__company-page-url')[0].text
            location = browser.find_elements_by_class_name('org-about-company-module__headquarters')[0].text
            found_year = browser.find_elements_by_class_name('org-about-company-module__founded')[0].text
            specialties = browser.find_elements_by_class_name('org-about-company-module__specialities')[0].text
            print(name, website, location, found_year, specialties)
            cur_dic = {
                'name': name,
                'website': website,
                'location': location,
                'found_year': found_year,
                'specialties': specialties
            }
            dic_data[name] = cur_dic
            CACHE_FNAME = 'company_cache.json'
            cache_file = open(CACHE_FNAME, 'w')
            cache_file.write(json.dumps(dic_data))
            cache_file.close()
            current_company = Company(name=name, web=website, location=location, found_year=found_year, specialties=specialties)
        except:
            print('This company doesn\'s have much information')
            current_company = Company()
    else:
        if target_company in dic_data:
            cached_coampny = dic_data[target_company]
        elif target_company.title() in dic_data:
            cached_coampny = dic_data[target_company.title()]
        print('Already has it in cache...')
        current_company = Company(name=cached_coampny['name'], web=cached_coampny['website'], location=cached_coampny['location'], found_year=cached_coampny['found_year'],specialties=cached_coampny['specialties'])
    return current_company

def login(browser):
    ## Authentication
    emailElement = browser.find_element_by_id("username")
    emailElement.send_keys(email)
    passElement = browser.find_element_by_id("password")
    passElement.send_keys(password)
    passElement.submit()

def input_scrape(chrome_options):
    ## interaction with user input for scrapping section

    browser = webdriver.Chrome(executable_path=secret.path,options=chrome_options)
    browser.get("https://linkedin.com/uas/login")
    login(browser)
    company_name = input('Enter the company you want to scrape or enter \'n\' to create the Database: ').lower()
    if company_name!='n':
        current_company = get_company_info(browser, company_name)
        job_title = input('Enter the job title you are interested in or enter \'n\' to create the Database:').lower()
    else:
        job_title='n'
    if job_title!='n':
        list_people_url = get_people_in_company(browser, job_title, company_name)
        current_company = info_scrapping(browser, list_people_url, current_company)

        if_continue = input('scrape another company or enter \'n\' to create the Database:')
    else:
        if_continue='n'
    while if_continue != 'n':
        company_name = if_continue.lower()
        current_company = get_company_info(browser, company_name)
        job_title = input('Enter the job title you are interested in:')
        list_people_url = get_people_in_company(browser, job_title, company_name)
        current_company = info_scrapping(browser, list_people_url, current_company)
        if_continue = input('scrape another company or enter \'n\' to next step:').lower()
    browser.close()
    return current_company

def Main():
    # Open another headless browser
    chrome_options = Options()
    print("Welcome! The code starts to run...")
    # The scrape people information from Linkedin
    input_= input('Input \'y\' to scrape or enter \'n\' to next step:')
    if input_ == 'y':
        try:
            current_company = input_scrape(chrome_options)
        except:
            current_company = None
            print('The internet is not good or you are kicked out from log-in, let\'s view the data we got first!')
    # Build up the database
    db = input('Enter \'y\' to insert into the database, enter\'rebuild\' to rebuild the datebase or enter \'n\' to view the display:')
    if db == 'rebuild':
        setup_db.rebuild_data()
    elif db == 'y':
        setup_db.insert_company(current_company)
    # Display the data we scrapped
    visual_num = input('Display the data with(or enter \'quit\' to exit):\n1.Art word\n2.Flask Website(quit and run flask)\n3.Map\n4.Histogram\n:')
    while visual_num != 'quit':
        if visual_num == '1':
            num_skill=input('Please input the number of top skill you want to view:')
            try: 
                num_skill_int = int(num_skill)
                word_art.Main(num_skill_int)
            except:
                print('The input is not valid')
        elif visual_num == '2':
            print('Please quit and run the \'app.py\' in \'flask_display\' at terminal.')
        elif visual_num =='3':
            map_plot.Main()
        elif visual_num =='4':
            num_skill = input('Please input the number of top skill you want to view:')
            map_plot.plot_Histogram(num_skill)
        visual_num = input('Display the data with(or enter \'quit\' to exit):\n1.Art word\n2.Flask Website\n3.Map\n4.Histogram\n:')
    print('Bye!')

if __name__ == '__main__':
    Main()