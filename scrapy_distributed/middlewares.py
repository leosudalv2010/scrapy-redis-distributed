# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse


class SeleniumMiddleware(object):
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable--gpu')
        self.driver = selenium.webdriver.Chrome(chrome_options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.maximize_window()

    def __del__(self):
        self.driver.quit()

    def process_request(self, request, spider):
        """
        Make use of the webdriver to simulate the webpage scrolling in order to load
        the complete information of the webpage (sinse Ajax is used for the webpage).
        """
        try:
            self.driver.get(request.url)
            self.wait.until(EC.presence_of_element_located((By.XPATH,
                '//div[@id="J_goodsList"]/ul/li//div[@class="p-shop"]/span/a')))
            for i in range(5):
                self.wait.until(EC.presence_of_element_located((By.XPATH,
                    '//div[@id="J_goodsList"]/ul/li//div[@class="p-shop"]/span/a')))
                items = len(self.driver.find_elements_by_xpath(
                    '//div[@id="J_main"]/div[@class="m-list"]//div[@id="J_goodsList"]/ul/li'))
                if items > 50 or i == 4:
                    break
                self.driver.execute_script('window.scrollBy(0,3000)')  # webpage scrolling
                self.driver.save_screenshot('shot{}.png'.format(i))
            if i < 4:
                return HtmlResponse(url=request.url, status=200,
                                    body=self.driver.page_source, request=request, encoding='utf-8')
            else:
                raise TimeoutException
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)


