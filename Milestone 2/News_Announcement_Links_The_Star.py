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


# Importing related Python modules/packages.
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pymysql


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
    #print(company_code)            # For debugging purpose 
    #company_code = str(4723)       # For debugging purpose
    main_site = 'https://www.thestar.com.my' 
    URL = 'https://www.thestar.com.my/business/marketwatch/stocks/?qcounter='
    URL = URL + str(company_code)
    print(URL)
    
    req = Request(URL)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")
    #print(soup)

    weblinks = []
    for weblink in soup.findAll('a'):
        weblinks.append(weblink.get('href'))
        
    stock_news_links =[]
    for weblink in weblinks: 
        if weblink != None:
            stock_news_links.append(weblink) 

    #print(weblinks)
    #print(stock_news_links)
    
    for stock_news_link in stock_news_links:
        print(stock_news_link)
        
        x = re.findall("news|announcements", stock_news_link)
        if (x):
            
            # Storing scrapped data to News_Announcement_Links table in KLSE database.
            connection = pymysql.connect(host='localhost', user='root', password='', db='KLSE')
            cursor = connection.cursor()
            
            insert_to_database = (company_code, main_site, stock_news_link)
            
            sql = 'INSERT INTO news_announcement_links (stock_code, main_site, weblink) VALUES (%s,%s,%s)'
            cursor.execute(sql, insert_to_database)	
            connection.commit()
            
            print('Stock Code:'+ company_code)
            print('Website:'+ main_site + stock_news_link)
            print("Records were saved to database successfully\n\n")
        
        else:
            
            print("No match")

