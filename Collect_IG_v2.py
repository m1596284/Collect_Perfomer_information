# -*- coding: UTF-8 -*-
import os
from bs4 import BeautifulSoup
import threading
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import numpy as np
import re
from time import sleep
import sys
import random
from fake_useragent import UserAgent
import time

ua = UserAgent()
# ua = "Mozilla/5.0 (Linux; U; Android 2.2.1; en-us; Nexus One Build/FRG83) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
# ua = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
ua = ua.random
headerPara = {'User-Agent': ua}

pyPath, filename = os.path.split(__file__)
keyword = ["leejieun"]



accounts = [
            "ID1","PW1",
            "ID2","PW2",
            "ID3","PW3",
            "...and so on"
            ]
infoStart = 0
loopStart = 0
loopSleepTime = 95+random.randint(1,5)
sleepTime = 5
errorSleepTime = 5
period = 10
tagRunIndex = 3

def Tags(keywordinput):
    keyword = keywordinput
    urlList=[]
    tags_page = "https://www.instagram.com/explore/tags/"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加載圖片, 提升速度
    # chrome_options.add_argument('--headless') 
    chrome_options.add_argument("user-agent={}".format(ua))
    driver = webdriver.Chrome(executable_path=pyPath + '/chromedriver.exe',chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(tags_page + keyword + '/?hl=zh-tw')
    sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        tagNum = soup.find('span',class_="g47SY").text.replace(",","")
    except:
        tagNum = "30"
    try:
        if tagNum == "NaN":
            tagNum = "30"
    except:
        pass
    if tagNum.find(".")>0:
        tagNum = tagNum.replace("萬","000")
        tagNum = tagNum.replace(".","")
    else:
        tagNum = tagNum.replace("萬","0000")
    tagRun = int(int(tagNum)/tagRunIndex)
    # print(tagRun)
    if tagRun>10000:
        tagRun = 10000
    # sleep(10000)
    # print(tagRun)

    for i in range(1,tagRun):
        print(keyword + ": " + str(i) + "/" + str(tagRun))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.5)
        driver.execute_script("window.scrollBy(-330,-330);")
        sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        urls = soup.find_all('a',href=re.compile("/p/B"))
        for url in urls:
            # print(url.get('href'))
            urlList.append(str(url.get('href')))
    urlList2 = list(set(urlList)) #duplicate
    driver.close()

    f2 = open(pyPath + "/" + keyword + "_urls.txt","w+", encoding='UTF-8')
    for num, url in enumerate(urlList2):
        f2.write(str(urlList2[num]) + '\n')
    f2.close
    print(keyword + " urls collected Done")

def IDs(keywordinput):
    keyword = keywordinput
    Main_page = "https://www.instagram.com/"
    f3 = open(pyPath + "/" + keyword + "_urls.txt","r", encoding='UTF-8')
    readFile3 = f3.readlines()
    f3.close
    # print('1')
    # print(len(readFile3))
    # print(readFile3[1].strip('\n'))
    IDList =[]
    f = open(pyPath + "/" + keyword + "_IDs.txt","a", encoding='UTF-8')
    for i in range(0,int(len(readFile3))):
        try:
            r = requests.get(Main_page + readFile3[i], headers=headerPara)
            print(keyword + ": " + str(i) + '/' + str(len(readFile3)-1))
            if r.text.find("(@") == -1:
                nameStart = r.text.find("@")+1
                nameEnd = r.text.find(" on Instagram",nameStart)
                # print(r.text[nameStart:nameEnd])
                r2 = r.text[nameStart:nameEnd]
                if len(r2)>30:
                    pass
                else:
                    IDList.append(r2)
                print(r2)
            else:
                nameStart = r.text.find("(@")+2
                nameEnd = r.text.find(")",nameStart)
                # print(r.text[nameStart:nameEnd])
                r2 = r.text[nameStart:nameEnd]
                if len(r2)>30:
                    pass
                else:
                    IDList.append(r2)
                print(r2)
            f.write(str(r2) + '\n')
        except:
            sleep(60)
            continue
    f.close
    f = open(pyPath + "/" + keyword + "_IDs.txt","r", encoding='UTF-8')
    readFile = f.read()
    f.close
    IDList2 = list(set(IDList))
    f4 = open(pyPath + "/" + keyword + "_IDs.txt","w", encoding='UTF-8')
    for ID in IDList2:
        f4.write(str(ID) + '\n')
    f4.close
    print(keyword + " IDs collected Done")


