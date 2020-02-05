#!/usr/bin/python3
#coding=utf-8

import os
import requests
import sys
from tqdm import tqdm

class DownLoad():
    ''' 
    视频下载api
    '''
    def __init__(self,root):
        '''初始化文件存储路径'''
        self.root =  root
        
    def download_videofile(self,link):
        '''
        参数:视频链接
        '''
        response = requests.get(link,stream=True)
        file_size = int(response.headers['content-length'])
        response.close()
        file_name = link.split('/')[-1]
        file_dst = self.root+file_name
        #断点判断
        if os.path.exists(file_dst):
            first_byte=os.path.getsize(file_dst)
        else:
            first_byte = 0
        header = {
            "Range":f"bytes={first_byte}-{file_size}"
        }
        #断点请求
        response = requests.get(link,headers=header,stream=True)
        
        #下载文件
        print("正在下载%s" %file_name)
        pbar = tqdm(total=file_size,initial=first_byte,unit='B',unit_scale=True,desc="下载进度",miniters=1)
         ##unit:定义迭代单元,B为字节,默认bit,,,unit_scale:进制转换自动转换MB和KB,,,miniters:最小更新间隔.

        with open(file_dst,'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        pbar.close()
        print("下载完成\n")
        response.close()
        return


if  __name__ == "__main__":
    download = DownLoad(sys.argv[1])
    for link in sys.argv[2:]:
        download.download_videofile(link)    

    
    