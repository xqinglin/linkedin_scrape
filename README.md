# Scrapping Linkedin Profile!

This is a python program for scrapping Linkedin profiles that lets a user choose a job title for a company. The data display will includes individual informations, the most frequent skills/technique and the working location from Linkedin. 


# **Data sources**

## Linkedin: 
the data include the company profile and people profile are from Linkedin. The account with **premium** of Linkedin is needed for scrapping, otherwise you only can visit very limited number of profiles.

Linkedin URL: https://www.linkedin.com/ 
> **Note:** The a premium of Linkedin is need for better scrapping.  
## Google Map
Google map API is used to find the geolocaion of people working place and plot the working place in Map in **Plotly** later.


# **Brief description**
## linkedin_scrape.py

The main file for running the app and also the start point. 
**The functionality lincludes:**

 1. The interaction with user. It asks if the user want to scrape more data, insert the scrappe the data, rebuild the whole database or display the rebuild the data.
 2. The OOP(Object Oriented Programming) for the project. Build up a projection from the real people and companys  to code. For example, the class 'Company()' has 'name', 'website', 'speciality', etc. as its field, while the class 'Person()' has 'skills', 'school', 'name', 'location', etc. as its own field. The class 'Company()' has many employees, so it also has a List of 'Person()' as the field 'employees'. 
 3. The key point of this project: 'Scrapping!'. The **Selenium** is used as the main tool for scrapping along with a **Chrome Driver** as the broswer. The process will first go through the authentication with 'login()'. Then scrapping the informations of the target company. After that, it will collect the amount of the interest of the URL of the employee's profile. With the collected URLs, the program will start will scrape the information of each person's information.
  >**Note:** A **Chrome Driver** is needed in same folder for scrapping. 

  4. The display choices for users. 1.Art word, 2.Flask Website(**quit and run flask**) 3.Map 4.Histogram
 > **Note:** For second display, the user need to run the flask server to view the result. More instruction will be given later. 

5. The cache is used for both company and employees  scrapping. Both of them have its own cache file. The key for company is the company name, while the key for employee is the URL(different people could share same name). 

# **User guide**

## Set up 

1. Download a browser driver, prefer **Chrome Driver**. 
> **download**: http://chromedriver.chromium.org/downloads
2. pip install all the packages for both main fold and flask folder. 
>**There are two **requirements.txt**. One is in the main folder, another one is in 'flask_display'.  Both of them are used.
3. Get into the current folder place and run **'python linkedin_scrape.py'** in terminal. The program will guide you enter company and the number of profile you want to scrape, also give you option to insert new data into database or rebuild the whole database. 
4. At the end the running, the terminal will give you choices of display type. 
The display choices for users: 
	1.Art word
	2.Flask Website(**quit and run flask**) 
	3.Map 
	4.Histogram. 
>**You would be able to view the display of all choices except the second one 'Flask Website'. 
6. Enter 'cd flask_display' to enter the flask folder. (Please install all package in requirement before running). Then run **'Python app.py'** to start the server. Open 'http://127.0.0.1:5000/' in browser and the result will be displayed~
>** Notice that if keep scrapping, the linkedin will kick you out and ask you do a test. In this is case, you have to do the a test like 'Pick all cars from image' before continue to scrape. 

