import sqlite3 as sqlite

def getSkills():
	res = []
	res.append(['Skill','Count'])
	conn = sqlite.connect('../linkedin.sqlite')
	cur = conn.cursor()
	data = cur.execute('SELECT * from Skill order by Frequency Desc').fetchall()
	for i in data:
		list_cur= [i[1], i[2]]
		res.append(list_cur)
	conn.close()
	return res 

def getPeople():
	res = []
	res.append(['Name', 'Title','Location', 'Skills', 'Recent_school', 'Company'])
	conn = sqlite.connect('../linkedin.sqlite')
	cur = conn.cursor()
	data = cur.execute('SELECT Name, Title, Location, Skills, Recent_school, Company from People ').fetchall()
	for i in data:
		list_cur= [i[0], i[1], i[2], i[3], i[4], i[5]]
		res.append(list_cur)
	conn.close()
	return res 

def getCompanys():
	res = []
	res.append(['Company', 'Website', 'Location', 'Found Year', 'Specialties'])
	conn = sqlite.connect('../linkedin.sqlite')
	cur = conn.cursor()
	data = cur.execute('SELECT *from Company ').fetchall()
	for i in data:
		list_cur= [i[0], i[1], i[2], i[3], i[4]]
		res.append(list_cur)
	conn.close()
	return res 