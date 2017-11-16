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
moviefilename = 'movie_list_'+time.strftime('%Y%m%d')+'.csv' #此檔會依日期生成，存放當日爬取的電影網頁名單，以CSV存放
seedlistfilename_csv = 'seed_list_'+time.strftime('%Y%m%d')+'.csv' #此檔會依日期生成，存放當日爬取的電影網頁和種子名單，以CSV存放
seedlistfilename_txt = 'seed_list_'+time.strftime('%Y%m%d')+'.txt' #此檔會依日期生成，存放當日爬取的種子名單，以TXT存放
seednewfilename = 'seed_list_new_'+time.strftime('%Y%m%d')+'.txt' #此檔會依日期生成，存放當日爬取的未寫入種子庫的種子名單，以TXT存放

for i in range(1, pages+1):
    res = get('http://www.dysfz.cc/' + str(i)+ '?o=2')
    soup = BeautifulSoup(res.text, 'html.parser')

    for title in soup.select('[target=_blank]'):
        url = str(title.get('href'))

        if 'movie' in url[10:]: #過濾出我們想要的連結
            #print url
            with open(moviefilename, 'a') as movielist: #將電影網頁連結寫入檔案
                movielist.write(url + '\n')
                movielist.close()


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


#將當日爬取到的種子列表與種子庫分別轉存list，作為帶毀轉換成set使用
seed_a = [line.strip() for line in open(seedlistfilename_txt)]
seed_lib = [line.strip() for line in open('seed_list_lib.txt')]
open('seed_list_lib.txt').close()

"""
利用集合的差集的概念，將當日爬取到的種子與種子庫做比較，挑選出還未寫入種子庫的種子
再將得到的結果分別存入新檔和回寫到種子庫
"""

set_a = set(seed_a) #將list轉換成set
set_lib = set(seed_lib)
set_new = set_a - set_lib #得到還未寫入種子庫的種子

seed_new = list(set_new) #set轉換成list，寫入檔案使用

#seednewfilename = 'seed_list_new_'+time.strftime('%Y%m%d')+'.txt'
for list_new in seed_new:
    with open(seednewfilename, 'a') as seedfilenew: #將未放入種子庫的種子寫入當日新種子檔
        seedfilenew.write(list_new + '\n')
        seedfilenew.close()

for list_new in seed_new:
    with open('seed_list_lib.txt', 'a') as seedfilelib: #將未放入種子庫的種子寫入種子庫
        seedfilelib.write(list_new + '\n')
        seedfilelib.close()
