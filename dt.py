from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re
import sqlite3
import base64
import time

def dt(name,user):
   #初始化
   br=webdriver.Chrome()
   br.get("xxxxxxxxxxxxxxxxxcxxxxxxx")
   WebDriverWait(br, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/a[1]'))).click()


   #赋值数据
   br.find_element_by_id('login_username').send_keys(user) # 输入用户名
   br.find_element_by_id('login_password').send_keys("123456") 
   br.find_element_by_xpath('//*[@id="loginForm"]/div/a').click()
   br.implicitly_wait(10)
   while len(br.find_elements_by_class_name("btn.btn-primary.btn-sm"))>0:
      #设置隐式等待，防止数据刷新不及时
      br.implicitly_wait(10)
      jc=br.find_element_by_class_name("btn.btn-primary.btn-sm")
      jc.click()
      #进入具体答题界面
      br.implicitly_wait(10)
      jc=br.find_element_by_class_name("btn.btn-xs.btn-green")
      jc.click()
      #获取题目
      for item in br.find_elements_by_class_name("testCont"):
         #题目
         tm=item.find_element_by_tag_name("b").text
         #选项
         choose=item.find_element_by_class_name("choose-list").text
         #获取正确答案
         selector=item.find_elements_by_tag_name("input")
         trueAn=getAnswer(tm[7:])
         trueC=""
         if trueAn==None:
            print(tm+":\n"+choose+"\n未找到正确答案\n\n")
            trueC=input("请纯手工输入该题的答案:")
         else:
            tanlist=trueAn.split("$")
            for i in tanlist:
               tmp=''.join(i)
               trueC=trueC+choose.split(tmp)[0][-2:-1].strip()
         for ii in trueC:
            print("找到正确答案  "+str(trueAn)+",选项:"+trueC)
            if ii=="A":
               sid=0
            if ii=="B":
               sid=1
            if ii=="C":
               sid=2
            if ii=="D":
               sid=3
            selector[sid].click()
      #答完题之后开始提交答案
      br.find_element_by_id("postExamAnswer").click()
      time.sleep(2)
      br.find_element_by_class_name("layui-layer-btn0").click()

      #input(":")
      br.back()
      br.back()
      #br.back()
      br.refresh()
   time.sleep(2)
   br.close()
   return True
   
   
def getAnswer(tm):
   cx=sqlite3.connect("./tk.db")
   cu=cx.cursor()
   cu.execute("select * from tk where tm='"+encode(tm)+"'")
   an=cu.fetchall()
   for i in an:
      return decode(i[1])
def encode(s):
   return base64.b64encode(s.encode()).decode("utf-8")
def decode(s):
   return base64.b64decode(s.encode()).decode("utf-8")
   
   
   
with open("./user.txt") as lines:
   for line in lines:
      data=line.split("\t")
      user=data[1]
      name=data[0]
      dt(name,user)
        