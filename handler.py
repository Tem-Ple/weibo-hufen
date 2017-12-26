# -*- coding: utf-8 -*-
import time
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Weibo:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
        except Exception, e:
            print e
        try:
            self.driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
        except Exception, e:
            print e
        #self.driver = webdriver.PhantomJS(executable_path="E:/weibo/app/phantomjs.exe")
        self.driver.implicitly_wait(10)

    def login(self, username, password):
        # print 'get weibo'
        self.driver.get("http://weibo.com/")
        # print 'click'
        self.driver.find_element_by_id("loginname").click()
        # print 'send key'
        self.driver.find_element_by_id("loginname").send_keys(username)
        time.sleep(1) #防止出现验证码
        self.driver.find_element_by_css_selector("span.enter_psw").click()
        self.driver.find_element_by_name("password").clear()
        self.driver.find_element_by_name("password").send_keys(password)
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@id='pl_login_form']/div/div[3]/div[6]/a/span").click()
        print 'login successfully'

    def close(self):
        self.driver.quit()

    def scan_hot_weibo(self, url):
        self.driver.get(url)
        hot_weibo_hrefs = []
        for i in xrange(1, 10):
            try:
                comments = self.driver\
                    .find_element_by_xpath(
                        "//div[@id='Pl_Core_NewMixFeed__3']/div/div[2]/div{num}/div[2]/div/ul/li[3]/a/span/span/span/em[2]"
                        .format(num='' if i == 1 else '[' + str(i) + ']'))
                print comments.text
                if int(comments.text) < 20:
                    continue
                comments.click()
                time.sleep(2)

                hot_weibo_hrefs.append(
                    self.driver.find_element_by_xpath(
                            "//div[@id='Pl_Core_NewMixFeed__3']/div/div[2]/div{num}/div[3]/div/div/div[2]/div[2]/div/a"
                            .format(num='' if i == 1 else '[' + str(i) + ']')
                    ).get_attribute('href')
                )
            except Exception, e:
                print e
        return hot_weibo_hrefs

    def auto_post(self, hrefs):
        for href in hrefs:
            self.driver.get(href)
            origin_text = self.driver\
                .find_element_by_css_selector('div.WB_text').text
            print origin_text
            with open("posted_weibos.txt", "r+") as f:
                origin_texts = [mystr.strip() for mystr in f.readlines()]
                if origin_text not in origin_texts:
                    f.write(origin_text+'\n')
                else:
                    self.driver.close()
                    self.driver.switch_to_window(self.driver.window_handles[0])
                    continue
            my_text = self.driver\
                .find_element_by_css_selector('div.list_ul[node-type="comment_list"]')\
                .find_element_by_css_selector('div.WB_text').text
            my_text = my_text.split("：")[1].split("¡")[0]
            self.driver.execute_script("document.getElementsByClassName('WB_feed_handle')[0].getElementsByTagName('span')[3].click()")
            self.driver.find_element_by_css_selector("div.p_input.p_textarea > textarea.W_input").send_keys(
                "[doge][doge]")
            self.driver.find_element_by_link_text(u"转发").click()
            time.sleep(3)
            break

    def random_follow(self, hrefs):
        cnt = 0
        for href in hrefs:
            href = href.split("?")[0]
            print href
            self.driver.get(href)
            time.sleep(5)
            try:
                self.driver.find_element_by_link_text(u"按时间").click()
                time.sleep(1)
            except Exception, e:
                print e
                print "order by time failed!"

            comment_roots = self.driver.find_elements_by_css_selector("div.list_li.S_line1.clearfix")
            for comment_num in xrange(15):
                try:
                    self.driver.execute_script(
                        'document.getElementsByClassName("list_ul")[0].getElementsByClassName("WB_face W_fl")[{num}].getElementsByTagName("a")[0].click()'.format(num=comment_num))
                except Exception, e:
                    print e
                    continue
                time.sleep(3)
                self.driver.switch_to_window(self.driver.window_handles[-1])

                sex = 'W_icon icon_pf_male'
                #判断性别
                try:
                    sex = self.driver.find_element_by_css_selector("div.pf_username").find_element_by_tag_name("i").get_attribute("class")
                except Exception, e:
                    print e
                    print "get gender failed"

                strongs_flag = False
                # 判断粉丝数
                try:
                    strongs = self.driver.find_element_by_class_name('PCD_counter').find_elements_by_tag_name('strong')
                    flo = int(strongs[0].text)
                    fan = int(strongs[1].text)
                    print 'flo:', flo, ' fan:', fan
                    strongs_flag = True if flo > fan else False
                except Exception, e:
                    print e
                    print "get strongs failed"

                if sex != 'W_icon icon_pf_male' and strongs_flag:
                    try:
                        self.driver.execute_script('document.getElementsByClassName("WB_row_line WB_row_r4 clearfix S_line2")[0].getElementsByTagName("li")[3].getElementsByTagName("em")[0].click()')
                        # 点赞
                        time.sleep(1)
                        self.driver.execute_script('document.getElementsByClassName("opt_box clearfix")[0].getElementsByTagName("a")[0].click()')
                        # 关注
                        print "follow success"
                        cnt += 1
                        print 'single cnt =',cnt
                        time.sleep(3)
                    except Exception, e:
                        print e
                        print "follow failed"
                self.driver.close()
                self.driver.switch_to_window(self.driver.window_handles[0])
        return cnt

    def real_follow(self, href):
        cnt = 0
        self.driver.get(href)
        time.sleep(5)

        for comment_num in xrange(10):
            try:
                self.driver.execute_script(
                    "document.getElementsByClassName('W_face_radius')[{num}].click()".format(num=comment_num*3+2))
            except Exception, e:
                print e
                continue
            time.sleep(3)
            self.driver.switch_to_window(self.driver.window_handles[-1])

            # sex = 'W_icon icon_pf_male'
            # #判断性别
            # try:
            #     sex = self.driver.find_element_by_css_selector("div.pf_username").find_element_by_tag_name("i").get_attribute("class")
            # except Exception, e:
            #     print e
            #     print "get gender failed"

            strongs_flag = False
            # 判断粉丝数
            try:
                strongs = self.driver.find_element_by_class_name('PCD_counter').find_elements_by_tag_name('strong')
                flo = int(strongs[0].text)
                fan = int(strongs[1].text)
                print 'flo:', flo, ' fan:', fan*0.5
                strongs_flag = True if flo > fan*0.5 else False
            except Exception, e:
                print e
                print "get strongs failed"

            is_followed = True
            #判断是否已关注
            try:
                followed = self.driver.find_element_by_css_selector('div.opt_box.clearfix')\
                    .find_element_by_tag_name('a').text
                print followed
                if followed == u'+关注':
                    is_followed = False
            except Exception, e:
                print e
                print "get is_followed failed!"

            if strongs_flag and not is_followed:
                try:
                    # self.driver.execute_script('document.getElementsByClassName("WB_row_line WB_row_r4 clearfix S_line2")[0].getElementsByTagName("li")[3].getElementsByTagName("em")[0].click()')
                    # 点赞
                    time.sleep(1)
                    self.driver.execute_script('document.getElementsByClassName("opt_box clearfix")[0].getElementsByTagName("a")[0].click()')
                    # 关注
                    print "follow success"
                    cnt += 1
                    print 'single cnt =', cnt
                    time.sleep(3)
                except Exception, e:
                    print e
                    print "follow failed"
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])
        return cnt

    def auto_refollow(self):
        self.driver.implicitly_wait(3)
        self.driver.get('http://weibo.com/p/1005052749672122/myfollow?relate=fans#place')
        try:
            # 把悬浮物去掉
            self.driver.execute_script(
                'document.getElementsByClassName("WB_global_nav WB_global_nav_v2 UI_top_hidden ")[0].style.display = "none"')
            time.sleep(1)
            self.driver.execute_script(
                'document.getElementsByClassName("webim_fold clearfix")[0].style.visibility= "hidden"')
            time.sleep(1)
        except Exception, e:
            print e
        follow_bottons = self.driver.find_elements_by_link_text(u"Y+关注")
        print follow_bottons
        for follow_botton in follow_bottons:
            follow_botton.click()
            time.sleep(3)
            self.driver.find_element_by_link_text("X").click()
        self.driver.implicitly_wait(10)

    def auto_unfollow(self):
        self.driver.implicitly_wait(3)
        cnt = 0
        for page_num in xrange(20, 300):
            if cnt > 100:
                break
            self.driver.get('http://weibo.com/p/1005052749672122/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__93_page={num}#Pl_Official_RelationMyfollow__93'.format(num=page_num))
            try:
                # 把悬浮物去掉
                self.driver.execute_script(
                    'document.getElementsByClassName("WB_global_nav WB_global_nav_v2 UI_top_hidden ")[0].style.display = "none"')
                time.sleep(1)
                self.driver.execute_script(
                    'document.getElementsByClassName("webim_fold clearfix")[0].style.visibility= "hidden"')
                time.sleep(1)
                self.driver.execute_script(
                    'document.getElementsByClassName("opt_bar clearfix S_bg2")[0].style.display="none"'
                )
                time.sleep(1)
            except Exception, e:
                print e

            #遍历所有人
            all_people = self.driver.find_elements_by_css_selector('div.member_wrap.clearfix')
            for people in all_people:
                try:
                    statu = people.find_element_by_css_selector('div.statu').find_element_by_tag_name('span').text
                    groupname = people.find_element_by_css_selector('span[node-type="groupName"]').text
                    # 点击取关
                    print statu, groupname
                    if statu == u'已关注' and groupname == u'未分组':
                        self.driver.execute_script(
                            'var q=document.getElementsByClassName("layer_menu_list"); for(i = 1; i < q.length; i++)  q[i].style.display = ""')
                        time.sleep(1)
                        people.find_element_by_css_selector('a[action-type="cancel_follow_single"]').click()
                        time.sleep(1)
                        self.driver.find_element_by_link_text(u"确定").click()
                        time.sleep(1)
                        cnt += 1
                        print statu, groupname, 'unfollow success!  cnt =', cnt
                except Exception, e:
                    print e
        self.driver.implicitly_wait(10)

    def auto_comment(self):
        self.driver.get("http://d.weibo.com")
        for i in xrange(10):
            try:
                self.driver.execute_script(
                        'document.getElementsByClassName("WB_row_line WB_row_r4 clearfix S_line2")[{num}].getElementsByTagName("a")[2].click()'
                        .format(num=i))
                time.sleep(2)
            except Exception, e:
                print e
                continue

            try:
                self.driver.find_element_by_css_selector("textarea.W_input").clear()
                self.driver.find_element_by_css_selector("textarea.W_input").send_keys(unicode("关注我的 10秒之内 如果我没回粉 请取关 算我输 就是这么自信[doge]"+time.strftime('%Y-%m-%d %X', time.localtime()), errors='ignore'))
                time.sleep(2)
                self.driver.find_element_by_link_text(u"评论").click()
                time.sleep(2)
                self.driver.execute_script('document.getElementsByClassName("WB_handle W_fr")[0].getElementsByTagName("a")[2].click()')
                time.sleep(2)
            except Exception, e:
                print e

            try:
                self.driver.execute_script(
                        'document.getElementsByClassName("WB_row_line WB_row_r4 clearfix S_line2")[{num}].getElementsByTagName("a")[2].click()'
                        .format(num=i))
                time.sleep(2)
            except Exception, e:
                print e
