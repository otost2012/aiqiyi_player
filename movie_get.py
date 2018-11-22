"""
VIP视频解析：http://www.vipjiexi.com/
无名小站：http://www.wmxz.wang/
http://www.iqiyi.com/lib/dianying/%E5%96%9C%E5%89%A7,%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86,2018_11_1.html
"""

import requests
import re
import os
from lxml import etree
from  selenium import webdriver



class Pro:
    header_ai={'Referer': 'http://www.iqiyi.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.17 Safari/537.36'

    }
    header_you={'Referer': 'http://list.youku.com/category/video','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    header_pp = {'Referer': 'http://list.pptv.com/',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    way=False
    def __init__(self):
        pass

    def search_movies_type(self,u_name,u_type,page):#两个参数 根据状态输出规则
        dic1 = {'m': 1, 't': 2, 'z': 6, 'd': 4, 'j': 3}
        dic2 = {'m': 96, 't': 97, 'z': 85, 'd': 100, 'j': 84}
        dic3 = {'m': 1, 't': 2, 'z': 4, 'd': 3, 'j': 210548}
        headers={}
        #爱奇艺 a/电影m:1 t:2 z:6 d:4 j:3  优酷y / m:96 t:97 z:85 d:100 j:84 pptv  p/m:1 t:2 z:4 d:3 j:210548
        url, pa_movie_title, pa_movie_url, pa_move_pic='','','',''
        url_aiqiyi='http://list.iqiyi.com/www/{}/-------------24-{}-1-iqiyi--.html'.format(dic1[u_type],page)
        url_youku='https://list.youku.com/category/show/c_{}_s_1_d_1_p_{}.html'.format(dic2[u_type],page)
        # url_pptv='http://list.pptv.com/category/type_{}.html'.format(dic3[u_type])
        url_pptv='http://list.pptv.com/channel_list.html?page={}&type={}'.format(page,dic3[u_type])
        pa_ai_movie_title = '//div[@class="site-piclist_pic"]/a[@class="site-piclist_pic_link"]/@title'
        pa_ai_movie_url = '//div[@class="site-piclist_pic"]/a[@class="site-piclist_pic_link"]/@href'
        pa_ai_movie_pic = '//div[@class="site-piclist_pic"]/a[@class="site-piclist_pic_link"]/img/@src'
        pa_you_movie_title='//div[@class="p-thumb"]/a/@title'
        pa_you_movie_url='//div[@class="p-thumb"]/a/@href'
        pa_you_movie_pic='//div[@class="p-thumb"]/img[@class="quic"]/@src'
        pa_pp_movie_title='//li/a[@class="ui-list-ct"]/@title'
        pa_pp_movie_url='//li/a[@class="ui-list-ct"]/@href'
        pa_pp_movie_pic='//li/a[@class="ui-list-ct"]/p[@class="ui-pic"]/img/@data-src2'
        if u_name=="a":#如果是爱奇艺
            url=url_aiqiyi
            pa_movie_title=pa_ai_movie_title
            pa_movie_url=pa_ai_movie_url
            pa_move_pic=pa_ai_movie_pic
            headers=self.header_ai
        elif u_name=="y":#如果是优酷
            url=url_youku
            pa_movie_title=pa_you_movie_title
            pa_movie_url=pa_you_movie_url
            pa_move_pic=pa_you_movie_pic
            headers=self.header_you

        elif u_name=="p":#如果是PPTV
            url=url_pptv
            pa_movie_title=pa_pp_movie_title
            pa_movie_url=pa_pp_movie_url
            pa_move_pic=pa_pp_movie_pic
            headers=self.header_pp

        return url,pa_movie_title,pa_movie_url,pa_move_pic,headers


    def get_movie_res(self,u_name,u_type,page):#输出电影名 链接 图片
        url, pa_movie_title, pa_movie_url, pa_move_pic,headers=self.search_movies_type(u_name,u_type,page)
        res=requests.get(url=url,headers=headers).content.decode('utf-8')
        # print(res)
        html=etree.HTML(res)
        movie_url=html.xpath(pa_movie_url)
        movie_title=html.xpath(pa_movie_title)
        movie_src_pic=html.xpath(pa_move_pic)
        print(len(movie_title),movie_title)
        print(len(movie_url),movie_url)
        print(len(movie_src_pic),movie_src_pic)
        return movie_url,movie_title,movie_src_pic

    def change_urlink(self,lis):
        for i in range(len(lis)):
            if '\\' in lis[i]:
                lis[i] = lis[i].replace('\\', '')
        # print(lis)
        return lis

    def change_youku_link(self,urls):
        pa_link='//.+[.]html'
        if re.match(pa_link,urls):
            urls='http:'+urls
        return urls

    def get_more_tv_urls(self,url,u_name,u_type):#获取电视剧分集链接
        tv_dic_new = {}
        if u_name == 'y':
            url=self.change_youku_link(url)
            res = requests.get(url, headers=self.header_you).text.encode(encoding='utf-8').decode('utf-8')
            html = etree.HTML(res)
            print(res)
            if u_type=="m" or u_type=="t":
                self.tv_more_title = html.xpath('//div[@class="item item-num"]/@title')
                self.tv_more_url = html.xpath('//div[@class="item item-num"]/a[@class="sn"]/@href')
            elif u_type=="d":
                self.tv_more_title = html.xpath('//div[@class="item item-txt"]/@title')
                self.tv_more_url = html.xpath('//div[@class="item item-txt"]/a[@class="sn"]/@href')
            elif u_type=="z":
                self.tv_more_title = html.xpath('//div[@class="item item-cover"]/@title')
                self.tv_more_url = html.xpath('//div[@class="item item-cover"]/a/@href')
            elif u_type == "j":
                self.tv_more_title = html.xpath('//div[@class="item item-cover current"]/@title')
                self.tv_more_url = html.xpath('//div[@class="item item-cover current"]/a/@href')
        elif u_name == 'a':
            res = requests.get(url, headers=self.header_ai).text.encode(encoding='utf-8').decode('utf-8')
            html = etree.HTML(res)
            print(res)
            if u_type=="m" or u_type=="t" or u_type=='d':
                self.tv_more_title = html.xpath(
                    '//ul/li[@data-albumlist-elem="playItem"]/div[@class="site-piclist_pic"]/a[1]/@title')
                self.tv_more_url = html.xpath(
                    '//ul/li[@data-albumlist-elem="playItem"]/div[@class="site-piclist_pic"]/a[1]/@href')
            elif u_type=="z" or u_type=="j":
                self.tv_more_title = html.xpath('//div[@class="recoAlbumTit"]/a[1]/@title')
                self.tv_more_url = html.xpath('//div[@class="recoAlbumTit"]/a[1]/@href')
        elif u_name == 'p':
            res = requests.get(url, headers=self.header_pp).text.encode(encoding='utf-8').decode('utf-8')
            # html = etree.HTML(res)
            self.tv_more_url2 = re.compile('{"url":"(.+?)"').findall(res)
            self.tv_more_url = self.change_urlink(self.tv_more_url2)
            self.tv_more_title = ["第{}集".format(x) for x in range(1, len(self.tv_more_url) + 1)]
        for i, j in zip(self.tv_more_title, self.tv_more_url):
            tv_dic_new[i] = j
        print(len(self.tv_more_title), self.tv_more_title)
        print(len(self.tv_more_url), self.tv_more_url)
        print(tv_dic_new)
        return tv_dic_new

    def url_change(self,url,flag):
        pa_url='http://www.iqiyi.com/a_[.+].html'
        if flag=="0":#通道1
            if re.match(pa_url, url):
                _url = url.replace('a', 'v')
            else:
                _url=url
            # new_url='http://www.wq114.org/weixin.php?url={}'.format(_url[21:])
            new_url='http://www.wq114.org/weixin.php?url={}'.format(_url)
            return new_url
        elif flag == "1":
            if re.match(pa_url, url):
                _url = url.replace('a', 'v')
            else:
                _url = url
            new_url='http://www.wmxz.wang/video.php?url={}'.format(_url)
            return new_url


    def play_movie(self,url,flag):
        play_url=self.url_change(url,flag)
        print('播放地址:',play_url)
        web = webdriver.Chrome()
        web.get(play_url)


if __name__ == '__main__':
    p=Pro()
    # http://www.iqiyi.com/a_19rrh1ncud.html#vfrm=2-4-0-1'
    #//v.youku.com/v_show/id_XMzcyMTIyMTE4MA==.html
    #http://v.pptv.com/show/1RD9eibNJufda2EA.html?rcc_src=L1
    # p.play_movie('http://v.pptv.com/show/yfmwL5f9basOjPQ.html?rcc_src=P4&spm=movie_index_web.sb_2719422.0.1.0.1.0.0.0.0')
    # p.search_movies_id('扶摇')
    # p.get_more_tv_urls('http://v.youku.com/v_show/id_XMzcyMTIyMTE4MA==.html','y')
    # p.get_more_tv_urls('http://www.iqiyi.com/a_19rrh1ncud.html#vfrm=2-4-0-1','a')
    # p.get_more_tv_urls('http://www.iqiyi.com/a_19rrguaab9.html#vfrm=2-4-0-1', 'a','j')
    p.play_movie('https://v.youku.com/v_show/id_XMzcxODEzMDMzNg==.html','0')
    # p.get_movie_res('p','t')
    #https://v.youku.com/v_show/id_XMzYzNDYyNzcyOA==.html
    #http://www.wq114.org/weixin.php?url=https%3A%2F%2Fv.youku.com%2Fv_show%2Fid_XMzYzNDYyNzcyOA%3D%3D.html
    #http://www.iqiyi.com/v_19rre4cfyg.html
    #http://www.wq114.org/weixin.php?url=http%3A%2F%2Fwww.iqiyi.com%2Fv_19rre4cfyg.html