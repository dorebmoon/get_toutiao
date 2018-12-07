#coding=utf-8
import requests
import os.path
import os
from hashlib import md5
from urllib.parse import urlencode
from multiprocessing.pool import Pool


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
    baseurl = "https://www.toutiao.com/search_content/?"
    url = baseurl + urlencode(params)
    try:
        response = requests.get(url)
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
            images = item.get('image_list')
            try:
                for image in images:
                    yield {
                        #'image':image.get('url'),
                        'image':ahead+'/'.join((image.get('url')).split('/')[4:]),
                        'title':title
                    }
            except TypeError:
                return None

def save_image(items):
    for item in items:
        if not os.path.exists(item.get('title')):
            os.mkdir(item.get('title'))
        response = requests.get(item.get('image'))
        file_path = '{0}/{1}.{2}'.format(item.get('title'),md5(response.content),'jpg')
        if not os.path.exists(file_path):
            with open(file_path,'wb') as f:
                f.write(response.content)
        else:
            print('%s already download'%(file_path))

def main(offset):
    json = get_page(offset)
    items = get_image(json)
    save_image(items)

if __name__ == "__main__":
    pool = Pool()
    group = ([x * 20 for x in range(0,21)])
    pool.map(main,group)
    pool.close()
    pool.join()








