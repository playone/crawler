#! python2.7
#encoding: utf-8

"""
這是專門以人人裡面的我的收藏為主的爬蟲
人人有提供眾多的下載方式，在這裡專門以磁力與驢子為主要的爬取重點
第一次使用前須先創造一個 seed_list_lib.txt 做為種子庫使用 (與程式檔存放在同一個folder)
此爬蟲一日使用一次，假如要當日連續使用，請每次執行時，先移除 folder "list" 裡面所有的檔案
"""

import requests
from bs4 import BeautifulSoup
import time
import sys
import progressbar

reload(sys)
sys.setdefaultencoding('utf-8')

yy_favor_url = 'http://www.zimuzu.tv/user/fav' #人人我的收藏的網址
favorlistfilename = 'yylist\yyfavor_list_'+time.strftime('%Y%m%d')+'.txt' #收藏裡的影片資料連結清單，給程式做參照用
favortitlefilename = 'yylist\yyfavor_title_list_'+time.strftime('%Y%m%d')+'.txt' #影片裡的片名清單，給使用者作參考用
userseedlistfilename = 'yylist\user_seedlist_'+time.strftime('%Y%m%d')+'.txt' #種子清單，提供給使用者作參考用
usered2klistfilename = 'yylist\user_ed2klist_'+time.strftime('%Y%m%d')+'.txt' #eDonkey種子清單，提供給使用者作參考用
usermagnetlistfilename = 'yylist\user_magnetlist_'+time.strftime('%Y%m%d')+'.txt' #磁力連結清單，提供給使用者作參考用
seedlistfilename = 'yylist\seedlist_'+time.strftime('%Y%m%d')+'.txt' #程式執行當日爬取到的種子清單，給程式做比對用
newseedlist_magnetfilename = 'yylist\yynew_magnet_seedlist_'+time.strftime('%Y%m%d')+'.txt' #比對完成之後，還未使用過的種子清單，可提供給下載程式做使用
newseedlist_edonkeyfilename = 'yylist\yynew_edonkey_seedlist_'+time.strftime('%Y%m%d')+'.txt' #比對完成之後，還未使用過的種子清單，可提供給下載程式做使用
seedlibfilename = 'seed_list_lib.txt' #存放爬取過的種子名單。重要! 不可隨意更改檔名與內容。
raw_cookie = 'UM_distinctid=160018c89c412a-08d5769eeec2be8-4c322f7c-144000-160018c89c5119; CNZZDATA1254180690=816159804-1511853929-http%253A%252F%252Fwww.zimuzu.tv%252F%7C1511853929; help_yyets=1; PHPSESSID=57qeueg1lar3vov8uc7vq3mcq5; GINFO=uid%3D4852682%26nickname%3Dquicktimes%26group_id%3D1%26avatar_t%3Dhttp%3A%2F%2Ftu.zmzjstu.com%2Fftp%2Favatar%2Ff_noavatar_t.gif%26main_group_id%3D0%26common_group_id%3D56; GKEY=70aa7187b83ac08672bed51359ad785d'
#raw_cookie是以我的帳號所生成的人人的登入cookies, 用以維持requests登陸網頁做使用


def make_cookie(raw_cookie = raw_cookie):
    """
    此方法是將提供的cookies字典化，以利於requests使用，raw_cookie需在利用此方法前先確認是否可用
    :param raw_cookie:  使用者所提供的人人登入cookies
    :return: 字典化之後的cookies
    """
    cookies = {}
    for line in raw_cookie.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value

    return cookies #Type是 dictionary

def site_status(yy_favor_url = yy_favor_url, cookies = make_cookie()):
    """
    此方法是用來判斷網站狀態
    :param yy_favor_url: 人人我的收藏的網址
    :param cookies: 人人的登入cookies
    :return: none
    """
    res = requests.get(yy_favor_url, cookies=cookies)
    soup = BeautifulSoup(res.text, 'html.parser')
    for title in soup.select('[name=description]'): #原本想用網頁回傳的狀態碼判斷，但無法正確判斷網頁狀態。因此後來選用觀察網頁的特性，利用網頁的敘述來判斷狀態。
        key = title.get('content')

    if 'ZiMuZu' not in key:
        sys.exit('Site link is failed, please check the status.')
    else:
        print 'Site status is good.'


def define_pages(yy_favor_url = yy_favor_url, cookies = make_cookie()):
    """
    此方法是用來判別使用者在人人收藏的頁數，以利於後面爬取流程做使用
    :param yy_favor_url: 人人我的收藏的網址
    :param cookies: 人人的登入cookies
    :return: 判別出來的頁數
    """
    print 'Start to define pages count'
    res = requests.get(yy_favor_url, cookies=cookies)
    soup = BeautifulSoup(res.text, 'html.parser')
    #site_status(yy_favor_url, cookies)

    for block in soup.select('a'):
        key = block.text
        if '...' in key:
            keytemp = key.split('.')
            pages = keytemp[-1] #pages 的type是string
    print 'Pages define complete.'
    return pages


