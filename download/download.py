#!/usr/bin/python3
#coding=utf-8

import requests
import sys

class DownLoad():
    ''' 
    视频下载api
    '''
    def __init__(self,root):
        '''初始化文件存储路径'''
        self.root =  root
        
    def download_videofile(self,link):
        '''
        逐个下载视频
        参数:视频链接列表
        '''
        file_name = link.split('/')[-1]
        #在这里加命令行进度条
        print("开始下载:%s" % file_name)
        #在这里加命令行进度条
        r = requests.get(link,stream=True)
        with open(self.root+file_name,'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        #在这里加命令行进度条
        print("%s 下载完成\n" % file_name)
        return


if  __name__ == "__main__":
    print("输入文件路径和视频链接")
    download = DownLoad(sys.argv[1])
    for link in sys.argv[2:]:
        download.download_videofile(link)    

    
    