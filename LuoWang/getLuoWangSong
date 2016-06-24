#-*- coding: utf-8 -*-
__author__ = 'Wu_cf'


import os,time
import sys
import requests
import unicodedata
from bs4 import BeautifulSoup

LUOO_URL = "http://www.luoo.net/music/{}"
MP3_URL = "http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio{}/{}.mp3"
SONG_NAME = "{} -{}.mp3"
basePath = os.path.join(os.getcwd(), r'luowang')
reload(sys)
sys.setdefaultencoding('utf-8')


def get_song_list(volumn):

    # **** http://www.luoo.net/music/801
    r = requests.get(LUOO_URL.format(volumn))

    bs = BeautifulSoup(r.content, 'html.parser')

    songs = bs.find_all('div', 'player-wrapper')

    print u"本期歌单{}:".format(volumn)

    result = []
    # 获取歌曲目录列表
    for song in songs:

        meta = {}

        meta['name'] = song.find('p', 'name').getText()
        meta['artist'] = song.find('p', 'artist').getText()

        print '{}'.format(meta['name'])

        result.append(meta)

    return result

def download_songs(volumn):

    songs = get_song_list(volumn)
    #创建存储目录
    filename = os.path.join(basePath,str(volumn))

    if not os.path.exists(filename):

        os.makedirs(filename)
        # 转移到当前工作目录
        os.chdir(filename)

    print  u"开始下载"

    index = 0

    for song in songs:

        index += 1

        track = '%02d' % index

        # http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio801/01.mp3
        #  volumn就是801页面，01就是歌曲标识

        r = requests.get(MP3_URL.format(volumn,track), stream=True)

        song_name = SONG_NAME.format(song['name'], song['artist'])
        # Requests 获取头部响应流
        with open(song_name, 'wb') as fd:

            for chunk in r.iter_content():

                fd.write(chunk)

            fd.close()

        print u"{}下载成功".format(song['name'])
        # 睡一下
        time.sleep(1);

        print u"开始下载下一首,干点别的去吧"

if __name__ == '__main__':

    print u"请输入音乐期刊号，如:804\n>"

    vol = raw_input()

    print u"开始下载初始化"

    download_songs(vol)
