from flask import Flask, render_template, url_for, request
import time
from selenium import webdriver
import requests
import pandas as pd
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

    #Redirecting to URL
driver.get('https://dse.com.bd/')
#driver.get('https://dse.com.bd/recent_market_information_more.php')
    #driver.get('https://dse.com.bd/recent_market_information.php')

    #Maximizing Window
driver.maximize_window()

    #Click on Link and Redirect to another page
driver.find_element_by_link_text("Recent Market Information").send_keys("\n")
time.sleep(0.5)
driver.find_element_by_link_text("More recent market information").send_keys("\n")
time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="startDate"]').send_keys("01/01/2013")
time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="endDate"]').send_keys("08/10/2022")
time.sleep(0.5)
driver.find_element_by_name('searchRecentMarket').send_keys("\n")


h = driver.page_source
with open("dse_1year.html","w") as f:
    f.write(h)
driver.close()

    # Downloading contents of the web page
    #url = 'https://dse.com.bd/recent_market_information.php'
    #data = requests.get(url).text
data = open("dse_1year.html", "r")
data = data.read()

    #extracting dsex data
    
    # Create BeautifulSoup object
soup = BeautifulSoup(data, 'html5lib')
    # Get table
table = soup.find('table', _id='data-table')

contents = []
df = pd.DataFrame(columns=['Date', 'Total Trade', 'Total Volume', 'Total Value in Taka (mn)', 'Total Market Cap in Taka (mn)', 'DSEX Index', 'DSES Index',
                            'DS30 Index', 'DGEN Index'])
    # Getting all rows
    #for row in table.find_all('th'):
    #    print(row)

for row in table.tbody.find_all('tr'):    
        # Find all data for each column
    columns = row.find_all('td')
    if(columns != []):
        date = columns[0].text.strip()
        ttrade = columns[1].text.strip()
        tvol = columns[2].text.strip()
        tvt = columns[3].text.strip()
        tmc = columns[4].text.strip()
        dsex = columns[5].text.strip()
        dses = columns[6].text.strip()
        ds30 = columns[7].text.strip()
        dgen = columns[8].text.strip()

        df = df.append({'Date': date,  'Total Trade': ttrade, 'Total Volume': tvol, 'Total Value in Taka (mn)': tvt, 'Total Market Cap in Taka (mn)': tmc,
                        'DSEX Index': dsex, 'DSES Index': dses, 'DS30 Index': ds30, 'DGEN Index': dgen}, ignore_index=True)
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y').dt.date
    #df = df.set_index("Date")
    #df.to_csv('test.csv', sep=',', date_format='%d-%m-%Y', index = True, encoding='utf-8') # True: included index
df.to_excel("output.xlsx", index=False)
print(df)
