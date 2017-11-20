#! python 2.7
#encoding: utf-8

"""
這是爬取網站 http://www.dysfz.cc/ 裡面關鍵字搜尋之後的爬蟲，這裡是用"2017秋季日劇"為關鍵字
一樣是專門用以抓取裡面提供的磁力與驢子的鏈結
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
import crawler_dydy_v2

reload(sys)
sys.setdefaultencoding('utf8') #宣告預設的encoding是utf-8


crewler_url = 'http://www.dysfz.cc/key/2017%E7%A7%8B%E5%AD%A3%E6%97%A5%E5%89%A7/' #關鍵字搜尋頁面網址，關鍵字是: 2017秋季日剧 (簡體字)
moviefilename = 'jpdrama_list_'+time.strftime('%Y%m%d')+'.csv' #此檔會依日期生成，存放當日爬取的電影網頁名單，以CSV存放
seedlistfilename_csv = 'jpdrama_seed_list_'+time.strftime('%Y%m%d')+'.csv' #此檔會依日期生成，存放當日爬取的電影網頁和種子名單，以CSV存放
seedlistfilename_txt = 'jpdrama_seed_list_'+time.strftime('%Y%m%d')+'.txt' #此檔會依日期生成，存放當日爬取的種子名單，以TXT存放
seednewfilename = 'jpdrama_seed_list_new_'+time.strftime('%Y%m%d')+'.txt' #此檔會依日期生成，存放當日爬取的未寫入種子庫的種子名單，以TXT存放
seedlibfilename = 'seed_list_lib.txt' #存放爬取過的種子名單。重要! 不可隨意更改檔名與內容。

pages = crawler_dydy_v2.key_page(crewler_url) #呼叫key_page來幫忙抓取頁數

"""
以下的還是利用原本搜尋電影的code來搜尋日劇(或者你想要的關鍵字)，檔案名稱就依個人喜好修改
moviefilename 這檔案是給程式作參考使用，會利用裡面存取的名單一次爬取網頁裡面所有種子連結
seedlistfilename_csv 這檔案是給使用者比對使用，會將網頁與網頁裡內含的種子寫在檔案裡面
seedlistfilename_txt 存放當日爬取的種子名單，程式參考用。
seednewfilename 存放當日爬取的未寫入種子庫的種子名單，可直接利用於下載流程。
"""

crawler_dydy_v2.make_movielist(pages, crewler_url, moviefilename)
crawler_dydy_v2.make_seedlist(moviefilename, seedlistfilename_csv, seedlistfilename_txt)
crawler_dydy_v2.defineseedlist(seedlistfilename_txt, seedlibfilename, seednewfilename)