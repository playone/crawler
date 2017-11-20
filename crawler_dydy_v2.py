#! python 2.7
#encoding: utf-8

"""
這是爬取網站 http://www.dysfz.cc/ 的爬蟲
是專門用以抓取裡面提供的磁力與驢子的鏈結
第一次使用前須先創造一個 seed_list_lib.txt 做為種子庫使用 (與程式檔存放在同一個folder)
此網頁是簡體中文，Windows的Command line因為預設的編碼是cp950，所以會顯示亂碼，
解決方法是換enoding為utf-8 ，指令是: chcp 65001，就可以正常顯示文字(Linux 則是終端機的預設編碼就是utf-8，所以應該不會有這問題)
(PS. 我還沒試過解決方法，所以有興趣的試看看的人可以試看看結果如何)
此爬蟲一日使用一次，假如要當日連續使用，請每次執行時，先移除 movie_list_xxxx.csv, seed_list_xxxxx.csv, seed_list_xxxxx.txt, seed_list_new_xxxxx.txt,
"""

from requests import *
from bs4 import BeautifulSoup
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8') #宣告預設的encoding是utf-8

pages=10 #爬取 10頁
crewler_url = 'http://www.dysfz.cc/'
moviefilename = 'movie_list_'+time.strftime('%Y%m%d')+'.csv' #此檔會依日期生成，存放當日爬取的電影網頁名單，以CSV存放
seedlistfilename_csv = 'seed_list_'+time.strftime('%Y%m%d')+'.csv' #此檔會依日期生成，存放當日爬取的電影網頁和種子名單，以CSV存放
seedlistfilename_txt = 'seed_list_'+time.strftime('%Y%m%d')+'.txt' #此檔會依日期生成，存放當日爬取的種子名單，以TXT存放
seednewfilename = 'seed_list_new_'+time.strftime('%Y%m%d')+'.txt' #此檔會依日期生成，存放當日爬取的未寫入種子庫的種子名單，以TXT存放
seedlibfilename = 'seed_list_lib.txt' #存放爬取過的種子名單。重要! 不可隨意更改檔名與內容。
"""
moviefilename 這檔案是給程式作參考使用，會利用裡面存取的名單一次爬取網頁裡面所有種子連結
seedlistfilename_csv 這檔案是給使用者比對使用，會將網頁與網頁裡內含的種子寫在檔案裡面
seedlistfilename_txt 存放當日爬取的種子名單，程式參考用。
seednewfilename 存放當日爬取的未寫入種子庫的種子名單，可直接利用於下載流程。
"""


def make_movielist(pages = pages, crewler_url = crewler_url, moviefilename = moviefilename):
    """
    以pages為爬取範圍，在範圍內爬取可用的電影網頁連結。會產生一個檔案moviefilename，檔名要在使用此方法前定義好
    :param pages: 定義想爬取的網頁頁數。在使用此方法前自行定義，或利用key_page()所得到的值。
    :param crewler_url: 定義爬取的網址，需在使用此方法前定義好。
    :param moviefilename: 定義檔名。存放爬取到的電影網址的檔名。檔名需在使用此方法前定義好。
    :return: none
    """
    for i in range(1, pages+1):
        res = get(crewler_url + str(i) + '?o=2')
        soup = BeautifulSoup(res.text, 'html.parser')

        for title in soup.select('[target=_blank]'):
            url = str(title.get('href'))

            if 'movie' in url[10:]: #過濾出我們想要的連結
                #print url
                with open(moviefilename, 'a') as movielist: #將電影網頁連結寫入檔案
                    movielist.write(url + '\n')
                    movielist.close()

