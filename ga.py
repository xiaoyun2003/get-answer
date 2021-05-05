from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re
import sqlite3
import base64
import time

def ga(xb,user):
   #初始化
   br=webdriver.Chrome()
   br.get("xxxxxxxxxxxxxxxxxxxxxxx")
   WebDriverWait(br, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/a[1]'))).click()
   #赋值数据
   br.find_element_by_id('login_username').send_keys(user) # 输入用户名
   br.find_element_by_id('login_password').send_keys("123456") 
   br.find_element_by_xpath('//*[@id="loginForm"]/div/a').click()
   br.implicitly_wait(10)
   list11=br.find_elements_by_class_name("btn.btn-success.btn-sm")
   size=len(list11)
   jc=list11[xb]
   jc.click()
   #进入具体答题界面
   jc=br.find_element_by_class_name("btn.btn-xs.btn-green")
   jc.click()
   #获取题目
   cx=sqlite3.connect("./tk.db")
   cu=cx.cursor()
   br.implicitly_wait(10)
   for item in br.find_elements_by_class_name("testCont"):
      #题目
      br.implicitly_wait(10)
      tm=item.find_element_by_tag_name("b").text
      #选项
      choose=item.find_element_by_class_name("choose-list").text+"\n"
      #正确选项
      trueC=re.findall("[A-D]",item.find_elements_by_class_name("mb5")[1].text)
      print(trueC)
      
      an=""
      for ii in trueC:
         a=''.join(re.findall(ii+"\.(.*?)\n",choose))
         an=an+a+"$"
      an=an[:-1]
      print(an)
      print("=============")
      #写入题库
      cu.execute("create table if not exists tk(tm text unique,da text)")
      cu.execute("insert or replace into tk values ("+"'"+encode(tm[7:])+"','"+encode(an)+"')")
      cx.commit()
   cu.close()
   time.sleep(2)
   br.close()
   pass

def encode(s):
   return base64.b64encode(s.encode()).decode("utf-8")
def decode(s):
   return base64.b64decode(s.encode()).decode("utf-8")
   


global size
size=0
while True:
   print("数据总数为:"+str(size))
   xb=int(input("输入读取的数据:"))
   ga(xb,"xxxxxxxxxxxxxx")
   