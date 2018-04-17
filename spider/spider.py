

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re
import time
import asyncio

payload={
    'from':'/bbs/Gossiping/index.html',
    'yes':'yes' 
}


OVER_18_URL = 'https://www.ptt.cc/ask/over18'

PTT_HOST_URL = 'https://www.ptt.cc/'
PTT_BBS_HOST_URL = PTT_HOST_URL+'bbs/'
PTT_BOARD_NAME = 'Gossiping'



def getPageNumber(content) :
    startIndex = content.find('index')
    endIndex = content.find('.html')
    pageNumber = content[startIndex + 5 : endIndex]
    return pageNumber

def showTitle(soup):
    titles = soup.find_all('a', {'href': re.compile('/bbs/Gossiping/M.*')})
    for title in titles:
        print(title)


def getAllArticleUrl(allPageNumber, limitPage):
    urllist = []
    result_urllist = []
    for index in range(allPageNumber, allPageNumber-int(limitPage), -1):

        url = PTT_BBS_HOST_URL+ PTT_BOARD_NAME +'/index'+ str(index) +'.html'
        
        res = rs.get(url, verify = False)
        soup = BeautifulSoup(res.text,'html.parser')
        for entry in soup.select('.r-ent'):
            atag = entry.select('.title')[0].find('a') 
            if(atag != None):
                url = atag['href']      
                urllist.append('https://www.ptt.cc' + url)   

        #需要反轉,因為網頁版最下面才是最新的文章
        for URL in reversed(urllist):
            yield URL

def getPushCentent(soup):
    push_content = soup.findAll(attrs={'class': 'push-content'})
    for content in push_content :
        text = content.text.replace(": ", "")
        m = re.search('[\u4e00-\u9fff]+', text)
        if m != None and len(text)>10:
            print(text)    

def extractChinese(str):
    return re.sub(r"[^\u4e00-\u9fff\n]","",str)

def getAllArticleContent(urlGenerator):

    with open('ptt.txt', 'w', encoding ='utf-8') as output:
        for index, url in enumerate(urlGenerator):
            res = rs.get(url, verify = False)
            soup = BeautifulSoup(res.text, 'html.parser')
            data = soup.select('.bbs-screen.bbs-content')[0].text
            data_line = data.splitlines()
            
            new_data = ''
            for line in data_line:
                if re.search(r"^噓|^推",line) != None:
                    line =  line[2:] 
                if re.search(r"^作者|^標題|^時間|^※",line) == None:
                    line = extractChinese(line)
                    if len(line) > 5 :
                        new_data = new_data + line +'\n'
              
            output.writelines(new_data)  
            if (index+1) % 20 == 0:
                print('已完成'+str(index+1)+'筆網址')
                
    print("結束")    
 

if __name__ == '__main__':
    

    rs = requests.session()
    rs.post(OVER_18_URL, data=payload)
    res = rs.get(PTT_BBS_HOST_URL+PTT_BOARD_NAME+'/index.html', verify = False)

    soup = BeautifulSoup(res.text,'html.parser')

    allPageURL = soup.select('.btn.wide')[1]['href']
    allPageNumber = int(getPageNumber(allPageURL)) + 1
    print("處理總頁面數 : "+str(allPageNumber))
     
    urlGenerator  = getAllArticleUrl(allPageNumber, 20)       
     
    print("開始取得文章內容 ......")
    t1 = time.time()
    getAllArticleContent(urlGenerator)
    print("total time : ", time.time() - t1)
 
