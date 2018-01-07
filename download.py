from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
import sys
import shutil
from time import sleep


class App:

    def __init__(self,username,password,target_username):
        self.username = username
        self.password = password
        self.target_username = target_username
        self.driver = webdriver.Chrome('./chromedriver')
        self.main_url = "https://www.instagram.com"
        self.driver.get(self.main_url)
        self.error_flag = False
        self.login()
        if not self.error_flag:
            self.open_target_profile()
        if not self.error_flag:
            self.scroll_down()
        if not self.error_flag:
            self.download_image()
        self.driver.close()

    def login(self):
        try:
            login_button = self.driver.find_element_by_link_text("Log in")
            login_button.click()
            try:
                username_field = self.driver.find_element_by_xpath("//input[@placeholder='Phone number, username, or email']")
                username_field.send_keys(self.username)
                password_field = self.driver.find_element_by_xpath("//input[@placeholder='Password']")
                password_field.send_keys(self.password)
                password_field.submit()
                sleep(2)
                self.close_popup()
            except Exception:
                self.error_flag = True
                print('username or password field not found')
        except Exception:
            self.error_flag = True
            print('Login button not found')


    def close_popup(self):
        try:
            close_button = self.driver.find_element_by_xpath("//button[@class='_dcj9f']")
            close_button.click()
        except Exception:
            pass

    def open_target_profile(self):
        try:
            search_bar = self.driver.find_element_by_xpath("//input[@placeholder='Search']")
            search_bar.send_keys(self.target_username)
            target_url = self.main_url+'/'+self.target_username+'/'
            try:
                self.driver.get(target_url)
            except Exception:
                self.error_flag = True
                print('Target profile not found')

        except Exception:
            self.error_flag = True
            print('Search bar not found')

    def scroll_down(self):
        try:
            no_of_post = self.driver.find_element_by_xpath("//span[@class='_fd86t']")
            no_of_post = str(no_of_post.text).replace(',','')
            self.no_of_post = int(no_of_post)
            no_of_scroll = int(self.no_of_post / 12) + 3
            try:
                for value in range(no_of_scroll):
                    self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                    sleep(1)
            except Exception:
                self.error_flag = True
                print('error in scrolling')
        except Exception:
            self.error_flag = True
            print('no of post not found')

    def download_image(self):
        soup = BeautifulSoup(self.driver.page_source,'lxml')
        all_img = soup.find_all('img')
        for index,img in enumerate(all_img):
            link = img.get('src')
            file_name = 'image_'+str(index)+'.jpg'
            response = requests.get(link,stream=True)
            if not os.path.exists('./images'):
                os.mkdir('images')
            try:
                with open('./images/'+file_name,'wb') as f:
                    shutil.copyfileobj(response.raw, f)
            except Exception:
                print('Could not download image')


if __name__ == '__main__':
    arguments = sys.argv
    username = arguments[arguments.index('-u')+1]
    password = arguments[arguments.index('-p')+1]
    target = arguments[arguments.index('-t')+1]
    app = App(username,password,target)
