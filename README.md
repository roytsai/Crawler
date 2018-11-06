# Crawler 
### 我先簡單介紹一下依爬蟲困難程度差別 :
1. 簡單的網頁內容，也就是不用經過其他步驟，也沒有js渲染。比方:https://doc.scrapy.org/en/latest/intro/tutorial.html
    * 此情況只需要透過單純的 http requests即可解決
    ~~~
    rs = requests.session()
    res = rs.get('https://doc.scrapy.org/en/latest/intro/tutorial.html', verify = False)
    soup = BeautifulSoup(res.text,'html.parser')
    ~~~
        
2. 需要透過一些步驟才能進入網站。比方:https://www.ptt.cc/bbs/Gossiping/index.html
    * 此狀況有兩種解法
        * 可單純模擬button按下去後所發出的request再發出一次
            ~~~
            payload={
                'from':'/bbs/Gossiping/index.html',
                'yes':'yes' 
            }
            rs = requests.session()
            rs.post('https://www.ptt.cc/ask/over18', data=payload)
            res = rs.get('https://doc.scrapy.org/en/latest/intro/tutorial.html', verify = False)
            soup = BeautifulSoup(res.text,'html.parser')
            ~~~
        * 進階一點可透過selenium+phantomjs，模擬執行Button點擊動作
           ~~~
            driver = webdriver.PhantomJS(".\phantomjs.exe")
            driver.get("https://www.ptt.cc/bbs/Gossiping")
            driver.find_element_by_class_name("btn-big").click()
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            ~~~
        
3. 較複雜的網站甚至會有js的渲染
    * 此狀就需要透過selenium+phantomjs解決，所得到的html response也就是被js渲染過的。
    * 備註說明: 要解決js渲染不止上述所提的方式
        * selenium+webdriver([Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads), 
                               [Firefox](https://github.com/mozilla/geckodriver/releases),
                                [Safari](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)) : 
          但缺點就是瀏覽器會跟著被開啟，所以效率差。
        ~~~
            driver = webdriver.Chrome('.\chromedriver.exe') 
            driver.get("https://tw.news.yahoo.com/foods")
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
        ~~~          
        * selenium+phantomjs ([phantomjs](http://phantomjs.org/)) : 此做法就是可以改善上述的優點，不會有瀏覽器被開啟。
         ~~~
            driver = webdriver.Chrome('.\phantomjs.exe') 
            driver.get("https://tw.news.yahoo.com/foods")
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
        ~~~           
        * scrapy/splash ([scrapy](https://docs.scrapy.org/en/latest/)) : 
          scrapy是一個crawl framework整合了爬蟲，數據處理，儲存的服務等，有這麼多優點相對來說使用門檻會稍微高一點，
          所以我會建議除非你是每天都需要爬蟲的再來考慮這個架構，不然使用上述的解法已經很夠了。
          

### 取得正確的content後 : 
1. 基本上就是用BeautifulSoup來parser html，再利用regular expression及人工觀察其規則parser出我們要的內容。
~~~
allPageURL = soup.select('.btn.wide')[1]['href']
~~~
