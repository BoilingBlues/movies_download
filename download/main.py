from downloader import DownLoad
from geturls import GetUrls
import os



def check_root(root):
    if root[-1]!='/' and root[-1]!='\\':
        return False
    else:
        return True

def main():
    print("使用前请仔细查看README.md,Ctrl+C可以终止程序")
    while(1):
        choose = input("请选择运行方式\n 1.通过urls.txt文件下载\n 2.搜寻网址并下载\n 输入:")
        if choose=='2':
            online_download()
            return
        elif choose=='1':
            file_download()
            return
        else:
            print("请输入1或2")
def online_download():
    get = GetUrls()
    link = input("请输入要搜寻的网址:")
    print("开始搜寻")
    links = get.get_all_video_urls_by_url(link)
    print("请确认是否是想要的视频链接,如果不是请到settings.py中添加正则表达式过滤匹配链接")
    result = input("确认下载请输入y或Y,输入save将链接保存到当前目录下的urls.txt,可以手动删除不需要的链接  \n 输入: ")
    if result == 'save':
        with open('urls.txt','w') as f:
            for  link in links:
                f.write(link+'\n')
        print("已保存,退出成功")
    if result!='y' and result!='Y':
        print("退出成功")
        return
    download_to_index(links)

def download_to_index(links):
    while(1):
        dst = input("请输入保存视频的目录:")
        if not check_root(dst):
            print("请在目录的末尾加/,windows请加\\")
        else:
            break
    download = DownLoad(dst)
    num = 0
    for link in links:
        download.download_videofile(link)
        num+=1
        print("已下载%d个,一共%d个"%(num,len(links)))

def file_download():
    if not os.path.exists('urls.txt'):
        print("当前目录下没有urls.txt\n退出成功")
        return
    links = []
    with open('urls.txt','r') as f:
        for line in f:
            links.append(line[:-1])
    download_to_index(links)
    



        
if  __name__ == "__main__":
    main()