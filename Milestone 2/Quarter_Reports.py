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
import lxml.html
import requests
import pymysql


# Retrieving list of main board companies from KLSE database, Main_Listed_Companies table.
connection = pymysql.connect(host='localhost', user='root', password='', db='KLSE')
cursor = connection.cursor()
query = "SELECT `stock_code` FROM `main_listed_companies`"
cursor.execute(query)
select_result = cursor.fetchall()
companies_codes = [list(i) for i in select_result]
#print(companies_codes)        # For debugging purpose 


# Using for loop to crawl on every company from klsescreener website. 
# The basic URL is shown below.
# The URL is concatenate with the company or stock code.
# As the result, the URL can be used as html address to go to specific stock page of the respective company.
for company_code in companies_codes:
    company_code = company_code[0]
    #print(company_code)            # For debugging purpose 
    #company_code = str(4723)       # For debugging purpose 
    URL = 'https://www.klsescreener.com/v2/stocks/view/'
    URL = URL + str(company_code)
    print(URL)
    html = requests.get(URL)
    doc = lxml.html.fromstring(html.content)

    # QR = Quarter Report Tab Path.
    # We scrape data from Quarter Report tab of the webpage.
    QR = doc.xpath('//div[@id="quarter_reports"]')[0]
    
    # Most of the companies release Quarter Reports
    # Means 4 reports for every year.
    # But there are companies that not released the previous years reports such as for year 2016, 2017 etc.
    i = [-6,-5,-4,-3,-2,-1]    
    q = 1
    a = 6
    
    # The code gives flexibility in scrapping Quarter Reports.
    # If the user needs to scrap Quarter Report just for a year back, then user may use q < 5.
    # If the user needs to scrap Quarter Report for 2 years back, then user may use q < 9.
    # And so on for 3 years, 4 years back.
    while q < 9:
        
        if q <= 4:
            Q_Year = 2018
        
        elif 5 <= q <= 8:
            Q_Year = 2017
        
        elif 9 <= q <= 12:
            Q_Year = 2016
            
        elif 13 <= q <= 16:
            Q_Year = 2015 
        
        elif 17 <= q <= 20:
            Q_Year = 2014 
        
        # Scrapped quarter financial data.   
        null = None
        
        try:          
            EPS = QR.xpath('.//td[@class="number"]/text()')[i[0]+a]
        except:
            EPS = str(null)
            
        try:
            DPS = QR.xpath('.//td[@class="number"]/text()')[i[1]+a]
        except:
            DPS = str(null)
            
        try:
            NTA = QR.xpath('.//td[@class="number"]/text()')[i[2]+a]
        except:
            NTA = str(null)
            
        try: 
            Revenue = QR.xpath('.//td[@class="number"]/text()')[i[3]+a]
        except:
            Revenue = str(null)
        
        try:
            PL = QR.xpath('.//td[@class="number"]/text()')[i[4]+a]
        except:
            PL = str(null)
            
        try:
            Quarter = QR.xpath('.//td[@class="number"]/text()')[i[5]+a]
        except:
            Quarter = str(null)
        
        q = q + 1
        a = a + 6
        
        # Storing scrapped data to Quarter_Reports table in KLSE database.
        connection = pymysql.connect(host='localhost', user='root', password='', db='KLSE')
        cursor = connection.cursor()
        
        insert_to_database = (company_code, EPS, DPS, NTA, Revenue, PL, Quarter, Q_Year)
        
        sql = 'INSERT INTO quater_reports (stock_code, EPS, DPS, NTA, Revenue, PL, Quarter, Q_Year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, insert_to_database)	
        connection.commit()
        
        # For debugging purpose
        print('Stock Code:'+ company_code)
        print('EPS:'+ EPS)
        print('DPS:'+ DPS)
        print('NTA:'+ NTA)
        print('Revenue:'+ Revenue)
        print('PL:'+ PL)
        print('Quarter:'+ Quarter)
        print('Q Year:' + str(Q_Year))
        print("Records were saved to database successfully\n\n")