def Info(keywordinput,botID,acctID,acctPW):
    keyword = keywordinput
    botID = botID
    ID = acctID
    PW = acctPW
    Main_page = "https://www.instagram.com/"
    login_page ="https://www.instagram.com/accounts/login/?source=auth_switcher"
    f = open(pyPath + "/" + keyword + "_IDs.txt","r", encoding='UTF-8')
    readFile = f.readlines()
    f.close
    print(len(readFile))
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless') 
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument("user-agent={}".format(ua))
    driver = webdriver.Chrome(executable_path=pyPath + '/chromedriver.exe',chrome_options=chrome_options)
    driver.get(login_page)
    sleep(5)
    timeStart = time.time()
    cnt = 0
    sleepCnt = 0
    for i in range(infoStart,int(len(readFile))):
        if i%botNum == botID:
            cnt = cnt + 1
            infoNow = i
            infoNum =(infoNow-infoStart-botID)/botNum+1
            try:
                username = driver.find_element_by_xpath('//*[@name="username"]')
                password = driver.find_element_by_xpath('//*[@name="password"]')
                login_btn = driver.find_element_by_xpath('//*[@class="sqdOP  L3NKy   y3zKF     "]')
                username.send_keys(ID)
                password.send_keys(PW)
                sleep(1)
                login_btn.click()
                sleep(3)
                # username = driver.find_element_by_xpath('//*[@name="username"]')
                # password = driver.find_element_by_xpath('//*[@name="password"]')
                # login_btn = driver.find_element_by_xpath('//*[@class="sqdOP  L3NKy   y3zKF     "]')
                # action = ActionChains(driver)
                # action2 = ActionChains(driver)
                # action3 = ActionChains(driver)
                # action.move_to_element(username).click(username).send_keys("markchu159").perform()
                # sleep(2)
                # action2.move_to_element(password).click(password).send_keys("chuIG159").perform()
                # sleep(2)
                # # action3.send_keys(keys.ENTER).perform()
                # # sleep(2)
                # login_btn.click()
            except:
                pass
            # print(keyword + ": " + str(i) + '/' +str(len(readFile)))
            UserID = str(readFile[i]).strip('\n')
            # print(UserID)
            driver.implicitly_wait(3)
            driver.get(str(Main_page + UserID))
            sleep(1)
            for ii in range(random.randint(1,5)):
                driver.execute_script("window.scrollBy(" + str(random.randint(100,500)) + "," + str(random.randint(100,500)) + ");")
                sleep(1)
            timesCnt = 0
            while driver.page_source.find("請幾分鐘後再試一次。") > -1 or driver.page_source.find("Please wait a few minutes before you try again") > -1:
                timesCnt = timesCnt +1
                timeNow = time.time()
                timeAvg = (timeNow-timeStart)/infoNum
                print("Bot " + str(botID) + " error " + keyword + ": " + str(i) + "/" + str(len(readFile)) + " " + "Avg time: " + str(timeAvg) + " waiting for few mins, timer: " + str(timesCnt))
                try:
                    driver.get("https://tw.geoipview.com/")
                except:
                    continue
                sleep(errorSleepTime*60)
                driver.get(str(Main_page + UserID))
            f = open(pyPath + "/" + keyword + "_timer.txt","a", encoding='UTF-8')
            f.write(str(i) + '\t' + str(timesCnt) + '\n')
            f.close
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # f = open(pyPath + "/" + keyword + "_soup.txt","a", encoding='UTF-8')
            # f.write(str(soup))
            # f.close

            if soup.find('h1',class_='rhpdm') == None:
                UserName = UserID
            else:
                UserName = soup.find('h1',class_='rhpdm').text
            # print(soup.find('div',class_='-vDIg'))
            if soup.find('div',class_='-vDIg') == None or soup.find('div',class_='-vDIg').find('span') == None:
                UserDis ="No Dis"
            else:
                UserDis = soup.find('div',class_='-vDIg').find('span').text
            if soup.find('a',class_='yLUwa') == None:
                UserUrl = "No url"
            else:
                UserUrl = soup.find('a',class_='yLUwa').get('href')
            details = soup.find_all('span',class_='g47SY')
            # print(details)
            try:
                UserPosts = details[0].text
                UserFollowers = details[1].text
                UserFollowing = details[2].text
            except:
                UserPosts = "No"
                UserFollowers = "No"
                UserFollowing = "No"
            timeNow = time.time()
            timeAvg = (timeNow-timeStart)/infoNum
            print("Bot " + str(botID) + " OK " + keyword + ": " + str(i) + "/" + str(len(readFile)) + " " +"Avg time: " + str(timeAvg) + " " + UserID + " " + UserName + " " + UserPosts + " " + UserFollowers + " " + UserFollowing)
            # print(UserDis)
            f = open(pyPath + "/" + keyword + ".txt","a", encoding='UTF-8')
            f.write(UserName + '\t' + UserPosts + '\t' + UserFollowers + '\t' + UserFollowing + '\t' + UserDis + '\t' + UserUrl + '\t' +Main_page + UserID + '\n')
            f.close
            driver.get("https://tw.geoipview.com/")
            sleep(loopSleepTime)
            # print(str(cnt) + "/" + str(cnt/period))
            # print("mod:" + str(i%period))
            if (cnt%period) == 0:
                sleepCnt = sleepCnt+1
                print("Bot " + str(botID) + " Sleep Count: " + str(sleepCnt) + " Sleep for few mins")
                sleep(sleepTime*60)
        else:
            pass
    driver.close()
    print("Bot " + str(botID) + " " + keyword + " Info collected Done")


for iii in range(loopStart,len(keyword)):
    # if iii == 9999:
    #     infoStart = 9999
    # else:
    #     infoStart = 0
    # threads = []
    # botNum = 5
    # for num in range(botNum):
    #     botID = num
    #     acctID = accounts[botID*2]
    #     acctPW = accounts[botID*2+1]
    #     threads.append(threading.Thread(target = Info, args = (keyword[iii],botID,acctID,acctPW)))
    #     threads[num].start()
    #     # sleep(5)
    # for num in range(botNum):
    #     threads[num].join()

    Tags(keyword[iii])
    IDs(keyword[iii])
    # Info(keyword[iii])