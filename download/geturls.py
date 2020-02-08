#!/usr/bin/python3
#coding=utf-8

import  requests
from bs4 import  BeautifulSoup as bs
from settings import Settings
import re
class  GetUrls():
    """
        解析url
    """
    def __init__(self):
        settings = Settings()
        self.user_agent = settings.user_agent
        self.video_type = settings.video_type
        self.url_ban = settings.url_ban

    def if_page(self,link):
        """判断链接是否为页面"""
        end = link.split('/')[-1]
        if not '.' in end:
            return True
        if end and end.split('.')[-1] != "html":
            return False
        else:
            return True

    def if_video(self,link):
        """判断链接是否为视频链接"""
        typeoflink = link.split('.')[-1] 
        if  typeoflink in self.video_type:
            return True
        else:
            return False

    def __get_content_by_url(self,link):
        """使用requests得到链接的页面内容,如果链接是一个文件返回Fales"""
        headers = {
            'User-Agent':self.user_agent
        }
        response = requests.get(link,headers=headers,stream=True)
        content = response.text
        response.close()
        return content

    def get_all_urls_from_content(self,content,rootlink):
        """通过页面内容获取链接,并返回一个链接列表"""
        urls = []
        soup = bs(content,'lxml')
        for item in soup.find_all("a"):
            if item.string == None:
                continue
            else:
                link = item.get('href')
                if link[0:4] != 'http':
                        if link[0]== '/':
                            continue
                        else:
                            link = rootlink + link
                if re.search(self.url_ban,link):
                    continue
                urls.append(link)
        return set(urls)

    def get_all_video_urls_by_url(self,rooturl):
        """通过页面获取全站视频链接"""
        urls = []
        gettedurls = []
        def inside(url):
            if self.if_video(url):
                urls.append(url)
                print("已得到链接%d,%s"%(len(urls) ,url))
                return
            if not self.if_page(url) or url in gettedurls:
                return
            try:
                content = self.__get_content_by_url(url)
                somelinks = self.get_all_urls_from_content(content,url)
            except:
                gettedurls.append(url)
                print("连接失败,无法获得该页面连接:%s"%url)
            if len(somelinks)==0:
                return
            for link in somelinks:
                    inside(link)
            return
        inside(rooturl)
        return set(urls)

if __name__ == "__main__":
    get = GetUrls()
    result = get.get_all_video_urls_by_url("http://lab.nqnwebs.com/descargas/")