# author:lenglingx@gmail.com
# date:2014-12-08

# coding:utf-8

import os
import sys
import re
import urllib.request
import urllib.parse
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    '''
    网页解析生成一个HTMLParser的类，然后利用这个类，
    把给定的一个网址中所需要的地址解析并保存在该类中，
    然后利用该类的的地址，下载图片。
    '''

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        pass

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:",tag)
        if tag == "img":
            s = []
            for (variable, value) in attrs:
                s.append(value)
            # print("ss:",s)
            self.links.append(s)
            s = []
        pass

    def handle_endtag(self, tag):
        # print("Encountered a end tag:",tag)
        pass

    def handle_data(self, data):
        # print("Encountered some data:",data)
        pass


def geturl(url):
    '''
    打开给定的网页，并返回网页的内容,
    python3中来来是以字节码形式返回的，
    可以根据网页编码判定编码为gb2312,是gbk的子集，
    以字符串形式返回。
    '''
    req = urllib.request.urlopen(url)
    req = req.read()
    try:
        req = req.decode()
    except:
        req = req.decode('gbk')
    return req


def continsrc(src):
    '''
    根据网页的内容，找到我们所需要的内容，
    这里主要是有两个需要关注的内容，一个是picture标签，另一个是boxinfo标签。
    '''
    inta = src.find("<div id=\"picture\">")
    # print(inta) 所找的第一个位置点
    intb = src.find("<div class=\"boxinfo\">")
    # print(intb) 所找的第二个位置点
    content = src[inta:intb]
    return content


def pageinurl(url):
    '''
    这个是把上面的许多功能放在一个函数库里，方便操作。
    作用是给定一个url，自动去解析地址，并自动下载保存图片。
    '''
    src = geturl(url)
    content = continsrc(src)
    parser = MyHTMLParser()
    parser.feed(content)
    parser.close()
    alinks = parser.links
    for i in range(len(alinks)):
        print("filename:", alinks[i][0], "fileurl:", alinks[i][1])
        urllib.request.urlretrieve(alinks[i][1], alinks[i][0] + ".jpg")
    print("ok!!")


if __name__ == "__main__":
    print("------------------------")
    # url = "http://www.meizitu.com/a/4647.html"
    url = "http://www.meizitu.com/a/4674.html"
    src = geturl(url)

    content = continsrc(src)
    print(content)

    parser = MyHTMLParser()
    parser.feed(content)
    parser.close()

    print("------------------------------------------")
    print(parser.links)

    a = parser.links
    b = len(a)
    print(len(a))

    for i in range(b):
        print("filename:", a[i][0], "fileurl:", a[i][1])
        urllib.request.urlretrieve(a[i][1], a[i][0] + ".jpg")

    print("==================================")
    pageinurl("http://www.meizitu.com/a/4647.html")