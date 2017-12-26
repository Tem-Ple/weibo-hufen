# -*- coding: utf-8 -*-
# 批量关注
from handler import Weibo
import time

if __name__ == '__main__':
    cnt = 0
    while True:
        try:
            weibo = Weibo()
            weibo.login('13218016051', '2014070503wxh')
            hrefs = weibo.scan_hot_weibo("http://d.weibo.com")
            cnt += weibo.random_follow(hrefs)
            print 'total cnt =', cnt
            # weibo.random_follow(["http://weibo.com/1737961042/FdoJpjguI?filter=hot&root_comment_id=0&type=comment#_rnd1500715197667"])
        except Exception, e:
            print e
        finally:
            weibo.close()
            if cnt >= 100:
                cnt = 0
                print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print 'sleeping......'
                time.sleep(4444)

