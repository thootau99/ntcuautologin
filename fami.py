from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import captura
from PIL import Image

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

    account = driver.find_element_by_id('UserID')
    password = driver.find_element_by_id('PWD')
    cpinput = driver.find_element_by_id('txtCheckCode')
    loginButton = driver.find_element_by_xpath('//*[@id="login_btn"]')
    acc = input("帳號: ")
    pwd = input("密碼: ")
    account.send_keys("")
    password.send_keys("")
    cpinput.send_keys(capturaNum)
    print(capturaNum)
    #TODO: Why no click loginbutton then login?

    driver.save_screenshot("screenshot1.png")

    menu = driver.find_element_by_xpath("//*[@id='ShowHeaderMenuDiv']/table/tbody/tr/td/span[2]")
    menu.click()
    enterSystem = driver.find_element_by_xpath('//*[@id="div_content"]/div[1]/div[1]/div[4]/div/div[2]/div[2]/div[1]/a')
    enterSystem.click()
    driver.save_screenshot("screenshot2.png")
    driver.close()

