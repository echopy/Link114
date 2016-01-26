# coding: utf-8
# QueryAPI.py
# Created by Bayonet on 2016/1/22.

import requests
import re
from lxml import etree
import time
import socket
import MySQLdb


class API():
    def __init__(self, url):
        self.url = url
        self.end = ''

    def GetTitle(self):
        start = time.clock()
        req = requests.get(url='http://' + self.url)
        if req.status_code == 200:
            html = etree.HTML(req.content)
            try:
                title = html.xpath('//title/text()')[0]
                return title
            except IndexError:
                return None
            finally:
                self.end = time.clock() - start

    def BaiduSL(self):
        req = requests.get("http://www.baidu.com/s?wd=site:" + self.url)
        if req.status_code == 200:
            try:
                return re.findall(u'找到相关结果数约(.*?)个', req.text)[0].replace(',', '')
            except IndexError:
                try:
                    return re.findall('<b style="color:#333">(.*?)</b>', req.text)[0].replace(',', '')
                except IndexError:
                    return 0

    def get_ip_address(self):
        """
        :return: 根据URL 来获取 IP地址
        """
        try:
            return socket.gethostbyname(self.url)
        except socket.error, err_msg:
            print 'HostName: %s ErrorInfo: %s' % (self.url, err_msg)
            return '获取失败'

    def run(self):
        self.GetTitle()
        ip = self.get_ip_address()
        return {'ym': self.url, 'bt': self.GetTitle(), 'qz': '', 'sl': self.BaiduSL(), 'xy': round(self.end, 2),
                'jz': '', 'ip': ip}


def get_title(url):
    """
    According to URL get the site title
    :param url: DomainName
    :return: DomainName Title, Program Run Time or Exception:  '标题获取失败' , 0.0
    """
    start = time.clock()
    req = requests.get(url='http://' + url)
    if req.status_code == 200:
        html = etree.HTML(req.content)
        # 计算代码块运行时间
        end = time.clock() - start
        try:
            title = html.xpath('//title/text()')[0]
        except IndexError:
            title = u'标题获取失败'
            end = 0.0
        finally:
            return title, end


def baidu_sl(url):
    """
    According to URL get Baidu collected
    :param url:
    :return:
    """
    req = requests.get("http://www.baidu.com/s?wd=site:" + url)
    if req.status_code == 200:
        try:
            return re.findall(u'找到相关结果数约(.*?)个', req.text)[0].replace(',', '')
        except IndexError:
            try:
                return re.findall('<b style="color:#333">(.*?)</b>', req.text)[0].replace(',', '')
            except IndexError:
                return 0.0


def get_ip_address(url):
    """
    :param url:
    :return: 根据URL 来获取 IP地址
    """
    try:
        return socket.gethostbyaddr(url)
    except socket.error, err_msg:
        print 'HostName: %s ErrorInfo: %s' % (url, err_msg)
        return '获取失败'


class Data_Access():
    """
    数据入库
    """
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='', db='query', charset='utf8')
    cursor = conn.cursor()

    def __init__(self, url):
        self._url = url

    def insert_data(self):
        """
        向数据库中插入一个数据
        """
        pass
