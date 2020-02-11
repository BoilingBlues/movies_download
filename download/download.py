#!/usr/bin/python3
#coding=utf-8

import os
import requests
import sys
from tqdm import tqdm
import threading
import time

class DownLoad():
    ''' 
    视频下载api
    '''
    def __init__(self,root,th_num,link):
        '''
        初始化文件存储路径
        初始化线程数
        确定下载链接
        '''
        self.root =  root
        self.th_num = th_num
        self.link = link
        self.current_size = 0
        
    def download_videofile(self,pach_num,start,end):
        '''
        控制单个下载线程
        '''
        file_name = self.link.split('/')[-1]
        file_dst = self.root+file_name+str(pach_num)
        #断点判断
        if os.path.exists(file_dst):
            start=start + os.path.getsize(file_dst)

        header = {
            "Range":"bytes={0}-{1}".format(start,end)
        }
        print(header)
        #断点请求
        try:
            response = requests.get(self.link,headers=header,stream=True)
            #下载文件
            print("正在下载%s" %file_name)
            with open(file_dst,'ab') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        self.current_size += 1024
            print("第%d个pach下载完成\n"%pach_num)
            response.close()
        except:
            print("错误：第%d个pach下载失败\n"%pach_num)

        return

    
    def p_bar(self,file_size):
        """
        进度条
        """
        #断点判断
        existed_size = 0
        for i in range(self.th_num):
            file_name = self.link.split('/')[-1]
            file_dst = self.root+file_name+str(i)
            if os.path.exists(file_dst):
                existed_size += os.path.getsize(file_dst)
        #创建进度条
        pbar = tqdm(total=file_size,initial=existed_size,unit='B',unit_scale=True,desc="下载进度",miniters=1)
        #unit:定义迭代单元,B为字节,默认bit,,,unit_scale:进制转换自动转换MB和KB,,,miniters:最小更新间隔.

        #更新进度条
        last_time_size = 0
        while self.current_size+existed_size<file_size:
            if self.current_size != last_time_size:
                pbar.update(self.current_size-last_time_size)
                last_time_size = self.current_size
            time.sleep(1)
        pbar.close()
        print('下载完成！')
        return

            

    def multi_th_down(self):
        '''
        多线程下载
        '''
        try:
            response = requests.get(self.link,stream=True)
            file_size = int(response.headers['content-length'])
            print(file_size)
            response.close()

        except:
            print('错误：链接异常')

        else:
            #分pach下载
            pach_size = file_size//self.th_num
            thread = []
            for i in range(self.th_num):
                if i != self.th_num-1:
                    start = i*pach_size
                    end = (i+1)*pach_size
                else:
                    start = i*pach_size
                    end = file_size
                print('%d,%d,\n'%(start,end))
                #添加下载线程
                thread.append(threading.Thread(target=self.download_videofile,args=(i,start,end)))
                thread[i].start()

            #添加进度条线程
            pbar_thread = threading.Thread(target=self.p_bar,args=[file_size])
            pbar_thread.start()
            #等待进度条线程运行结束
            pbar_thread.join()
            #判断文件是否完整下载
            download_size = 0
            file_name = self.link.split('/')[-1]
            for i in range(self.th_num):
                pach_file_dst = self.root+file_name+str(i)
                if os.path.exists(pach_file_dst):
                    download_size += os.path.getsize(pach_file_dst)
            if download_size == file_size:
                #合并文件
                file_dst = self.root+file_name
                with open(file_dst,'ab') as f:
                    for i in range(self.th_num):
                        pach_file_dst = self.root+file_name+str(i)
                        with open(pach_file_dst,'rb') as p_f:
                            l = p_f.read()
                            f.write(l)
                print('文件合并完成！')
            else:
                print('错误：文件不完整')
        return


        





if  __name__ == "__main__":
    l = 'http://mirror.as29550.net/releases.ubuntu.com/18.04.3/ubuntu-18.04.3-desktop-amd64.iso'
    download = DownLoad('./',2,l)
    download.multi_th_down()
