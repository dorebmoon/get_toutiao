import requests
from pyquery import PyQuery as pq
import os
from hashlib import md5
from urllib.parse import urlencode

https://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab&pd=synthesis
https://www.toutiao.com/search_content/?offset=20&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab&pd=synthesis
https://www.toutiao.com/search_content/?offset=40&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab&pd=synthesis
https://www.toutiao.com/search_content/?offset=60&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab&pd=synthesis

def get_page(offset):
    headers = {
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'x-requested-with':'XMLHttpRequest',
        'referer':'https://www.toutiao.com/search/?keyword=街拍'}
    params = {
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'1',
        'form':'search_tab',
        'pd':'synthesis'
        }
    baseurl = "https://www.toutiao.com/search_content/"
    url = baseurl + urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None
#经过观察发现每张图片分为缩略图，中等图跟大图，这里获取大图，前一段为http://p3-tt.bytecdn.cn/large/加上缩略图的最后一段
def get_image(json):
    ahead = "http://p3-tt.bytecdn.cn/large/"
    if json.get('data'):
        items = json.get('data')
        for item in items:
            title = item.get('title')
            images = ahead+item.get('image_list').split('/')[]
            for image in images:
                yield {
                    'image':image.get('url'),
                    'title':title
                }
def save

