# -*- coding:utf-8 -*-
from playwright.sync_api import sync_playwright
from playwright._impl._page import BindingCall, Page, Worker
from utils import *


def test():
    # WebSocket 地址，根据实际情况修改
    browser_ws_endpoint = 'ws://127.0.0.1:1234/devtools/browser/<your-browser-id>'

    with sync_playwright() as p:
        # 连接到已经打开的浏览器
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')

        # 获取所有已打开的页面
        pages = browser.contexts[0].pages
        p: Page = pages[0]
        p.goto(url='https://taobao.com')
        # p.wait_for_event('load')
        # p.wai
        p.get_by_text('请登录').click()
        p.get_by_placeholder('手机号').click()
        p.input_value('tophop')
        # print(p.content())
        # res=p.locator('span:has-text("麦当劳")').first.text_content()
        # print(res)
        # # 遍历每个页面并获取其 URL
        # for page in pages:
        #     print("Page URL:", page.url)
        #     page.close()
        #
        # # 关闭浏览器
        # browser.close()


def login_tb():
    pages = Pages()
    pg = pages.get_active()
    pg.bring_to_front()
    pg.goto('https://taobao.com', timeout=0)
    pg.locator(':text("请登录")').click(delay=3)
    pg.get_by_placeholder('账号名').fill('用户名')
    pg.get_by_placeholder('请输入登录密码').fill('密码')
    pg.locator('button', has_text='登录').click(delay=3)


def get_wangwang_messages():
    pages = Pages()
    pg = pages.get(title='旺旺')
    pg.locator(':text("麦当劳")').first.click()
    chat_list = pg.locator('.desc').all()
    for i in chat_list:
        print(i.text)


if __name__ == '__main__':
    login_tb()
