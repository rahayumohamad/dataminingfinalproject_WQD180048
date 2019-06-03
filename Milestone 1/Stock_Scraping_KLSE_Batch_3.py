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

# Batch 3

# Importing related Python modules/packages.
from lxml import html
from datetime import datetime
import requests
import pymysql


# List of companies that listed in KLSE Main Board.
companies = (
'PUNCAK','SENDAI','SUNCON','SYCAL','TRC','TSRCAP','TSRCAP-WB','VIZIONE','VIZIONE-WC','WCEHB',
'WCT','WCT-WE','ZECON','ZELAN','AHP','ALAQAR','ALSREIT','AMFIRST','ARREIT','ATRIUM',
'AXREIT','CMMT','HEKTAR','IGBREIT','KIPREIT','KLCC','MQREIT','PAVREIT','SUNREIT','TWRREIT',
'UOAREIT','YTLREIT','ABLEGRP','ADVPKG','AEM','AEM-WA','AFUJIYA','AISB','AJIYA','AJIYA-WA',
'ALCOM','ANALABS','ANCOM','ANNJOO','ANNJOO-PA','ANZO','ANZO-WA','ANZO-WB','ANZO-WC','APB',
'APM','ARANK','ASTINO','ATAIMS','ATTA','ATTA-PA','ATTA-WB','ATTA-WC','ATURMJU','ATURMJU-PA',
'AWC','AWC-WA','AYS','BIG','BINTAI','BINTAI-WA','BJCORP','BJCORP-WB','BJCORP-WC','BOILERM',
'BORNOIL','BORNOIL-WC','BORNOIL-WD','BOXPAK','BOXPAK-WA','BPPLAS','BRIGHT','BSLCORP','BSTEAD','BTM',
'BTM-WA','BTM-WB','CANONE','CAP','CBIP','CBIP-WA','CCM','CEPCO','CFM','CHINHIN',
'CHINWEL','CHOOBEE','CHUAN','CICB','CME','CME-WA','CMSB','CNASIA','COMCORP','COMFORT',
'COMPUGT','CSCSTEL','CYL','CYMAO','CYPARK','DAIBOCI','DAIBOCI-WB','DANCO','DANCO-WA','DESTINI',
'DNONCE','DNONCE-WA','DOLMITE','DOLPHIN','DOLPHIN-WA','DOMINAN','DOMINAN-WA','DUFU','EDGENTA','EFFICEN',
'EG','EG-PA','EG-WC','EITA','EKSONS','EMETALL','ENGTEX','EPMB','EVERGRN','FACBIND',
'FAVCO','FIBON','FIMACOR','FITTERS','FITTERS-WB','FLBHD','FPGROUP','GESHEN','GLOTEC','GLOTEC-WA',
'GOODWAY','GPA','GPA-WA','GPHAROS','GUH','HALEX','HAPSENG','HEVEA','HEVEA-WB','HEXZA',
'HIAPTEK','HIAPTEK-WB','HIGHTEC','HIL','HIL-WB','HOKHENG','HSSEB','HSSEB-WA','HUMEIND','HWGB',
'HWGB-WD','IMASPRO','IPMUDA','IRETEX','IRETEX-WA','JASKITA','JCBNEXT','JETSON','JMR','KARYON',
'KEINHIN','KFIMA','KGB','KGB-WA','KIALIM','KIANJOO','KIMHIN','KINSTEL','KKB','KNUSFOR',
'KOBAY','KOMARK','KOMARK-WB','KPSCB','KSENG','KSSC','KUB','KYM','LAFMSIA','LBALUM',
'LCTITAN','LEONFB','LEWEKO','LEWEKO-WB','LFECORP','LIONFIB','LIONIND','LSTEEL','LUSTER','LUSTER-WA',
'LUSTER-WB','LUXCHEM','LYSAGHT','MASTEEL','MASTER','MBL','MBL-WA','MCEHLDG','MELEWAR','MELEWAR-WB',
'MENTIGA','METROD','MIECO','MINETEC','MINETEC-WA','MINHO','MINHO-WC','MSC','MTRONIC','MUDA',
'MYCRON','MYCRON-WA','NGGB','NGGB-WA','NWP','NYLEX','OKA','ORNA','PA','PA-WB',
'PANSAR','PANSAR-WA','PANTECH','PANTECH-WA','PANTECH-WB','PCHEM','PECCA','PERSTIM','PESTECH','PGLOBE',
'PGLOBE-WA','PICORP','PIE','PJBUMI','PJBUMI-WA','PMBTECH','PMBTECH-WA','PMETAL','PMETAL-WC','PNEPCB',
'POLY','PPHB','PRESTAR','PWORTH','QUALITY','RALCO','RALCO-WB','RESINTC','RGTBHD','RGTBHD-WB',
'ROHAS','RUBEREX','SAB','SAM','SAMCHEM','SAPIND','SCABLE','SCGM','SCGM-WA','SCIB',
'SCICOM','SCIENTX','SCNWOLF','SEACERA','SEACERA-WB','SEACERA-WC','SEB','SGB','SGB-PA','SGB-WA',
'SIGGAS','SKBSHUT','SKPRES','SLP','SMISCOR','SSTEEL','STONE','STONE-WA','SUBUR','SUCCESS',
'SUNWAY','SUNWAY-WB','SUPERLN','TASEK','TASEK-PA','TAWIN','TECHBND','TEXCHEM','TGUAN','TGUAN-WA')


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