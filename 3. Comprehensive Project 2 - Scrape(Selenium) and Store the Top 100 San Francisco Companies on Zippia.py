import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import math
from pymongo import MongoClient
import re
import json
from random import randint


driver = webdriver.Chrome('/usr/local/bin/chromedriver') # change this path to your driver's path
driver.implicitly_wait(10)
driver.set_script_timeout(120)
driver.set_page_load_timeout(20)


# Go to the 20 Best Company page using Selenium
link = 'https://www.zippia.com/company/best-companies-in-san-francisco-ca/'
driver.get(link)
time.sleep(5.2)


# By default the website will show the top 20 companies
# Click the 'Show More' Button for 4 times to load the top 100 companies
# You can change the value for variable <num_companies_shown> to the number of companies you are interested in

num_companies_shown = 100  # Change this value to load the number of companies you are interested in
num_pages_need = math.floor(num_companies_shown / 20) - 1

for i in range(num_pages_need):
    # try to click the 'Show More' Button
    try:
        button_showmore = driver.find_element_by_xpath("//p[@class='showMoreTopCompanies primary-button-big']")
        button_showmore.click()
        time.sleep(3.7)
    # However, sometimes there will be a pop-up window, if so, close the pop-up window
    except:
        button_closepopwindow = driver.find_element_by_xpath("//div[@class = 'session-popup-close-btn']")
        button_closepopwindow.click()
        time.sleep(3.2)


### Connect to MongoDB and create DataBase for Top100 companies
client = MongoClient('localhost:27017')
database_name = "Zippia_SF_Top_100_Companies"
Zippia_SF_Top_100_Companies = client[database_name]
### Create a new collection called Zippia_SF_Top_100_Companies in the database
collection_name = "Zippia_SF_Top_100_Companies"
collection = Zippia_SF_Top_100_Companies[collection_name]



# The folloing prefix 'c_' of each variable stands for 'company'

### to contain the links that direct to each company
c_link_list = []

for i in range(num_companies_shown):
    company_card_i_locator = "div[id='companyCard" + str(i) + "']"
    company_card_i = driver.find_element_by_css_selector(company_card_i_locator)
    soup = BeautifulSoup(company_card_i.get_attribute('outerHTML'), 'html.parser')

    ### Get the rank and name of the company on the list
    c_rankandname = soup.find('h2').text
    if i <=8:
        c_rank = int(c_rankandname[0])
        c_name = c_rankandname[3:]
    elif i <= 98:
        c_rank = int(c_rankandname[:2])
        c_name = c_rankandname[4:]
    else:
        c_rank = int(c_rankandname[:3])
        c_name = c_rankandname[5:]

    ### Get the link direct to the company's page
    c_page_link = "https://www.zippia.com" + soup.div.a['href']
    print(c_page_link)
    c_link_list.append(c_page_link)

    ### Get the Zippia score of each company
    c_zippia_score = soup.find('p', class_ = 'greyLabel').text
    ### Get the discription of each company
    c_highlights = soup.select('div[class^=companyDescription]')[0].p.text


    ### Concat the above information into a document and insert the document into the MongoDB collection
    document = {'Ranking': c_rank,
                'Company Name': c_name,
                'Zippia Link': c_page_link,
                'Zippia Score': c_zippia_score,
                'Company Description': c_highlights
                }
    collection_test.insert_one(document)

#     print(c_rank)
#     print(c_name)
#     print(c_page_link)
#     print(c_zippia_score)
#     print(c_highlights)

# print(c_link_list)



### Access all 100 companies' webpage
### Later we will extract more information from the page and update them into the collection