def make_seedlist(moviefilename = moviefilename, seedlistfilename_csv = seedlistfilename_csv, seedlistfilename_txt = seedlistfilename_txt):
    """
    爬取電影連結裡每個可用的seed link，會產生兩個檔案，seedlistfilename_csv和seedlistfilename_txt。檔名需在使用此方法前定義好
    :param moviefilename: 存放爬取到的電影網址的檔名，在這方法裡會被用來當作爬取的參考。
    :param seedlistfilename_csv: 定義檔名。此csv檔會存放爬取到的電影網址和種子鏈結，可以讓使用者作參照用。檔名需在使用此方法前定義好。
    :param seedlistfilename_txt: 定義檔名。此txt檔存放爬取到的所有種子連結。檔名需在使用此方法前定義好。
    :return: none
    """
    movie_a = [line.strip() for line in open(moviefilename)] #將連結檔案內容轉存list，提供給爬取種子使用

    for li in movie_a:
        res_movie = get(li)
        soup_movie = BeautifulSoup(res_movie.text, 'html.parser')
        print '-----------------------'
        print li
        with open(seedlistfilename_csv, 'a') as seedlist2:
            seedlist2.write('----------------' + '\n' + li + '\n' )
            seedlist2.close()
        for title_movie in soup_movie.select('[target=_blank]'):
            seed_link = str(title_movie.get('href'))

            if 'ed2k://' in seed_link: #爬取edonkey
                #print seed_link.decode('utf8', 'ignore')
                print seed_link
                with open(seedlistfilename_txt, 'a') as seedlist: #將種子連結分別存入csv和txt
                    seedlist.write(seed_link + '\n')
                    seedlist.close()
                with open(seedlistfilename_csv, 'a') as seedlist2:
                    seedlist2.write(seed_link + '\n')
                    seedlist2.close()
            elif 'magnet:?' in seed_link: #爬取磁力連結
                print seed_link
                with open(seedlistfilename_txt, 'a') as seedlist: #將種子連結分別寫入csv和txt
                    seedlist.write(seed_link + '\n')
                    seedlist.close()
                with open(seedlistfilename_csv, 'a') as seedlist2:
                    seedlist2.write(seed_link + '\n')
                    seedlist2.close()

def defineseedlist(seedlistfilename_txt = seedlistfilename_txt, seedlibfilename = seedlibfilename, seednewfilename = seednewfilename):
    """
    此方法會挑選出還未使用過的種子連結，並將之寫存在seednewfilename和回存到seedlibfilename。seednewfilename可利用於之後的下載流程
    :param seedlistfilename_txt: 定義檔名。此txt檔存放爬取到的所有種子連結。在此方法被拿來比較參照用。
    :param seedlibfilename: 定義檔名。此txt檔是種子庫，存放所有已使用過的種子連結。將會被用於和seedlistfilename_txt比較，挑選出還未使用過的種子連結。
    :param seednewfilename: 定義檔名。此txt檔存放還未使用的種子連結。會於之後的下載流程做使用。
    :return: none
    """

    #將當日爬取到的種子列表與種子庫分別轉存list，作為轉換成set使用
    seed_a = [line.strip() for line in open(seedlistfilename_txt)]
    seed_lib = [line.strip() for line in open(seedlibfilename)]
    open(seedlibfilename).close()

    """
    利用集合的差集的概念，將當日爬取到的種子與種子庫做比較，挑選出還未寫入種子庫的種子
    再將得到的結果分別存入新檔和回寫到種子庫
    """

    set_a = set(seed_a) #將list轉換成set
    set_lib = set(seed_lib)
    set_new = set_a - set_lib #得到還未寫入種子庫的種子

    seed_new = list(set_new) #set轉換成list，寫入檔案使用

    for list_new in seed_new:
        with open(seednewfilename, 'a') as seedfilenew: #將未放入種子庫的種子寫入當日新種子檔
            seedfilenew.write(list_new + '\n')
            seedfilenew.close()

    for list_new in seed_new:
        with open(seedlibfilename, 'a') as seedfilelib: #將未放入種子庫的種子寫入種子庫
            seedfilelib.write(list_new + '\n')
            seedfilelib.close()

def key_page(crewler_url = crewler_url):
    """
    提取頁數的做法。關鍵字搜尋之後，它有一定頁數，因此用這方法來提取準確頁數，以利接下來的網頁爬蟲。
    :param crewler_url: 想要爬取的網址
    :return: pages。可在於方法make_movielist()做使用。
    """
    keyres = get(crewler_url)  #關鍵字搜尋結果網頁
    keysoup = BeautifulSoup(keyres.text, 'html.parser')

    for keytitle in keysoup.select('.last'):
        keyurl = str(keytitle.get('href'))

    keyurl = keyurl.split('/')
    temp = keyurl[-1]
    temp = temp.split('?')
    pages = int(temp[0])
    print pages
    return pages

if __name__ == '__main__':
    make_movielist()
    make_seedlist()
    defineseedlist()