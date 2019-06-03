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

# Batch 2

# Importing related Python modules/packages.
from lxml import html
from datetime import datetime
import requests
import pymysql


# List of companies that listed in KLSE Main Board.
companies = (
'TUNEPRO','AMEDIA','AMTEL','ASTRO','AXIATA','BJMEDIA','DIGI','ECOHLDS','GPACKET','GPACKET-WB',
'MAXIS','MEDIA','MEDIAC','OCK','OCK-WA','PPG','SASBADI','SJC','STAR','TIMECOM',
'TM','UTUSAN','3A','AAX','AAX-WA','ACOSTEC','AEON','AHB','AHB-WB','AIRASIA',
'AJI','AMTEK','AMWAY','APFT','APOLLO','ASB','ASIABRN','ASIAFLE','ATLAN','AVI',
'BAT','BAUTO','BIOOSMO','BJFOOD','BJLAND','BJTOTO','BONIA','BRAHIMS','CAB','CAB-WA',
'CAELY','CAELY-WA','CAMRES','CARING','CARLSBG','CCB','CCK','CCK-WA','CHEETAH','CIHLDG',
'CNI','CNOUHUA','COCOLND','CSCENIC','CSL','CWG','DBE','DBE-WB','DEGEM','DKSH',
'DLADY','DRBHCOM','EASTLND','EIG','EKA','EMICO','ENGKAH','EURO','EUROSP','F%26N',
'FCW','FIAMMA','FIHB','FIHB-PA','FIHB-PB','FPI','G3','G3-WA','GCB','GCE',
'GENM','GENTING','GETS','GREENYB','HAIO','HARISON','HBGLOB','HEIM','HLIND','HOMERIZ',
'HOMERIZ-WA','HUPSENG','HWATAI','IQGROUP','JADI','JAYCORP','JERASIA','JOHOTIN','KAMDAR','KAREX',
'KAWAN','KFM','KHEESAN','KHIND','KPOWER','KSTAR','KSTAR-WA','KTB','LANDMRK','LATITUD',
'LAYHONG','LAYHONG-WA','LEESK','LIIHEN','LONBISC','LONBISC-WA','LTKM','MAGNI','MAGNUM','MARCO',
'MAXWELL','MAXWELL-WA','MBG','MBMR','MESB','MESB-WA','MFLOUR','MFLOUR-WC','MILUX','MINDA',
'MSM','MSPORTS','MUIIND','MULPHA','MYNEWS','NESTLE','NHFATT','NICE','NICE-WB','NIHSIN',
'NTPM','OCB','OCNCASH','OFI','OLYMPIA','ORIENT','OWG','OWG-WA','PADINI','PANAMY',
'PAOS','PAOS-WA','PARAGON','PARKSON','PCCS','PCCS-WA','PELIKAN','PENSONI','PENSONI-WB','PERMAJU',
'PETDAG','PMCORP','PMHLDG','POHKONG','POHUAT','POHUAT-WB','PPB','PRG','PRG-WA','PRLEXUS',
'PRLEXUS-WA','PTRANS','PTRANS-WA','PWF','PWF-WA','PWROOT','PWROOT-WA','QL','REX','RGB',
'RHONEMA','SALUTE','SANBUMI','SAUDEE','SAUDEE-WA','SEG','SEM','SERNKOU','SERNKOU-WA','SHANG',
'SHH','SIGN','SIGN-WA','SIME','SINOTOP','SMCAP','SMCAP-WC','SNC','SOLID','SOLID-WA',
'SPRITZER','SUIWAH','SWSCAP','SWSCAP-WB','SYF','SYF-WB','TAFI','TCHONG','TECGUAN','TEKSENG',
'TEKSENG-WA','TEOSENG','TEOSENG-WA','TGL','TOMEI','TPC','TPC-WA','UMW','UPA','VERTICE',
'VERTICE-WA','WANGZNG','WARISAN','XDL','XDL-WD','XIANLNG','XINQUAN','XINQUAN-WA','XINQUAN-WB','YEELEE',
'YOCB','ZHULIAN','ADVCON','AZRB','AZRB-WA','BENALEC','BPURI','BREM','CRESBLD','DKLS',
'ECONBHD','ECONBHD-WA','EKOVEST','EKOVEST-WB','FAJAR','FAJAR-WB','GADANG','GADANG-WB','GAMUDA','GAMUDA-WE',
'GBGAQRS','GBGAQRS-WB','GKENT','HOHUP','HSL','IJM','IKHMAS','INTA','IREKA','IREKA-WB',
'JAKS','JAKS-WB','KERJAYA','KERJAYA-WB','KIMLUN','KIMLUN-WA','LEBTECH','MELATI','MERCURY','MERGE',
'MGB','MGB-WA','MITRA','MITRA-WD','MITRA-WE','MTDACPI','MUDAJYA','MUHIBAH','OCR','OCR-PA',
'OCR-WC','OCR-WD','PEB','PESONA','PESONA-WC','PRTASCO','PRTASCO-WA','PSIPTEK','PSIPTEK-WA','PTARAS')


