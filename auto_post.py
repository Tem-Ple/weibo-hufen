# -*- coding: utf-8 -*-
# 自动转发微博
from handler import Weibo
from time import sleep

if __name__ == '__main__':
    while True:
        try:
            weibo = Weibo()
            weibo.login('13218016051', '2014070503wxh')
            hrefs = weibo.scan_hot_weibo("http://d.weibo.com")
            weibo.auto_post(hrefs)
        except Exception, e:
            print e
            weibo.close()
            continue
        weibo.close()
        print 'sleeping......'
        sleep(3600)
