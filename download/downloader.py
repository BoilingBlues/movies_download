#!/usr/bin/python3
#coding=utf-8

import os
import requests
from tqdm import tqdm
import threading
from settings import Settings
import random

class DownLoad():
    ''' 
    视频下载api
    '''
    def __init__(self,root):
        '''初始化'''
        setting = Settings()
        self.root = root
        self.th_num = setting.th_num
        self.user_agent = setting.user_agent
    
    def download_videofile(self,link):
        '''下载器'''
        file_name = self.get_file_name(link)
        solo,file_size = self.if_solo(link)
        pbar1 = self.p_bar(file_size,"正在分配空间")
        self.pre_file_creat(file_name,file_size,pbar1)
        pbar1.close()
        pbar2 = self.p_bar(file_size,"正在下载")
        if solo:
            self.part_download(link,file_name,1,0,file_size,pbar2)
        else:
            pach_size = file_size//self.th_num
            thread = []
            for i in range(self.th_num):
                if i==self.th_num-1:
                    thread.append(threading.Thread(target=self.part_download,args=(link,file_name,i,i*pach_size,file_size,pbar2)))
                else:
                    thread.append(threading.Thread(target=self.part_download,args=(link,file_name,i,i*pach_size,(i+1)*pach_size,pbar2)))
                thread[i].start()
        pbar2.close()

    def part_download(self,link,file_name,pach_num,start,end,pbar):
        '''下载指定段文件到指定段位置'''
        headers = {
            "Range":"bytes={0}-{1}".format(start,end),
            'User-Agent':self.user_agent
        }
        response = requests.get(link,headers=headers,stream=True)
        print("正在下载%s" %file_name)
        with open(self.root+file_name,'rb+') as f:
            f.seek(start)
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        response.close()

    def pre_file_creat(self,file_name,size,pbar):
        '''预创建指定大小的文件'''
        with open(self.root+file_name,"wb") as f:
            times = size//1024
            remain = size%1024
            for i in range(times):
                f.write(b'\x2F'*1024)
                pbar.update(1024)
            for i in range(remain):
                f.write(b'\x2F')
                pbar.update(1)


    def if_solo(self,link):
        '''判断网址是否支持断点续传'''
        headers = {
            'User-Agent':self.user_agent
        }
        response = requests.get(link,headers=headers,stream=True)
        file_size = int(response.headers['content-length'])
        if response.headers['accept-ranges']:
            solo = True
        else:
            solo = False
        return solo,file_size

    def p_bar(self,size,message):
        '''进度条,返回一个pbar实例'''
        pbar = tqdm(total=size,initial=0,unit='B',unit_scale=True,desc=message,miniters=1)
        return pbar

    def get_file_name(self,link):
        file_name = link.split('/')[-1]
        return file_name

if  __name__ == "__main__":
    dl = DownLoad('./')
    dl.download_videofile('http://89.40.4.78/walking_dead/The.Walking.Dead.S09E01.HDTV.x264-SVA%5Bettv%5D.mkv')