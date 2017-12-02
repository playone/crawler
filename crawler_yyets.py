#! python2.7
#encoding: utf-8

import requests
from bs4 import BeautifulSoup
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

yy_favor_url = 'http://www.zimuzu.tv/user/fav'
favorlistfilename = 'yylist\yyfavor_list_'+time.strftime('%Y%m%d')+'.txt'
favortitlefilename = 'yylist\yyfavor_title_list_'+time.strftime('%Y%m%d')+'.txt'
userseedlistfilename = 'yylist\user_seedlist_'+time.strftime('%Y%m%d')+'.txt'
usered2klistfilename = 'yylist\user_ed2klist_'+time.strftime('%Y%m%d')+'.txt'
usermagnetlistfilename = 'yylist\user_magnetlist_'+time.strftime('%Y%m%d')+'.txt'
seedlistfilename = 'yylist\seedlist_'+time.strftime('%Y%m%d')+'.txt'
newseedlistfilename = 'yylist\yynewseedlist_'+time.strftime('%Y%m%d')+'.txt'
seedlibfilename = 'seed_list_lib.txt' #存放爬取過的種子名單。重要! 不可隨意更改檔名與內容。
raw_cookie = 'UM_distinctid=160018c89c412a-08d5769eeec2be8-4c322f7c-144000-160018c89c5119; CNZZDATA1254180690=816159804-1511853929-http%253A%252F%252Fwww.zimuzu.tv%252F%7C1511853929; help_yyets=1; PHPSESSID=57qeueg1lar3vov8uc7vq3mcq5; GINFO=uid%3D4852682%26nickname%3Dquicktimes%26group_id%3D1%26avatar_t%3Dhttp%3A%2F%2Ftu.zmzjstu.com%2Fftp%2Favatar%2Ff_noavatar_t.gif%26main_group_id%3D0%26common_group_id%3D56; GKEY=70aa7187b83ac08672bed51359ad785d'

def make_cookie(raw_cookie = raw_cookie):
    cookies = {}
    for line in raw_cookie.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value

    return cookies

def site_status(yy_favor_url= yy_favor_url, cookies = make_cookie()):
    res = requests.get(yy_favor_url, cookies=cookies)
    soup = BeautifulSoup(res.text, 'html.parser')
    for title in soup.select('[name=description]'):
        key = title.get('content')

    if 'ZiMuZu' not in key:
        sys.exit('網站無法存取')
    else:
        print '網站可用'


def define_pages(yy_favor_url= yy_favor_url, cookies = make_cookie()):
    res = requests.get(yy_favor_url, cookies=cookies)
    soup = BeautifulSoup(res.text, 'html.parser')
    #site_status(yy_favor_url, cookies)

    for block in soup.select('a'):
        key = block.text
        if '...' in key:
            keytemp = key.split('.')
            pages = keytemp[-1] #pages 的type是string
    return pages


def make_favor_list(pages = define_pages(), yy_favor_url = yy_favor_url, favorlistfilename = favorlistfilename, favortitlefilename= favortitlefilename, cookies = make_cookie()):
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
                    if '/resource/list/' in source_link:
                        with open(favorlistfilename, 'a') as favor:
                            favor.write('http://www.zimuzu.tv'+source_link+'\n')
                            favor.close()
            #print block.text
            with open(favortitlefilename, 'a') as title:
                title.write(block.text.encode('utf-8', 'ignore')+'\n')
                title.close()


def make_seedlist(favorlistfilename = favorlistfilename, userseedlistfilename = userseedlistfilename, seedlistfilename = seedlistfilename, usered2klistfilename = usered2klistfilename, usermagnetlistfilename = usermagnetlistfilename, cookies = make_cookie()):

    favorlist = [line.strip() for line in open(favorlistfilename)]
    open(favorlistfilename).close()

    for list in favorlist:
        res = requests.get(list, cookies=cookies)
        soup = BeautifulSoup(res.text, 'html.parser')

        print '------------------------------------------'
        print soup.title.text
        print list
        with open(userseedlistfilename, 'a') as seedlist:
            seedlist.write('----------------------' + '\n' + list + '\n' + soup.title.text + '\n')
            seedlist.close()
        with open(usered2klistfilename, 'a') as seedlist:
            seedlist.write('----------------------' + '\n' + list + '\n' + soup.title.text + '\n')
            seedlist.close()
        with open(usermagnetlistfilename, 'a') as seedlist:
            seedlist.write('----------------------' + '\n' + list + '\n' + soup.title.text + '\n')
            seedlist.close()

        print '+++++++MP4+++++++'
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
                    print url
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
                    print url
                    with open(userseedlistfilename, 'a') as seedlist:
                        seedlist.write(url+'\n')
                        seedlist.close()
                    with open(seedlistfilename, 'a') as seedlist:
                        seedlist.write(url+'\n')
                        seedlist.close()
                    with open(usermagnetlistfilename, 'a') as seedlist:
                        seedlist.write(url+'\n')
                        seedlist.close()

        print '+++++++HR-HDTV++++++'
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
                    print url2
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
                    print url2
                    with open(userseedlistfilename, 'a') as seedlist:
                        seedlist.write(url2 + '\n')
                        seedlist.close()
                    with open(seedlistfilename, 'a') as seedlist:
                        seedlist.write(url2 + '\n')
                        seedlist.close()
                    with open(usermagnetlistfilename, 'a') as seedlist:
                        seedlist.write(url2 + '\n')
                        seedlist.close()
'''                 
        for block2 in soup.select('[type=magnet]'):
            url2 = block2.get('href')
            print url2
            #with open('seedlist.txt', 'a') as seedlist:
            #    seedlist.write(url2 + '\n')
            #    seedlist.close()
'''

def defineseedlist(seedlistfilename = seedlistfilename, seedlibfilename = seedlibfilename, newseedlistfilename = newseedlistfilename):

    seed_a = [line.strip() for line in open(seedlistfilename)]
    open(seedlistfilename).close()
    seed_lib = [line.strip() for line in open(seedlibfilename)]
    open(seedlibfilename).close()

    set_a = set(seed_a) #將list轉換成set
    set_lib = set(seed_lib)
    set_new = set_a - set_lib #得到還未寫入種子庫的種子

    seed_new = list(set_new) #set轉換成list，寫入檔案使用

    for list_new in seed_new:
        with open(newseedlistfilename, 'a') as seedfilenew: #將未放入種子庫的種子寫入當日新種子檔
            seedfilenew.write(list_new + '\n')
            seedfilenew.close()

    for list_new in seed_new:
        with open(seedlibfilename, 'a') as seedfilelib: #將未放入種子庫的種子寫入種子庫
            seedfilelib.write(list_new + '\n')
            seedfilelib.close()


if __name__ == '__main__':
    make_cookie()
    site_status()
    define_pages()
    make_favor_list()
    make_seedlist()
    defineseedlist()

