############################################################################################
#                                                                                          #
#      This code is written during team meet-up by team members as shown below ...         #
#                                                                                          #  
#                    HAFIFI BIN YAHYA - WQD170042                                          #
#                    NOR ASMIDAH BINTI MOHD ARSHAD - WQD180006                             #
#                    MAS RAHAYU BINTI MOHAMAD - WQD180048                                  #
#                    LEE CHUN MUN - WQD180066                                              #
#                    JOJIE ANAK NANJU - WQD180029                                          #
#                                                                                          #
############################################################################################

import requests
import re
import pymysql
from bs4 import BeautifulSoup

# Retrieving list of main board companies from KLSE database, Main_Listed_Companies table.
connection = pymysql.connect(host='localhost', user='root', password='', db='KLSE')
cursor = connection.cursor()
query = "SELECT `stock_code` FROM `main_listed_companies`"
cursor.execute(query)
select_result = cursor.fetchall()
companies_codes = [list(i) for i in select_result]
#print(companies_codes)        # For debugging purpose 

for company_code in companies_codes:
    company_code = company_code[0]
    #print(company_code)       # For debugging purpose
    # Retrieving all weblinks(news) those related to the company_code or stock_code.
    connection = pymysql.connect(host='localhost', user='root', password='', db='KLSE')
    cursor = connection.cursor()
    query = "SELECT `weblink` FROM `news_announcement_links` where `stock_code` = "
    query = query + "'" + str(company_code) + "'"
    cursor.execute(query)
    select_result = cursor.fetchall()
    weblinks = [list(i) for i in select_result]
    print(weblinks)        # For debugging purpose
    
    for weblink in weblinks:
        weblink = weblink[0]
        print(weblink)
        main_site = 'https://www.klsescreener.com'
        URL = main_site + weblink
        
        list_of_searches_in_html = ['h1', 'h2', 'h3', 'p', 'a', 'ul', 'span', 'input']
        website = requests.get(URL)
        soup = BeautifulSoup(website.content, 'lxml')
        tags = soup.find_all(list)
        
        connection = pymysql.connect(host='localhost', user='root', password='', db='KLSE')
        cursor = connection.cursor()
        query = "SELECT `known_name` FROM `main_listed_companies` where `stock_code` ="
        query = query + "'" + str(company_code) + "'"
        cursor.execute(query)
        select_result = cursor.fetchall()
        known_names = [list(i) for i in select_result]
        
        for known_name in known_names:
            known_name = known_name[0]
            known_name = ''.join(known_name.split()[:1])
            regex = str('^\s*') + str(known_name) + str('.*')
            print(regex)
            text = soup.find_all(text=re.compile(regex, re.I))
            print(company_code)
            print(text)
            
            if text is not None:
                text = str(text)
            
            connection = pymysql.connect(host='localhost', user='root', password='', db='KLSE')
            cursor = connection.cursor()
            
            try:
                insert_to_database = (company_code, text, weblink)
                sql = 'INSERT INTO news_announcement_extraction (stock_code, news_details, link) VALUES (%s,%s,%s)'
                cursor.execute(sql, insert_to_database)	
                connection.commit()
            except:
                print('No Related News')
            