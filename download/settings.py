class Settings():
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"
        self.video_type = set(("mkv","avi","flv","mpg","mpeg","mpe","m1v","m2v","mpv2","mp2v","dat","ts","tp","tpr","pva","pss","mp4","m4v","m4p","m4b","3gp","3gpp","3g2","3gp2","ogg","mov","qt","amr","rm","ram","rmvb","rpm"))
        self.url_ban =  r'[...]?C=[A-Z];O=[A-Z]$'
        self.th_num = 4