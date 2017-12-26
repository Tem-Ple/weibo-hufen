# -*- coding: utf-8 -*-
# 自动评论并回粉
from handler import Weibo
from time import sleep

if __name__ == '__main__':
    weibo = Weibo()
    weibo.login('13218016051', '2014070503wxh')
    while True:
        try:
            weibo.auto_comment()
        except Exception, e:
            print e
        sleep(3000)
