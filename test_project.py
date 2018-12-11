import unittest
import linkedin_scrape as linkedin
import json
import sqlite3 as sqlite

class TestMedia(unittest.TestCase):

    ## Test the classes(Company() and Person()) and their functionality made in linkedin_scrape
    def testPerson(self):
        m1 = linkedin.Person()
        m2 = linkedin.Person(name='Lin', title='Student', location='Ann Arbor', skills=['Java','Python'], school='University of Michigan')

        self.assertEqual(m1.name, "None")
        self.assertEqual(m1.title, "None")
        self.assertEqual(m2.title, "Student")
        self.assertEqual(m2.location, "Ann Arbor")
        self.assertIsInstance(m2, linkedin.Person)

    def testCompany(self):
        m1 = linkedin.Company(name='Henglei', web='www.henlei.com', location='Shanxi', found_year='2004', specialties='Architecture Design')
        p1 = linkedin.Person(name='Lin', title='Strcuctural Engineer', location='Ann Arbor', skills=['Java', 'Python'],
                             school='University of Michigan')
        m1.add_employee(p1)
        self.assertEqual(m1.location, "Shanxi")
        self.assertEqual(m1.specialties, "Architecture Design")
        self.assertIsInstance(m1, linkedin.Company)
        self.assertIn(p1, m1.employee)
        self.assertEqual(p1, m1.employee[0])
    ## Test if the json file contains the data scrapped
    def testCache(self):
        file = open('company_cache.json','r')
        data_company = json.load(file)
        file.close()
        self.assertIn('Apple', data_company)
        self.assertIn('Amazon', data_company)
        self.assertEqual('2004', data_company['Facebook']['found_year'])
        self.assertEqual('http://www.google.com', data_company['Google']['website'])

    ## Test the database
    def testDB(self):
        conn = sqlite.connect('linkedin.sqlite')
        cur = conn.cursor()
        statement1 = '''
            select  count(*)  from People
        '''
        num_people = cur.execute(statement1).fetchall()[0][0]
        self.assertGreater(num_people, 100)
        conn.close()

        conn = sqlite.connect('linkedin.sqlite')
        cur = conn.cursor()
        statement1 = '''
            select  Name from Skill Order by Frequency Desc limit 1
        '''
        num_people = cur.execute(statement1).fetchall()[0][0]
        self.assertEqual(num_people, 'Java')
        conn.close()

        conn = sqlite.connect('linkedin.sqlite')
        cur = conn.cursor()
        statement1 = '''
            select  Found_year from Company where Name = \'netflix\' 
        '''
        num_people = cur.execute(statement1).fetchall()[0][0]
        self.assertEqual(num_people, '1997')
        conn.close()

unittest.main()
