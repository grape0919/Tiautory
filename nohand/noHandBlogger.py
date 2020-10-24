from PyQt5.QtCore import QDateTime
from openpyxl import load_workbook
import random
import requests
import os


class HeadOfBlogger:

    def __init__(self, prop):
        self.url = prop.url

    def readExcelFile(self, filepath):
        print("Blogger read excel")
        load_wb = load_workbook(filepath)
        #시트 이름으로 불러오기
        for load_ws in load_wb:
            # load_ws = load_wb['문단']
            mylist = [ [c.value for c in r]  for r in load_ws ]
            self.phList = list(map(list, zip(*mylist)))
            break

        self.isLoaded = True

    def makeArticle(self):
        if(self.isLoaded):
            result = []
            for phs in self.phList:
                temp = None
                while(temp==None):
                    temp = random.choice(phs)

                result.append(temp)
            return result
        else:
            print("문단 엑셀 파일을 먼저 불러오세요.")
            return None

class ApiBlogger(HeadOfBlogger):

    # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
    # APP_ID = ""
    # SECRET_KEY = ""
    REDIRECTION_URL = "http://"
    isLoaded=False
    ACCESS_TOKEN = ""

    url = ""
    
    def __init__(self, prop):
        super.__init__(self, prop)
        self.ACCESS_TOKEN = prop.token

   
    
    def postArticle(self):

        article = self.makeArticle()
        
        if(article is not None):
            result = ''
            for idx in range(len(article)):
                # print("!@#!@# : ", article[idx])
                if article[idx].startswith("<img"):
                    imgNumber = article[idx].split("=")[1]
                    imgNumber = imgNumber[0:len(imgNumber)]
                    # print(imgNumber)
                else :
                    result += article[idx]

        ##사진 업로드
            # files = {'uploadedfile': open(filepath, 'rb')}
            # datas = {
            #     "access_token":self.ACCESS_TOKEN,
            #     "blogName": self.blog_name
            # }
            # r = requests.post('https://www.tistory.com/apis/post/attach', data=datas, files=files)
            # print(r.text)

        ##글쓰기
            title = article[0]			 # 제목
            content = result			# 내용
            visibility = "3" 			# 0비공개-기본, 1보고,3발행
            category_id = "" 	    #카테고리 아이디. 자신의 blog 소스를 봐야한다.
            slogan = "" 				#문자주소. 뭔지 모르겠다.
            tag = ""  	#태그 ,로 구분
            acceptComment = "" 			#댓글 허용 (0, 1 - 기본값)
            password = "" 				#보호글 비밀번호
            datas = {
                "access_token":self.ACCESS_TOKEN,
                "output":"json",
                "blogName": self.url,
                "title":title,
                "content":content,
                "visibility":visibility,
                "category":category_id,
                "slogan":slogan,
                "tag":tag,
                "acceptComment":acceptComment,
                "password":password
            }
            r = requests.post('https://www.tistory.com/apis/post/write', data=datas)
            # print(r.text)



from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
import time
import threading

class SeleniumBlogger(HeadOfBlogger):

    url = ""
    id = ""
    passwd = ""

    running = False
    datetime = None
    period = 0

    def __init__(self):        
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        options = wb.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        self.driver = wb.Chrome(executable_path='lib/chromedriver.exe', chrome_options=options)
        self.driver.implicitly_wait(10)

    def setProp(self, prop, qDateTime, period):
        self.url = prop.url
        self.id = prop.id
        self.passwd = prop.passwd

        self.datetime = qDateTime
        self.period = period*60

    def postArticle(self):
        self.running = True

        try:
            if(self.url.endswith(".com")):
                self.url += "/"
        
            self.driver.get(self.url + "manage/entry/post")
            self.driver.find_element_by_id("loginId").send_keys(self.id)
            self.driver.find_element_by_id("loginPw").send_keys(self.passwd)

            self.driver.find_element_by_class_name("btn_login").click()
        except:
            return (False, "로그인 실패하였습니다.\nurl, id, password 를 확인해주세요.")

        th = threading.Thread(target=self.postingThread, args=())
        th.start()


    def postingThread(self):
        print("Blogger start posting")
        while(self.running):
            gap = self.datetime.secsTo(QDateTime.currentDateTime())
            print("gap : ", gap)
            if(gap < 0):
                print("1wait for ", (gap*-1))
                time.sleep(gap*-1)
                continue
            elif(gap >= 0):
                temp = gap%self.period
                if(temp > 0):
                    print("1wait for ", self.period-temp)
                    time.sleep(self.period-temp)
                    continue
                elif(temp == 0):
                    print("게시")
                    time.sleep(5)
                    self.post()
                    
    def post(self):
        article = self.makeArticle()
        if(article is not None):
            self.driver.get(self.url + "/manage/entry/post")
            try:
                time.sleep(1)
                alert = self.driver.switch_to.alert
                alert.dismiss()
            except:
                print("alert 창 없음")

            self.driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[2]/textarea").send_keys(article[0])
            
            iframes = self.driver.find_elements_by_tag_name('iframe')

            imgFolderPath = os.getcwd()+"\\img"

            for idx in range(1,len(article)):
                if(article[idx] == "<img>"):
                    img_file_list = os.listdir(imgFolderPath)
                    imgFilePath = imgFolderPath+"/"+random.choice(img_file_list)
                    self.driver.find_element_by_id("mceu_0-open").click()
                    self.driver.find_element_by_id("mceu_32").click()
                    self.driver.find_element_by_id("openFile").send_keys(imgFilePath)
                    self.driver.switch_to_frame(iframes[0])
                    self.driver.find_element_by_id("tinymce").send_keys(imgFilePath)
                    self.driver.find_element_by_id("tinymce").send_keys(Keys.ENTER)
                    self.driver.switch_to_default_content()

                else:
                    self.driver.switch_to_frame(iframes[0])
                    self.driver.find_element_by_id("tinymce").send_keys(article[idx])
                    self.driver.find_element_by_id("tinymce").send_keys(Keys.ENTER)
                    self.driver.switch_to_default_content()
                
            self.driver.find_element_by_xpath("/html/body/div[2]/div/div[4]/div[3]/button").click()
            self.driver.find_element_by_xpath("/html/body/div[7]/div/div/div/form/fieldset/div[3]/div/button[2]").click()