def make_favor_list(pages = define_pages(), yy_favor_url = yy_favor_url, favorlistfilename = favorlistfilename, favortitlefilename= favortitlefilename, cookies = make_cookie()):
    """
    此方法是用來爬取產生收藏頁面資料清單，會產生favorlistfilename 和favortitlefilename 兩個檔案，檔名需在使用此方法前定義好
    :param pages: 人人收藏頁的頁數
    :param yy_favor_url: 人人我的收藏的網址
    :param favorlistfilename: 收藏裡的影片資料連結清單，給程式做參照用
    :param favortitlefilename: 影片裡的片名清單，給使用者作參考用
    :param cookies: 人人的登入cookies
    :return: none
    """

    print 'Start to crawl urls in favor list'
    widgets = [' [', progressbar.Timer(), '] ', progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=int(pages))
    for page in range(1, int(pages)+1):
        res = requests.get(yy_favor_url+'?page='+str(page)+'&type=all', cookies=cookies)
        soup = BeautifulSoup(res.text, 'html.parser')
        for block in soup.select('strong'):
            for i in block.select('a'):
                url = 'http://www.zimuzu.tv'+i.get('href')
                res_s = requests.get(url, cookies=cookies)
                soup2 = BeautifulSoup(res_s.text, 'html.parser')
                for block2 in soup2.select('a.f3'):
                    source_link = block2.get('href')
                    if '/resource/list/' in source_link: #這link被隱藏，利用爬蟲將其爬取出來
                        with open(favorlistfilename, 'a') as favor:
                            favor.write('http://www.zimuzu.tv'+source_link+'\n')
                            favor.close()
        time.sleep(0.1)
        bar.update(page)
        #print 'Page'+str(page)+' is completed'
            #print block.text
            #with open(favortitlefilename, 'a') as title:
                #title.write(block.text.encode('utf-8', 'ignore')+'\n')
                #title.close()
    print '\n'+'Crawl urls complete.'


def make_seedlist(favorlistfilename = favorlistfilename, userseedlistfilename = userseedlistfilename, seedlistfilename = seedlistfilename, usered2klistfilename = usered2klistfilename, usermagnetlistfilename = usermagnetlistfilename, cookies = make_cookie()):
    """
    此方法用來爬取產生收藏網頁內的種子連結，會產生userseedlistfilename, usered2klistfilename, usermagnetlistfilename, usermagnetlistfilename ，檔名需在使用此方法前定義好
    :param favorlistfilename: 收藏裡的影片資料連結清單，在此方法做參照用
    :param userseedlistfilename: 種子清單，提供給使用者作參考用
    :param seedlistfilename: 程式執行當日爬取到的種子清單，給程式做比對用
    :param usered2klistfilename: eDonkey種子清單，提供給使用者作參考用
    :param usermagnetlistfilename: 磁力連結清單，提供給使用者作參考用
    :param cookies: 人人的登入cookies
    :return: none
    """
    favorlist = [line.strip() for line in open(favorlistfilename)] #將爬取的種子列表轉成list
    open(favorlistfilename).close()
    listcount = len(favorlist)
    i=0
    widgets = [' [', progressbar.Timer(), '] ', progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=listcount)
    print 'Start to crawl link and make list.'
    for list in favorlist:
        res = requests.get(list, cookies=cookies)
        soup = BeautifulSoup(res.text, 'html.parser')
        i=i+1
        #print '------------------------------------------'
        #print soup.title.text
        #print list
        with open(userseedlistfilename, 'a') as seedlist: #開啟檔案，假如檔案不存在則新增檔案
            seedlist.write('----------------------' + '\n' + list + '\n' + soup.title.text + '\n')
            seedlist.close()
        with open(usered2klistfilename, 'a') as seedlist: #開啟檔案，假如檔案不存在則新增檔案
            seedlist.write('----------------------' + '\n' + list + '\n' + soup.title.text + '\n')
            seedlist.close()
        with open(usermagnetlistfilename, 'a') as seedlist: #開啟檔案，假如檔案不存在則新增檔案
            seedlist.write('----------------------' + '\n' + list + '\n' + soup.title.text + '\n')
            seedlist.close()

        """
        以下會將爬取到的種子連結做分類，人人有提供許多下載檔案種類和下載連結種類
        在此則選取MP4和HR-HDTV這兩種檔案格式，選取eDonkey和磁力這兩種下載方法
        """
        #print '+++++++MP4+++++++'
        with open(userseedlistfilename, 'a') as seedlist:
            seedlist.write('+++++++MP4+++++++' + '\n')
            seedlist.close()
        with open(usered2klistfilename, 'a') as seedlist:
            seedlist.write('+++++++MP4+++++++' + '\n')
            seedlist.close()
        with open(usermagnetlistfilename, 'a') as seedlist:
            seedlist.write('+++++++MP4+++++++' + '\n')
            seedlist.close()
        for block1 in soup.select('[format=MP4]'):
            for block2 in block1.select('div.fr'):
                for block3 in block2.select('[type=ed2k]'):
                    url = str(block3.get('href'))
                    #print url
                    with open(userseedlistfilename, 'a') as seedlist:
                        seedlist.write(url+'\n')
                        seedlist.close()
                    with open(seedlistfilename, 'a') as seedlist:
                        seedlist.write(url+'\n')
                        seedlist.close()
                    with open(usered2klistfilename, 'a') as seedlist:
                        seedlist.write(url+'\n')
                        seedlist.close()

                for block3 in block2.select('[type=magnet]'):
                    url = str(block3.get('href'))
                    #print url
                    with open(userseedlistfilename, 'a') as seedlist:
                        seedlist.write(url+'\n')
                        seedlist.close()
                    with open(seedlistfilename, 'a') as seedlist:
                        seedlist.write(url+'\n')
                        seedlist.close()
                    with open(usermagnetlistfilename, 'a') as seedlist:
                        seedlist.write(url+'\n')
                        seedlist.close()

        #print '+++++++HR-HDTV++++++'
        with open(userseedlistfilename, 'a') as seedlist:
            seedlist.write('+++++++HR-HDTV++++++' + '\n')
            seedlist.close()
        with open(usered2klistfilename, 'a') as seedlist:
            seedlist.write('+++++++HR-HDTV++++++' + '\n')
            seedlist.close()
        with open(usermagnetlistfilename, 'a') as seedlist:
            seedlist.write('+++++++HR-HDTV++++++' + '\n')
            seedlist.close()

        for block5 in soup.select('[format=HR-HDTV]'):
            for block6 in block5.select('div.fr'):
                for block7 in block6.select('[type=ed2k]'):
                    url2 = str(block7.get('href'))
                    #print url2
                    with open(userseedlistfilename, 'a') as seedlist:
                        seedlist.write(url2+'\n')
                        seedlist.close()
                    with open(seedlistfilename, 'a') as seedlist:
                        seedlist.write(url2 + '\n')
                        seedlist.close()
                    with open(usered2klistfilename, 'a') as seedlist:
                        seedlist.write(url2 + '\n')
                        seedlist.close()

                for block7 in block6.select('[type=magnet]'):
                    url2 = str(block7.get('href'))
                    #print url2
                    with open(userseedlistfilename, 'a') as seedlist:
                        seedlist.write(url2 + '\n')
                        seedlist.close()
                    with open(seedlistfilename, 'a') as seedlist:
                        seedlist.write(url2 + '\n')
                        seedlist.close()
                    with open(usermagnetlistfilename, 'a') as seedlist:
                        seedlist.write(url2 + '\n')
                        seedlist.close()
        time.sleep(0.1)
        bar.update(i)
    print '\n'+'Link crawling complete.'


