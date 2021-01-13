from selenium import webdriver
from time import sleep
from Checker import checker
from creds import Fb_user,Fb_pass
import re

# Your chrome driver path
chromedriverpath = "chromedriver"

class bot():
    def __init__(self):
        if Fb_pass == "" or Fb_user == "" or chromedriverpath == "":
            print("Set FaceBook user name and password to login ! ")
            print(
                "! You should have a Tinder account with Facebook if not create one First")

        else:
            self.chrome_options = webdriver.ChromeOptions()
            self.prefs = {
                "profile.default_content_setting_values.notifications": 2}
            self.chrome_options.add_experimental_option("prefs", self.prefs)
            self.driver = webdriver.Chrome(
                executable_path=chromedriverpath, options=self.chrome_options)


    def login(self):
        self.driver.maximize_window()
        self.driver.get('https://tinder.com')
        sleep(2)

        # Accept button
        self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[2]/div/div/div[1]/button').click()

        # login button
        sleep(3)
        self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/button').click()

        sleep(3)

        try:
            # more options button
            moreoptions = self.driver.find_element_by_xpath(
                '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/button').click()
        except:
            pass
        # fb login button
         
        fblogin = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button').click()
        
        sleep(2)

        workspace = self.driver.window_handles[0]
        popup = self.driver.window_handles[1]
        self.driver._switch_to.window(popup)

        sleep(2)
        # setting email 
        email_fb = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_fb.send_keys(Fb_user)
        # setting password
        passwd_fb = self.driver.find_element_by_xpath('//*[@id="pass"]')
        passwd_fb.send_keys(Fb_pass)

        # fb login
        loing_fb = self.driver.find_element_by_xpath(
            '//*[@id="u_0_0"]').click()
        sleep(3)

        # back to tinder window
        self.driver.switch_to.window(workspace)
        sleep(2)


    def like(self):
        sleep(2)
        like = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like.click()
        sleep(1)

    def dislike(self):
        sleep(2)
        dislike = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')
        dislike.click()
        sleep(1)

    def sendmsg(self):
        textbox = self.driver.find_element_by_xpath(
            '//*[@id="chat-text-area"]')
        textbox.send_keys('Hey Cutie,:)')
        sleep(2)
        # message sent, not tested yet
        sendmsg = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[3]/form/button')
        sendmsg.click()
        sleep(2)

    def getpiclink(self):
        # from the page code get link to main pic using regex
        sleep(1)
        pic_regex = r"&quot;(https://images-ssl.gotinder.com/[\w]+/640x(?:\S)+)&quot"
        match = re.findall(pic_regex,self.driver.page_source)
        return match[1]

    def notintersted(self):
        sleep(1)
        self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div[2]/button[2]').click()


def main():
    
    try:
        b = bot()
        b.login()
    except:
        print("Error during Login")

    for i in range(50):
        try:
            b.driver.refresh()
            sleep(10)
            link = b.getpiclink()
            result = checker(link)
            sleep(1)
            print("result ", result)
            if result == 1:
                b.like()
            else:
                b.dislike()
            sleep(2)
        except:
            try:
            # No thanks
                b.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/button[2]').click()
            except Exception as e:
                try:
                    b.sendmsg()
                except:
                    b.notintersted()

if __name__ == "__main__":
    main()
