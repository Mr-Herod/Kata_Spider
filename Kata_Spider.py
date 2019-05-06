from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from bs4 import BeautifulSoup as bs
import os,time,pickle

def main():
    path1 = input("Please input the path where the files will be saved: ")
    url1  = input("Please input the link which you want to grab data from: ")
    G1 = Grap_kata(url = url1 , path = path1)
    if os.access(path1+"cookie.cki",os.F_OK):
        G1.set_cookie()
    else:
        print("You will have 20 seconds to login in order to get the cookie.")
        G1.get_cookie()
    print("")
    G1.init_browser()
    G1.get_profile()
    G1.get_urls_and_kata_name()
    G1.get_demos_in_urls()

class Grap_kata:
    def __init__(self,url = "https://www.codewars.com/",path = "D:\\"):
        self.url = url # 设置主页链接
        self.path = path # 设置文件保存路径
        
    def set_url(self,url): # 设置主页链接
        self.url = url 
        
    def set_file_path(self,path): # 设置文件保存路径
        self.path = path
        
    def get_cookie(self): # 获取cookie值
        browser = webdriver.Chrome()
        browser.get(self.url)
        time.sleep(20)
        self.cookie1 = browser.get_cookies()[0]
        with open(self.path + "cookie.cki" , "wb") as f:
            pickle.dump(self.cookie1,f)
            print("Cookie:\n{}\n saved successfully ！(at:{})".format(self.cookie1,self.path + "cookie.cki"))
        browser.close()
        
    def set_cookie(self): # 设置cookie值 用于保持登陆状态
        with open(self.path + "cookie.cki" , "rb") as f:
            self.cookie1 = pickle.load(f)
            print("Setting cookie succeeded ！")
        
    def get_profile(self,opt = 1):
        if opt:
            self.browser.get(self.url) # 抓取主页页面demo
            self.soup = bs(self.browser.page_source,"html.parser")# 解析主页页面
        else:
            path = input("Please enter the html file path: ")
            with open(path,"r") as f:
                self.soup = bs(f.read(),"html.parser") # 解析demo 
        print("Getting profile page succeeded !!!")

    def get_urls_and_kata_name(self): # 提取kata名以及链接
        # 提取题目链接
        self.url_list = [["https://www.codewars.com"+i.get("href"), i.get_text()] for i in bs(str(self.soup.find_all(attrs = {"class":"item-title"})),"html.parser").find_all("a")]
        # 提取题目等级
        levels = [i.get_text().replace(" ","_") for i in bs(str(self.soup.find_all(attrs = {"class":"item-title"})),"html.parser").find_all("span")]
        for i in range(len(self.url_list)): # 格式化kata名
            self.url_list[i][1] = ("#" +  levels[i] + " " + self.url_list[i][1]).replace(" ","_").replace("?","")\
                    .replace("!","").replace("/","_").replace("\\","")\
                    .replace("<","_").replace(">","_").replace(":","_").replace("*","_")\
                    .replace("\"","_").replace("|","_")
        i,lens = 0,len(self.url_list)
        while i < lens: # 移除重复链接
            try:
                if self.url_list.count(self.url_list[i]) > 1 or os.path.exists(self.path + self.url_list[i][1] + ".py"):
                    self.url_list.remove(self.url_list[i])
                    i,lens = i-1 , lens-1
            except:
                pass
            i += 1

    def init_browser(self): # 初始化抓取窗口
        self.browser = webdriver.Chrome() # 创建一个新的浏览器窗口
        self.browser.get(self.url) # 获取页面demo
        self.browser.add_cookie(cookie_dict = self.cookie1) # 设置cookie值 进行登陆
        print("Initializing browser succeeded !!!")

    def write_file(self,path,content): # 写入读取到的数据 （题目描述+通过代码+他人代码）
        try: 
            with open(path,"w") as f:
                f.write(content)
            print("Saving file succeeded :",path,"\n")
        except:
            print("Saving file failed :",path,"\n")
    
    
    def get_page(self,url,kata_name,way,value,url1 = ""): # 抓取特定页面
        try: 
            if url1: 
                self.browser.get(url1)
            else:
                self.browser.get(url)
            WebDriverWait(self.browser,10).until(EC.visibility_of(self.browser.find_element(way,value))) # 等待元素出现
        except TimeoutException:
            print("Program is still running ...")
            pass
        except:
            raise
            self.url_list.append([url,kata_name])
            return None
        return bs(self.browser.page_source,"html.parser")

    def restart_browser(self,num): # 重启浏览器
        self.browser.close()
        print("No.{} page waits for regrab !".format(num))
        self.init_browser()
        self.browser.add_cookie(cookie_dict = self.cookie1)

    def get_demos_in_urls(self): # 依次抓取列表中的页面demo
        print("\nMain process started !\nIt may take several minutes to get the work done.\n")
        for num,[url,kata_name] in enumerate(self.url_list):
            print("Grapping the No.{} page   ...".format(num+1))
            soup = self.get_page(url,kata_name,"id","solutions")
            if soup == None:
                self.restart_browser(num)
                continue
            desc = soup.find_all(attrs = {"class":"markdown"}) # 获取题目描述
            solutions = "https://www.codewars.com" + soup.find_all("a",attrs = {"id":"solutions"})[0].get("href") # 获取题目solution页面链接
            soup = self.get_page(url,kata_name,"tag name","code",url1 = "/".join(solutions.split("/")[:-1]) + "/python") # 抓取题目页面
            if soup == None:
                self.restart_browser(num)
                continue
            # 抓获取别人的代码（两份）
            codes = soup.find_all("code",attrs = {"class":"is-darkened","data-language":"python"})
            if len(codes) <= 2:
                self.url_list.append([url,kata_name])
                print("No.{} page waits for regrab !".format(num))
                continue
            code0,code1 = codes[0].get_text(),codes[2].get_text()
            # 抓取自己的代码
            soup = self.get_page(url,kata_name,"tag name","code",url1 = "/".join(solutions.split("/")[:-1]) + "/python/me/best_practice")
            if soup == None:
                self.restart_browser()
                continue
            mycode = soup.find_all("code",attrs = {"class":"is-darkened","data-language":"python"})
            if not mycode:
                mycode = "\n"
            else:
                mycode = mycode[0].get_text()
            # 填写文件内容
            content = "Description:\n\n" + "\"\"\"\n" + desc[0].get_text() + "\n\"\"\"\n\n" \
                     + "My codes:\n\n"   +  mycode \
                     + "\n\nOthers codes:\n\n" + code0 + "\n\n" + code1 + "\n"
            # 设置文件保存路径
            path =  self.path + kata_name + ".py"
            self.write_file(path,content)
        self.browser.close() # 关闭浏览器窗口
        print("Process finished !!!")

if __name__ == "__main__":
    main()