def defineseedlist(seedlistfilename = seedlistfilename, seedlibfilename = seedlibfilename, newseedlist_magnetfilename = newseedlist_magnetfilename, newseedlist_edonkeyfilename = newseedlist_edonkeyfilename):
    """
    此方法會挑選出還未使用過的種子連結，並將之寫存在seednewfilename和回存到seedlibfilename。seednewfilename可利用於之後的下載流程.
    :param seedlistfilename: 此txt檔存放爬取到的所有種子連結。在此方法被拿來比較參照用。
    :param seedlibfilename: 此txt檔是種子庫，存放所有已使用過的種子連結。將會被用於和seedlistfilename_txt比較，挑選出還未使用過的種子連結。
    :param newseedlistfilename: 此txt檔存放還未使用的種子連結。會於之後的下載流程做使用。
    :return: none
    """
    print 'Start to define link.'
    seed_a = [line.strip() for line in open(seedlistfilename)]
    open(seedlistfilename).close()
    seed_lib = [line.strip() for line in open(seedlibfilename)]
    open(seedlibfilename).close()

    set_a = set(seed_a) #將list轉換成set
    set_lib = set(seed_lib)
    set_new = set_a - set_lib #得到還未寫入種子庫的種子

    seed_new = list(set_new) #set轉換成list，寫入檔案使用

    for list_new in seed_new:
        if 'magnet:' in list_new:
            with open(newseedlist_magnetfilename, 'a') as seedfilenew: #將未放入種子庫的種子寫入當日新種子檔
                seedfilenew.write(list_new + '\n')
                seedfilenew.close()
        if 'ed2k://' in list_new:
            with open(newseedlist_edonkeyfilename, 'a') as seedfilenew2: #將未放入種子庫的種子寫入當日新種子檔
                seedfilenew2.write(list_new + '\n')
                seedfilenew2.close()

    for list_new in seed_new:
        with open(seedlibfilename, 'a') as seedfilelib: #將未放入種子庫的種子寫入種子庫
            seedfilelib.write(list_new + '\n')
            seedfilelib.close()
    print 'Link define complete.'


if __name__ == '__main__':
    make_cookie()
    site_status()
    define_pages()
    make_favor_list()
    make_seedlist()
    defineseedlist()