# Defining AppCrawler class that use to crawl stock data from the hardcoded weblink.
class AppCrawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.apps = []

    def crawl(self):
        self.get_app_from_link(self.starting_url)
        return

    def get_app_from_link(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)

# Crawled data            
        # Company name 
        stock_name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]
        
        # Company stock code in KLSE
        stock_code = tree.xpath('//li[@class="f14"]/text()')[1]
        
        # Stock open price of the day
        open_price = tree.xpath('//td[@id="slcontent_0_ileft_0_opentext"]/text()')[0]
        
        # Stock high price of the day
        high_price = tree.xpath('//td[@id="slcontent_0_ileft_0_hightext"]/text()')[0]
        
        # Stock low price of the day
        low_price = tree.xpath('//td[@id="slcontent_0_ileft_0_lowtext"]/text()')[0]
        
        # Stock last price of the day
        last_price = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
        
        # Stock price change
        price_change_up = tree.xpath('//td[@id="slcontent_0_ileft_0_chgtext"] //span[@class="quote_up"]/text()')
        price_change_down = tree.xpath('//td[@id="slcontent_0_ileft_0_chgtext"] //span[@class="quote_down"]/text()')
        
        if len(price_change_up) == 0 and len(price_change_down) != 0:
            price_change = price_change_down[0]
        
        elif len(price_change_down) == 0 and len(price_change_up) != 0:
            price_change = price_change_up[0]
        
        elif len(price_change_down) == 0 and len(price_change_up) == 0:
            price_change = 0

        # Stock price change in percentage
        price_change_percent = tree.xpath('//td[@id="slcontent_0_ileft_0_chgpercenttrext"]/text()')[0]
        
        # Stock volume
        stock_volume = tree.xpath('//td[@id="slcontent_0_ileft_0_voltext"]/text()')[0]
        
        # Buy volume
        buy_volume = tree.xpath('//td[@id="slcontent_0_ileft_0_buyvol"]/text()')[0]

        # Sell volume
        sell_volume = tree.xpath('//td[@id="slcontent_0_ileft_0_sellvol"]/text()')[0]


# Defining database connection that use to store crawled stock data together with the date of the stock price         
        connection = pymysql.connect(host='localhost', user='root', password='', db='KLSE')
        cursor = connection.cursor()
        
        current_Date = datetime.now()
        formatted_date = current_Date.strftime('%Y-%m-%d %H:%M:%S')
        #formatted_date = current_Date.strftime('%Y-%m-%d')
        
        insert_to_database = (stock_name, stock_code[3:], open_price, high_price, low_price, last_price, price_change, price_change_percent, stock_volume, buy_volume, sell_volume, formatted_date)
        
        sql = 'INSERT INTO Stock (stock_name, stock_code, open_price, high_price, low_price, last_price, price_change, price_change_percent, stock_volume, buy_volume, sell_volume, date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, insert_to_database)	
        connection.commit()
         
        print('Company Name: ' + str(stock_name))
        print('Stock Code: ' + str(stock_code[3:]))
        print('Open Price: ' + str(open_price))
        print('High Price: ' + str(high_price))
        print('Low Price: ' + str(low_price))
        print('Last Price: ' + str(last_price))
        print('Price Change: ' + str(price_change))
        print('Price Change in %: ' + str(price_change_percent))
        print('Stock Volume: ' + str(stock_volume))
        print('Buy / Volume: ' + str(buy_volume))
        print('Sell / Volume: ' + str(sell_volume))
        print("Records were saved to database successfully\n\n")
	
        return


# Crawling of stock data for the companies that set in the listing 
# The crawling is based on the hardcoded weblink and AppCrawler class
for company in companies:
    weblink = 'https://www.thestar.com.my/business/marketwatch/stocks/?qcounter=' + str(company)
    crawler = AppCrawler(weblink, 0)
    crawler.crawl()
    
# End of the code