from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import captura
from PIL import Image
import time
import tkinter as tk
someCourse = [['1','ZCS00080'], ['3','AGE20060']]


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.set_window_size(1024, 960)


    driver.get('http://ecsa.ntcu.edu.tw')

    cp = driver.find_element_by_id('ImgCheckCode')

    cpLocation = cp.location
    cpSize = cp.size
    driver.save_screenshot("screenshot.png")

    x = cpLocation['x'] * 2
    y = cpLocation['y'] * 2
    width = (cpLocation['x'] + cpSize['width']) * 2
    height = (cpLocation['y'] + cpSize['height']) * 2
    im = Image.open('./screenshot.png')
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save('captura.png')

    capturaNum = captura.solve_captcha('./captura.png')

    account = driver.find_element_by_xpath('//*[@id="UserID"]')
    password = driver.find_element_by_xpath('//*[@id="PWD"]')
    cpinput = driver.find_element_by_xpath('//*[@id="txtCheckCode"]')
    loginButton = driver.find_element_by_xpath('//*[@id="login_btn"]')
    acc = input("Account: ")
    pwd = input("Password: ")
    account.send_keys(acc)
    password.send_keys(pwd)
    cpinput.send_keys(capturaNum)
    print(capturaNum)
    #TODO: Why no click loginbutton then login?

    driver.save_screenshot("screenshot1.png")

    menu = driver.find_element_by_xpath("//*[@id='ShowHeaderMenuDiv']/table/tbody/tr/td/span[2]")
    menu.click()
    driver.get("http://ecsa.ntcu.edu.tw/STDWEB/SelChoose/SelChooseMain.aspx")
    time.sleep(3)
    driver.save_screenshot("screenshot2.png")

    queryCourseBtn = driver.find_element_by_xpath('//*[@id="cmdInquire"]')

    queryCourseBtn.click()
    time.sleep(1)
    courseIdInput = driver.find_element_by_xpath('//*[@id="txtCosID"]')
    courseQuery = driver.find_element_by_xpath('//*[@id="cmdQueryCur"]')
    courseGrade = driver.find_element_by_xpath('//*[@id="txtGrade"]')
    count = 0
    full = True

    
    while full:
        index = 0
        for i in someCourse:
            courseIdInput.send_keys(i[1])
            try:
                if driver.switch_to.alert():
                    driver.switch_to.alert().accept()
                    driver.get('http://ecsa.ntcu.edu.tw')

                    cp = driver.find_element_by_id('ImgCheckCode')

                    cpLocation = cp.location
                    cpSize = cp.size
                    driver.save_screenshot("screenshot.png")

                    x = cpLocation['x'] * 2
                    y = cpLocation['y'] * 2
                    width = (cpLocation['x'] + cpSize['width']) * 2
                    height = (cpLocation['y'] + cpSize['height']) * 2
                    im = Image.open('./screenshot.png')
                    im = im.crop((int(x), int(y), int(width), int(height)))
                    im.save('captura.png')

                    capturaNum = captura.solve_captcha('./captura.png')

                    account = driver.find_element_by_xpath('//*[@id="UserID"]')
                    password = driver.find_element_by_xpath('//*[@id="PWD"]')
                    cpinput = driver.find_element_by_xpath('//*[@id="txtCheckCode"]')
                    loginButton = driver.find_element_by_xpath('//*[@id="login_btn"]')
                    account.send_keys(acc)
                    password.send_keys(pwd)
                    cpinput.send_keys(capturaNum)
                    print(capturaNum)

                    driver.get("http://ecsa.ntcu.edu.tw/STDWEB/SelChoose/SelChooseMain.aspx")
            except:
                pass
            courseGrade.send_keys(i[0])
            courseQuery.click()
            time.sleep(1.2)

            chooseCount = driver.find_element_by_xpath('/html/body/form/div[5]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[10]')

            s = chooseCount.text
            s = s.split('/')
            print("id", i[1], "tē", count, "Round ","上限:", s[1], '已選', s[0])
            if int(s[0]) < int(s[1]):
                addBtn = driver.find_element_by_xpath('//*[@id="td_cur_list"]/table/tbody/tr[2]/td[1]/input')
                addBtn.click()
                time.sleep(1)
                print(driver.switch_to.alert.text)
                driver.switch_to.alert.accept()
                someCourse.remove(someCourse[index])
            courseIdInput.clear()
            courseGrade.clear()
            index = index + 1
        count = count + 1
        time.sleep(5)