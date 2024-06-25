import json
import os
import time

import playwright
from playwright.sync_api import sync_playwright, Playwright
from playwright._impl._page import BindingCall, Page, Worker
import pywinauto
import subprocess


class Window():
    pass


class Browser():

    def __init__(self):
        '''
            初始化时连接已打开浏览器endpoint
        '''
        self.connect()

    def connect(self):
        self.pl = sync_playwright().start()

        try:
            self.browser = self.pl.chromium.connect_over_cdp('http://127.0.0.1:9222')
        except:
            command = [
                r'C:\Users\SAM\AppData\Local\Google\Chrome\Application\chrome.exe',
                '--remote-debugging-port=9222'
            ]

            try:
                # 使用subprocess.Popen来启动Chrome
                process = subprocess.Popen(command)
                time.sleep(3)
                self.browser = self.pl.chromium.connect_over_cdp('http://127.0.0.1:9222')

                print("Chrome started with remote debugging on port 9222")
            except Exception as e:
                print(f"An error occurred while starting Chrome: {e}")

    def close(self):
        self.browser.close()

    def stop(self):
        self.pl.stop()


class Pages(Browser):
    def __init__(self):
        '''
            初始化时获取所有已打开页面对象
        '''
        super().__init__()
        self.pages = self.browser.contexts[0].pages
        self.page = self.get_active()

    def get(self, url: str = None, title: str = None) -> Page:
        '''
            url:通过url模糊匹配浏览器标签页url，返回页面page对象
            url:通过title模糊匹配浏览器标签页标题，返回页面page对象
        '''
        if url:
            for i in self.pages[::-1]:
                if i.url.find(url) > -1:
                    # i.bring_to_front()
                    return i

        if title:
            for i in self.pages[::-1]:
                if i.title().find(title) > -1:
                    # i.bring_to_front()

                    return i

    def get_active(self) -> Page:
        for i in self.pages[::-1]:
            # i.bring_to_front()

            return i

    def get_html(self):
        return self.page.content()


if __name__ == '__main__':
    pgs = Pages()
    # pgs.stop()
    pg = pgs.get_active()
    urls=pg.query_selector_all('.c-color-gray')
    for i in urls:
        print(i.get_text())
    # try:
    # new:Page=pg.context.new_page()
    # new.goto('https://baidu.com')
    #
    #     pg.goto('http://www.baidu.com/link?url=NUV9sfCaW0x_fa8sjL8OxziC5N7gxO-C6bHnuZ5vEpW',timeout=2)
    # except Exception as e:
    #     print(e)


