import json
import requests
from secret import API_geo_google
import sqlite3 as sqlite

def get_count():
    ## count the the number of occurance of each skills
    f = open('people_cache.json', 'r')
    dic = json.load(f)
    f.close()
    skills_all = {}
    for comapny in dic:
        current_company = dic[comapny]
        for people in current_company:
            people_current = current_company[people]
            skills = people_current['skills']
            for sk in skills:
                if sk in skills_all:
                    skills_all[sk] += 1
                else:
                    skills_all[sk] = 1
    return skills_all

def create_db():
    conn = sqlite.connect('linkedin.sqlite')
    cur = conn.cursor()
    statement = '''
             DROP TABLE IF EXISTS 'People';
         '''
    cur.execute(statement)

    statement = '''
             DROP TABLE IF EXISTS 'Company';
         '''
    cur.execute(statement)
    statement = '''
             DROP TABLE IF EXISTS 'Skill';
         '''
    cur.execute(statement)

    statement = '''
                 DROP TABLE IF EXISTS 'Place';
             '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def skill_db():
    # Connect to big10 database
    conn = sqlite.connect('linkedin.sqlite')
    cur = conn.cursor()
    statement = '''
            CREATE TABLE 'Skill' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name' TEXT NOT NULL,
                'Frequency' Integer
            );
        '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def people_db():
    # Connect to big10 database
    conn = sqlite.connect('linkedin.sqlite')
    cur = conn.cursor()
    statement = '''
            CREATE TABLE 'People' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name' TEXT NOT NULL,
                'Title' TEXT,
                'Location' TEXT,
                'Skills' TEXT,
                'Recent_school' TEXT, 
                'Company' TEXT, 
                CompanyId Integer,
                FOREIGN KEY (CompanyId) REFERENCES Company(Id)
            );
        '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def company_db():
    # Connect to big10 database
    conn = sqlite.connect('linkedin.sqlite')
    cur = conn.cursor()
    statement = '''
            CREATE TABLE 'Company' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name' TEXT NOT NULL,
                'Website' TEXT,
                'Location' TEXT,
                'Found_year' TEXT,
                'Specialties' TEXT 
            );
        '''
    cur.execute(statement)
    conn.commit()
    conn.close()
def place_db():
    conn = sqlite.connect('linkedin.sqlite')
    cur = conn.cursor()
    statement = '''
                CREATE TABLE 'Place' (
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'Place' TEXT NOT NULL,
                    'Lat' TEXT,
                    'Lng' TEXT
                );
            '''

    cur.execute(statement)
    conn.commit()
    conn.close()

def insert_allData():
    company_db()
    people_db()
    place_db()
    skill_db()
    ##Insert Company  id_CompanyLocationId = cur.execute('SELECT Id FROM  Countries where EnglishName = ?', (row[5],))
    conn = sqlite.connect('linkedin.sqlite')
    cur = conn.cursor()
    file_comapny = open('company_cache.json', 'r')
    file_json = json.load(file_comapny)
    for company in file_json:
        cur_company = file_json[company]
        name = cur_company['name'].lower()
        website = cur_company['website']
        location = cur_company['location']
        found_year = cur_company['found_year']
        specialties = cur_company['specialties']
        statement = '''
                                    INSERT INTO 'Company' (Name, Website, Location,Found_year,Specialties) VALUES (?, ?, ?,?,?)
                                '''
        cur.execute(statement, (name, website,location, found_year, specialties,))
    conn.commit()
    ##Insert People
    file_people = open('people_cache.json', 'r')
    file_json = json.load(file_people)
    for company in file_json:
        cur_company = file_json[company]
        CompanyId = cur.execute('SELECT Id FROM  Company where name = ?', (company.lower(),)).fetchall()[0][0]
        # print(CompanyId[0][0])
        for url_people in cur_company:
            people = cur_company[url_people]
            name = people['name']
            title = people['title']
            location = people['location']
            skills = people['skills']
            school_recent = people['school_recent']
            statement = '''
                                        INSERT INTO 'People' (Name, Title, Location,Skills,Recent_school, company, CompanyId) VALUES (?, ?, ?,?,?, ?,?)
                                    '''
            cur.execute(statement, (name, title,location, ' '.join(skills), school_recent,company, CompanyId,))
    conn.commit()

    ##Insert Skill
    skill_count = get_count()
    for skill in skill_count:
        count_cur = skill_count[skill]
        statement = '''
                                    INSERT INTO 'Skill' (Name, Frequency) VALUES (?,?)
                                '''
        cur.execute(statement, (skill,count_cur,))
    conn.commit()
    ##Insert Places
    statement='''
        SELECT distinct Location FROM  People
    '''
    conn = sqlite.connect('linkedin.sqlite')
    cur = conn.cursor()
    places = cur.execute(statement).fetchall()
    for cur_place in places:
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}r&key={}'.format(cur_place[0], API_geo_google)
        res = requests.get(url).json()
        location = res['results'][0]['geometry']['location']
        latitude = location['lat']
        longtitude = location['lng']
        cur_statement = '''
             INSERT INTO 'Place' (Place, Lat, Lng) VALUES (?,?,?)
        '''
        cur.execute(cur_statement, (cur_place[0],latitude, longtitude))
    conn.commit()
    conn.close()
    file_people.close()

def insert_company(current_company):
    if current_company == None:
        return
    conn = sqlite.connect('linkedin.sqlite')
    cur = conn.cursor()
    indb_if = cur.execute('select Name from Company where Name = ?', (current_company.name,)).fetchall()

    if len(indb_if) >0:
        print('Already has the company in DB...')
    else:
        statement = '''
                                    INSERT INTO 'Company' (Name, Website, Location,Found_year,Specialties) VALUES (?, ?, ?,?,?)
                                '''
        cur.execute(statement, (current_company.name.lower(), current_company.web,current_company.location, current_company.found_year, current_company.specialties,))
        conn.commit()
    conn.close()


def rebuild_data():
    create_db()
    print("Rebuilding the Linkedin Database...")
    insert_allData()
    print("done!")