for i in range(num_companies_shown):
    ith_c_link = c_link_list[i]

    driver.get(ith_c_link)
    time.sleep(1.5)

    ### There are two types of potential pop-up window, if they appears, close them
    try:
        pop_window_close = driver.find_element_by_xpath("//img[@class^='jobAlertPopup_closeIcon']")
        pop_window_close.click
    except:
        pass

    try:
        pop_window_close2 = driver.find_element_by_xpath("//div[@style='display: inline-block; max-width: 100%; overflow: hidden; position: relative; box-sizing: border-box; margin: 0px;']")
        pop_window_close2.click()
    except:
        pass
    time.sleep(1.3)

    ### Click the overview button to get the general information about the company
    ### Some links above will directlly take us to the 'Overview' tab but some will not.
    ### If we are already taken to 'Overview' page, then the try part will fail
    try:
        overview_button = driver.find_element_by_xpath("//a[text()='Overview']")
        overview_button.click()
    except:
        pass

    industry_section = driver.find_element_by_xpath("//p[text()='Industry']")
    industry = industry_section.find_element_by_xpath('.//following-sibling::*').text

    revenue_section = driver.find_element_by_xpath("//p[text()='Revenue']")
    revenue = revenue_section.find_element_by_xpath('.//following-sibling::*').text

    headquarter_section = driver.find_element_by_xpath("//p[text()='Headquarters']")
    headquarter = headquarter_section.find_element_by_xpath('.//following-sibling::*').text

    employees_section = driver.find_element_by_xpath("//p[text()='Employees']")
    employees = employees_section.find_element_by_xpath('.//following-sibling::*').text


    website_block = driver.find_element_by_xpath("//div[@class='col-12 JobCompanyInfoParameter companyDomain']")
    website_text = website_block.text[website_block.text.index('\n') + 1:]
    website = "https://" + website_text

    foundedin_section = driver.find_element_by_xpath("//p[text()='Founded in']")
    foundedin = foundedin_section.find_element_by_xpath('.//following-sibling::*').text

    organizationtype_section = driver.find_element_by_xpath("//p[text()='Organization Type']")
    organizationtype = organizationtype_section.find_element_by_xpath('.//following-sibling::*').text

    time.sleep(randint(1,3))


    ### Get the link for job page
    try:
        jobs_button = driver.find_element_by_xpath("//a[text()='Jobs']")
        job_page_link = jobs_button.get_attribute('href')
    except:
        job_page_link = "Not Avaliable"


    ### Click the 'Salary' section and scrape inforamation about salaries
    try:
        ### if the 'Salary' Section exists:
        salary_button = driver.find_element_by_xpath("//a[text()='Salary']")
        salary_button.click()
        time.sleep(randint(3,5))

        avg_salary = driver.find_element_by_xpath("//div[@class='average-salary-number']").text

        entry_level_salary_block = driver.find_element_by_xpath("//div[@class='entry-level-salary']").text
        entry_level_salary = entry_level_salary_block[entry_level_salary_block.index('\n') + 1:]

        salary_chart_block = driver.find_element_by_xpath("//div[@class='salary-chart-wrapper']")
        ten_percent_salary = salary_chart_block.find_element_by_xpath("//div[@class='first svg']").find_element_by_xpath("//div[@class='number']").text

        nighty_percent_quantile = salary_chart_block.find_element_by_xpath("//div[@class='ninth svg']").text
        nighty_percent_salary = nighty_percent_quantile[0: nighty_percent_quantile.index('\n')]
    except:
        ### if the 'Salary' Section doesn't exist:
        avg_salary = "Not Avaliable"
        entry_level_salary = "Not Avaliable"
        ten_percent_salary = "Not Avaliable"
        nighty_percent_salary = ''

#     html = driver.find_element_by_tag_name('html')
#     html.send_keys(Keys.PAGE_DOWN)
#     time.sleep(1)
#     html.send_keys(Keys.PAGE_DOWN)
#     time.sleep(1)
#     html.send_keys(Keys.PAGE_DOWN)
#     time.sleep(1)
#     html.send_keys(Keys.PAGE_DOWN)
#     time.sleep(1)
#     html.send_keys(Keys.PAGE_DOWN)
#     time.sleep(1)

    ### Scrape the Salary Ranking by position table in the Salary page
    try:
        ### if the table exists:
        salary_by_position_block = BeautifulSoup(driver.find_element_by_xpath("//section[@class='salary-company-job-title-section']").get_attribute('outerHTML'), 'html.parser')
        salary_by_position_table = salary_by_position_block.find('tbody')
        salary_by_position_rows = salary_by_position_table.find_all('tr')
        salary_by_position_container = []

        for row in salary_by_position_rows:
            cols = row.find_all('td')
            rank = int(cols[0].text)
            job_title = cols[1].text
            avg_yearly_salary = cols[2].text
            avg_hourly_salary = cols[3].text

            position_salary_i = {'Ranking' : rank,
                    'Job Title' : job_title,
                    'Yearly Average Salary' : avg_yearly_salary,
                    'Hourly Average Salary' : avg_hourly_salary
                   }
            salary_by_position_container.append(position_salary_i)
    except:
        ### If table doesn't exist:
        salary_by_position_container = 'Null'

#     print(salary_by_position_container)


    ### Update the new information into the database
    query = {"Ranking": i+1}
    new_info_industry = {"$set": {"Industry": industry}}
    new_info_revenue = {"$set": {"Revenue": revenue}}
    new_info_headquarter = {"$set": {"Headquarter": headquarter}}
    new_info_employees = {"$set": {"Employee Number": employees}}
    new_info_website = {"$set": {"Website": website}}
    new_info_foundedin = {"$set": {"Founded In": foundedin}}
    new_info_organizationtype = {"$set": {"Organization Type": organizationtype}}
    new_info_jobs = {"$set": {"Jobs": job_page_link}}
    new_info_avg_salary = {"$set": {"Average Salary": avg_salary}}
    new_info_salaryrange10_90 = {"$set": {"Salary Range": ten_percent_salary + '-' + nighty_percent_salary}}
    new_info_salarybyposition = {"$set": {"Salary Ranking by Position": salary_by_position_container}}

    collection.update_one(query, new_info_industry)
    collection.update_one(query, new_info_revenue)
    collection.update_one(query, new_info_headquarter)
    collection.update_one(query, new_info_employees)
    collection.update_one(query, new_info_website)
    collection.update_one(query, new_info_foundedin)
    collection.update_one(query, new_info_organizationtype)
    collection.update_one(query, new_info_jobs)
    collection.update_one(query, new_info_avg_salary)
    collection.update_one(query, new_info_salaryrange10_90)
    collection.update_one(query, new_info_salarybyposition)
