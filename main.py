# -*- coding:utf-8 -*-
from playwright.sync_api import sync_playwright
from playwright._impl._page import BindingCall, Page, Worker
from utils import *

def login_tb():
    pages = Pages()
    pg = pages.get_active()
    pg.bring_to_front()
    pg.goto('https://taobao.com', timeout=0)
    pg.locator(':text("请登录")').click(delay=3)
    pg.get_by_placeholder('账号名').fill('用户名')
    pg.get_by_placeholder('请输入登录密码').fill('密码')
    pg.locator('button', has_text='登录').click(delay=3)


def get_wangwang_messages(name):
    '''
    name: 旺旺聊天框左侧名字，模糊匹配
    '''
    pages = Pages()
    pg = pages.get(title='旺旺')
    frame = pg.frames[1]

    conversations=frame.query_selector_all('.conversation')
    for i in conversations:
        if i.text_content().find(name)>-1:
            i.click()
            tagrget=i
            break
    else:
        return
    frame.query_selector('.tpl-wrapper')
    text = frame.query_selector('.tpl-wrapper').text_content()
    shop0 = tagrget.text_content()
    print(shop0, text)


if __name__ == '__main__':
    get_wangwang_messages('mcd')
