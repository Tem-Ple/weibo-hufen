# -*- coding: utf-8 -*-
# 批量取消关注
from handler import Weibo
import time

if __name__ == '__main__':
    cnt = 0
    while True:
        try:
            weibo = Weibo()
            weibo.login('13218016051', '2014070503wxh?!')
            weibo.auto_unfollow()
            # weibo.random_follow(["http://weibo.com/1737961042/FdoJpjguI?filter=hot&root_comment_id=0&type=comment#_rnd1500715197667"])
        except Exception, e:
            print e
        finally:
            weibo.close()
            time.sleep(3600)

