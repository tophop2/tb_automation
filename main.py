# -*- coding:utf-8 -*-
from playwright.sync_api import sync_playwright
from playwright._impl._page import BindingCall, Page, Worker

def test():
    # WebSocket 地址，根据实际情况修改
    browser_ws_endpoint = 'ws://127.0.0.1:1234/devtools/browser/<your-browser-id>'

    with sync_playwright() as p:
        # 连接到已经打开的浏览器
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')

        # 获取所有已打开的页面
        pages = browser.contexts[0].pages
        p:Page=pages[0]
        # p.goto('https://taobao.com')
        # p.get_by_text('请登录').click()
        # p.get_by_text('手机号').click()
        # p.input_value('tophop')
        # print(p.content())
        res=p.locator('span:has-text("麦当劳")').first.text_content()
        print(res)
        # # 遍历每个页面并获取其 URL
        # for page in pages:
        #     print("Page URL:", page.url)
        #     page.close()
        #
        # # 关闭浏览器
        # browser.close()
if __name__ == '__main__':
    test()