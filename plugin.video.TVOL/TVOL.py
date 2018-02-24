# -*- coding: utf-8 -*-  
# TVOL.py 
# demo 
import urllib, xbmcplugin, xbmcgui, threading, re
import requests

def rootList():
    channelList = [['电影','1'], ['美剧','2'], ['韩剧','3'], ['日剧','4']]
    for i in channelList:
        rootChannelName = i[0]
        tid = i[1]
        listitem = xbmcgui.ListItem(rootChannelName) 
        url = sys.argv[0]+'?tid='+urllib.quote_plus(tid)+'&level=1'
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, True)
    xbmcplugin.endOfDirectory(int(sys.argv[1])) 

def tvShowList(tid):
        showInfoList(tid)

def showInfoList(tid):
    pgFile = urllib.urlopen('http://www.1993s.top/list/?'+tid+'.html')
    pgData = pgFile.read()
    pgFile.close()

    showInfoAll_r = re.compile('boxlist clearfix(.+?)pagenav',re.DOTALL)
    pgNum_r = re.compile('当前第(.+?)页')
    showInfoAll = showInfoAll_r.search(pgData).group()


    pgNum = pgNum_r.search(pgData).group().replace('当前第', '').replace('页', '')

    showInfoArr_r = re.compile('<li class="listfl">(.+?)</li>',re.DOTALL)
    showInfoArr = showInfoArr_r.findall(showInfoAll)

    showInfoList=[]
    for oneInfo in showInfoArr:
        
        #获得封面图片链接imgurl
        imgUrl_r = re.compile('data-original="(.+?)"')
        imgUrl = imgUrl_r.search(oneInfo).group(0)
        imgUrl_r = re.compile('"(.+?)"')
        imgUrl = imgUrl_r.search(imgUrl).group(0).replace('"', '')
        #print(imgUrl)
        
        #获得集数duration
        if tid != '1' and '1-' not in tid:
            
            duration_r = re.compile('class="duration">(.+?)<')
            duration = duration_r.search(oneInfo).group(0)
            duration_r = re.compile('>(.+?)<')
            duration = duration_r.search(duration).group(0).replace('>', '').replace('<', '')
            #print(quality)
        else:
            duration = ''

        #获得TVShow名字name
        name_r = re.compile('class="list-name">(.+?)</p>')
        name = name_r.search(oneInfo).group(0)
        name_r = re.compile('>(.+?)<')
        name = name_r.search(name).group(0).replace('>', '').replace('<', '')

        #获得影片showID
        showID_r = re.compile('/detail/?(.+?).html')
        showID = showID_r.search(oneInfo).group(0).replace('/detail/?', '').replace('.html', '')

        listitem = xbmcgui.ListItem(name+ '   '+duration,thumbnailImage = imgUrl.encode('utf-8'))
        url = sys.argv[0]+'?tid='+urllib.quote_plus(showID)+'&level=2'
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, True)
    
    #上一页、下一页、返回主页、页码
    currPg = pgNum.split('/')[0]
    lastPg = pgNum.split('/')[1]

    if '-' in tid:
        tid = tid.split('-')[0]
        
    if int(currPg) < int(lastPg):
        listitem = xbmcgui.ListItem('下一页')
        url = sys.argv[0]+'?tid='+urllib.quote_plus(tid+'-'+str(int(currPg)+1))+'&level=1'
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, True)  
    if int(currPg) > 1:
        listitem = xbmcgui.ListItem('上一页')
        url = sys.argv[0]+'?tid='+urllib.quote_plus(tid+'-'+str(int(currPg)-1))+'&level=1'
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, True) 
    
    listitem = xbmcgui.ListItem('返回主页')
    url = sys.argv[0]+'?tid='+urllib.quote_plus('')+'&level=1'
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, True) 

    listitem = xbmcgui.ListItem(pgNum)
    url = sys.argv[0]+'?tid='+urllib.quote_plus('')+'&level=1'
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, False) 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def endList(tid):
    pgFile = urllib.urlopen('http://www.1993s.top/detail/?'+tid+'.html')
    pgData = pgFile.read()
    pgFile.close()

    theShowInfo_r = re.compile('<ul class="dslist-group clearfix">(.+?)target',re.DOTALL)
    theShowInfo = theShowInfo_r.search(pgData).group()

    theShowUrl_r = re.compile('href=\'(.+?)\'')
    theShowUrl = theShowUrl_r.search(theShowInfo).group().replace('href=\'','').replace('\'','')

    pgFile = urllib.urlopen('http://www.1993s.top'+theShowUrl)
    pgData = pgFile.read()
    pgFile.close()
    
    videoInfoList_r = re.compile('\$\$\$(.+?)\$\$\$')
    videoInfoList = videoInfoList_r.search(pgData)
    videoInfoList = videoInfoList.group(0).replace('$$$','').replace('极速播放$$','')

    videoUrlList = videoInfoList.split('#')
    
    cookiesA='UM_v_distinctid=2E3DF131810400369B777C059441478695FF2FFDEB9973F4A6DF3BFEE66CE37D'
    cookies={} 
    for line in cookiesA.split(';'):
        name,value = line.strip().split('=',1)  
        cookies[name] = value 
    heads = {}
    heads = {'Host': 'parse.hcc11.cn',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.1993s.top/js/player/H5.html?_=1324234432132',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Pragma': 'no-cache'
        }

    for videoUrlInfo in videoUrlList:
        videoUrl = videoUrlInfo.split('$')
        name = videoUrl[0]
        url = videoUrl[1]
        
        req = requests.get(url,cookies=cookies,headers=heads,allow_redirects=False)
        print(req)
        try:
            url = req.headers['Location']
        except:
            print('=================')
            name = name+'【获取数据异常】'
            url = ''
        listitem = xbmcgui.ListItem(name)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, False) 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_params():
    param = []
    if len(sys.argv[2]) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]  #params=['/','?']，没有需要的成员，使程序出错
        pairsofparams = cleanedparams.split('&')  #['imgUrl','level=1','name=番剧','quality']
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=') #
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
       #{'imgUrl':,'level':'1','name':'番剧','quality':}
    return param


params = get_params()
level = None
tid = ''

try:
    level = params["level"]
except:
    pass
try:
    tid = params["tid"]
except:
    pass

if tid == '':
    rootList()
elif level == '1':
    tvShowList(tid)
elif level == '2':
    endList(tid)
        

    
    
