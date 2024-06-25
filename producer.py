# -*- coding:utf-8 -*-
import concurrent
import json
import threading

import pywinauto
from playwright.sync_api import sync_playwright
from playwright._impl._page import BindingCall, Page, Worker
from utils import *
import re
from urllib import parse
import copy
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

a = ''


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

    conversations = frame.query_selector_all('.conversation')
    for i in conversations:
        if i.text_content().find(name) > -1:
            i.click()
            tagrget = i
            break
    else:
        return
    frame.query_selector('.tpl-wrapper')
    text = frame.query_selector('.tpl-wrapper').text_content()
    shop0 = tagrget.text_content()
    print(shop0, text)


def get_shop_products():
    pg = Pages().get_active()
    # pg.reload()

    pg.on("request", lambda request: print(">>", request.method, request.url))
    try:
        pg.on("response", lambda response: parse_response(response))
    except:
        pass
    pg.reload()


def parse_response(res):
    try:
        print(res.json())
    except:
        pass


def test_win():
    app = pywinauto.Application().connect(handle=395548)
    app.active()


done = []
d = {}

filter_urls = set()


def check_exists(d):
    if not os.path.exists('urls.json'):
        with open('urls.json', 'w') as f:
            f.write('')
    with open('urls.json', 'r') as f:
        content = f.read()
        if content:
            res = json.loads(content)
        else:
            res = {}
    if res.get(d['url']):
        return True
    with open('urls.json', 'w') as f:
        res.update({d['url']: d['email']})
        f.write(json.dumps(res))


def test_spider(pg, base_url):
    try:
        pg.goto(base_url)
        html = pg.content()

    except Exception as e:
        print(e)
        return
    # print(html)
    urls = re.findall('href="(http.*?)"', html)
    global filter_urls
    [filter_urls.add(i) for i in urls if not i.find(base_url) > -1 and len(parse.urlparse(i).path) < 2]
    # print(filter_urls)
    emails = re.findall('\w+@\w+.com', html)
    d.update({base_url: emails})

    print({base_url: emails})
    if filter_urls:
        for j in filter_urls:
            if check_exists({'url': base_url, 'email': emails}):
                continue
            if len(parse.urlparse(j).path) > 2:
                continue

            test_spider(pg, j)


def get_url(html, flag):
    res = set()
    urls = re.findall('href="(http.*?)"', html)
    global filter_urls
    [res.add(i) for i in urls if i.find('link') > -1]

    return res


def get_link(base_url, html):
    filters = set()
    urls = re.findall('href="(http.*?)"', html)
    [filters.add(i) for i in urls if not i.find(base_url) > -1 and len(parse.urlparse(i).path) < 2]
    return filters


def write_file(content):
    # with open('urls.json','r') as f:
    #     f.write(json.dumps(content))
    if not content:
        return
    with open('urls.json', 'a') as f:
        f.writelines(json.dumps(list(content)))


def get_email(url, html):
    try:
        # html = pg.content()
        emails = re.findall('\w+@\w+.com', html)
        print({url: emails})
    except:
        pass


def search_in_se(pg, keyword):
    base_url = 'baidu.com'
    # new = pg.
    try:
        pg.goto('https://www.baidu.com/s?wd=%s' % keyword)
    except Exception as e:
        print(1, e)
        pg.go_back()
    while pg.get_by_text('下一页'):
        pg.get_by_text('下一页').click()
        html = pg.content()
        res = copy.deepcopy(get_url(html, 'link'))
        threads = []
        # with concurrent.futures.ThreadPoolExecutor(2) as f:
        #     for i in res:
        #         # f.submit(task, (i, html, pg))
        #         f.map(task, *zip(*[(i, html, pg), ]))
        #         # f.map(task2, [(1, 2, 3), ])
        # with ThreadPoolExecutor(3) as future:
        #     args = [(i, html, pg) for i in res]
        #     future.map(task, *args)
        # [future.map(task, [i, html, pg]) for i in res]
        for i in res:
            threads.append(threading.Thread(target=task(i, html,pg)))
        for t in threads:
            t.start()

    # while 1:


def task2(a, b, c):
    print(a, b, c)


def task(url, html, pg):
    try:
        new_page: Page = pg.context.new_page()
        new_page.goto(url)
        host = parse.urlparse(new_page.url).hostname
        # print(host)
        if any(list(
                filter(lambda x: host.find(x) > -1, ['iqiyi', 'baidu', 'haokan', '360', 'bilibili', 'youku']))):
            new_page.close()
            return
        # global filter_urls
        # filter_urls.remove(url)
        get_email(host, html)
        write_file(get_link(host, html))
        new_page.close()
    except Exception as e:
        print(e)
        new_page.close()


if __name__ == '__main__':
    # get_shop_products()
    context = Pages()
    pg = context.get_active()
    search_in_se(pg, '')
    # while 1:
    #     try:
    #
    #         if not filter_urls:
    #             test_spider(pg, 'https://1.com')
    #         else:
    #             for f in set(filter_urls):
    #                 test_spider(pg, f)
    #     except Exception as e:
    #         print(e)
    #
    #         pg.close()
    #         context.stop()
    #         context = Pages()
    #         pg = context.get_active()
