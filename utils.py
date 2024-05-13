import playwright
from playwright.sync_api import sync_playwright, Playwright
from playwright._impl._page import BindingCall, Page, Worker


class Broswer():

    def __init__(self):
        '''
            初始化时连接已打开浏览器endpoint
        '''
        self.pl = sync_playwright().start()
        self.broswer = self.pl.chromium.connect_over_cdp('http://127.0.0.1:9222')

    def close(self):
        self.broswer.close()

    def stop(self):
        self.pl.stop()


class Pages(Broswer):
    def __init__(self):
        '''
            初始化时获取所有已打开页面对象
        '''
        super().__init__()
        self.pages = self.broswer.contexts[0].pages

    def get(self, url: str = None, title: str = None) -> Page:
        '''
            url:通过url模糊匹配浏览器标签页url，返回页面page对象
            url:通过title模糊匹配浏览器标签页标题，返回页面page对象
        '''
        if url:
            for i in self.pages[::-1]:
                if i.url.find(url) > -1:
                    i.bring_to_front()
                    return i

        if title:
            for i in self.pages[::-1]:
                if i.title().find(title) > -1:
                    i.bring_to_front()

                    return i
    def get_active(self)-> Page:
        for i in self.pages[::-1]:
            i.bring_to_front()

            return i

if __name__ == '__main__':
    pgs = Pages()
    res = pgs.get(title='淘宝')

    print(res.title())
