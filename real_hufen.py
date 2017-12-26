# -*- coding: utf-8 -*-
# 批量关注
from handler import Weibo
import time

if __name__ == '__main__':
    while True:
        try:
            cnt = 0
            weibo = Weibo()
            weibo.login('13218016051', '2014070503wxh?!')
            while cnt < 100:
                cnt += weibo.real_follow('http://weibo.com/p/10080896b3c9baab600f412e89cc52a63521ee/super_index')
                print 'total cnt =', cnt
            # weibo.random_follow(["http://weibo.com/1737961042/FdoJpjguI?filter=hot&root_comment_id=0&type=comment#_rnd1500715197667"])
        except Exception, e:
            print e
        finally:
            weibo.close()
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print 'sleeping......'
            time.sleep(5555)

