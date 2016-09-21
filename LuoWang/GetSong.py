#-*- coding: utf-8 -*-
__author__ = 'Wu_cf'


import os,time
import sys
import getopt
import requests
import unicodedata
import eyed3
import re
from bs4 import BeautifulSoup

LUOO_URL = "http://www.luoo.net/music/{}"
MP3_URL = "http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio{}/{}.mp3"
SONG_NAME = "{}.mp3"
SONG_NAME_OLD = "{} -{}.mp3"
basePath = os.path.join(os.getcwd(), r'luowang')
reload(sys)
sys.setdefaultencoding('utf-8')
DOWNLOAD_MODE = 0 # 0:输入模式 1:旧版本修复模式 2:更新模式 3:精准模式(只下载指定专辑的指定歌曲)
song_shoot    = 0 #精准模式使用，指定(某个专辑的)歌曲
def save_page(page,dir_name):
    #创建存储目录
    filename = os.path.join(basePath,dir_name)

    if not os.path.exists(filename):
        os.makedirs(filename)
    # 转移到当前工作目录
    os.chdir(filename)
    #保存页面内容
    with open(dir_name+".html", 'w') as infofile:
        infofile.write(page)
    infofile.close()

def repair_page(page,old_name,dir_name):
    #将旧目录名改为新的
    oldfilename = os.path.join(basePath,old_name)
    newfilename = os.path.join(basePath,dir_name)

    if not os.path.exists(oldfilename):
        print u"文件目录不存在" + oldfilename
        return
    os.rename(oldfilename,newfilename)
    # 转移到当前工作目录
    os.chdir(newfilename)
    #保存页面内容
    with open(dir_name+".html", 'w') as infofile:
        infofile.write(page)
    infofile.close()
        
    

def get_song_list(volumn):

    # **** http://www.luoo.net/music/801
    r = requests.get(LUOO_URL.format(volumn))

    bs = BeautifulSoup(r.content, 'html.parser')
    name_number = bs.find("span","vol-number rounded").getText()
    name_title  = bs.find("span","vol-title").getText()
    name_sharp  = bs.find("a","vol-tag-item").getText()
    if DOWNLOAD_MODE == 1:
        repair_page(r.content, name_number,name_number + u" " + name_title + u" " + name_sharp)
    else:
        save_page(r.content, name_number + u" " + name_title + u" " + name_sharp)

    songs = bs.find_all('div', 'player-wrapper')
    print u"刊号: " + volumn + u" 基本信息取得完毕"
    result = []
    # 获取歌曲目录列表
    index = 1
    for song in songs:
        meta = {}
        meta['name']        = song.find('p', 'name').getText()
        meta['artist']      = re.sub(ur'Artist: ', u"", song.find('p', 'artist').getText()) #去掉 artist 中 Artist: 
        meta['oldartist']   = song.find('p', 'artist').getText()                            #修复模式使用
        meta['album']       = re.sub(ur'Album: ', u"", song.find('p', 'album').getText())   #去掉 album  中 Album: 
        meta['image']       = song.find('img')['src']                                       #专辑图片
        if DOWNLOAD_MODE == 3:#精准模式，只下载一首
            if index == song_shoot:
                result.append(meta)
        else:
            result.append(meta)
        index += 1
    print u"刊号: " + volumn + u" 歌曲信息取得完毕,共 " +str(len(result)) + u" 首"
    return result

def download_songs(volumn):

    songs = get_song_list(volumn)
    index = 0
    song_name = ""
    for song in songs:
        index += 1
        track = '%02d' % index
        song_name = SONG_NAME.format(song['name'])

        if DOWNLOAD_MODE == 1:#修复模式
            print u"刊号: " + volumn + u" " + str(index) + u"/" + str(len(songs)) + u" 开始修复: " + song['name']
            song_name_old = SONG_NAME_OLD.format(song['name'], song['oldartist'])
            if os.path.isfile(song_name_old)==True:
                os.rename(song_name_old,song_name)
            else:#没有文件则跳到下一首
                print u"刊号: " + volumn + u" " + str(index) + u"/" + str(len(songs)) + u" 未找到文件:"+ song_name_old +u" 跳过"
                continue
        else:
            print u"刊号: " + volumn + u" " + str(index) + u"/" + str(len(songs)) + u" 开始下载: " + song['name']
            # http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio801/01.mp3
            #  volumn就是801页面，01就是歌曲标识
            try:
                r = requests.get(MP3_URL.format(volumn,track), stream=False)
                if r.status_code != 200:
                    track = str(index)
                    r = requests.get(MP3_URL.format(volumn,track), stream=False)
                    
                # Requests 获取头部响应流
                with open(song_name, 'wb') as fd:
                    for chunk in r.iter_content():
                        fd.write(chunk)
                    fd.close()
            except:
                print u"刊号: " + volumn + u" " + str(index) + u"/" + str(len(songs)) + u" 下载失败 "
                with open(os.path.isfile(str(index) + u"_error.txt"), 'w') as fe:
                    fe.write(u"")
                fe.close()
        try:
            #读取专辑封面
            coverimage = requests.get(song['image'],stream=False)
            #写入id3
            audiofile = eyed3.load(song_name)
            if audiofile.tag is None:
                audiofile.tag = eyed3.id3.Tag()
                audiofile.tag.file_info = eyed3.id3.FileInfo(song_name)
            audiofile.tag.artist = song['artist']
            audiofile.tag.album  = song['album']
            audiofile.tag.album_artist = u"http://www.luoo.net"
            audiofile.tag.title  = song['name']
            if DOWNLOAD_MODE == 3:
                audiofile.tag.track_num = song_shoot
            else:
                audiofile.tag.track_num = index
            audiofile.tag.images.set(3,coverimage.content,"image/jpeg",u"")
            audiofile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION,encoding='utf-8')#id3v1 不支持unicode ，使用id3v2
        except:
            pass#id3v2写入失败，无所谓

        if DOWNLOAD_MODE == 1:
            print u"刊号: " + volumn + u" " + str(index) + u"/" + str(len(songs)) + u" 修复完成"
        else:
            print u"刊号: " + volumn + u" " + str(index) + u"/" + str(len(songs)) + u" 下载完成"
            # 睡一下
            time.sleep(3);
    if DOWNLOAD_MODE == 1:
        print u"专辑 " + volumn + u" 修复完成"
    else:
        print u"专辑 " + volumn + u" 下载完成"

def main(argv):
    #参数处理
    opts, args = getopt.getopt(argv, "hrf:t:s:e:u")
    page_from  = 0
    page_to    = 0
    page_shoot = 0
    global song_shoot
    global DOWNLOAD_MODE 

    for op, value in opts:
        if op == "-f":
            DOWNLOAD_MODE = 0
            try:
                page_from = int(value)
            except :
                print u"参数有误： -f 开始期刊 请输入大于零的数字"
                sys.exit()
        elif op == "-t":
            DOWNLOAD_MODE = 0
            try:
                page_to = int(value)
            except :
                print u"参数有误： -t 停止期刊 请输入大于零的数字"
                sys.exit()
        elif op == "-h":
            print u"参数： \n-f 开始期刊 \n-t 停止期刊 \n\
                        -h 参数列表\n-r 旧版本修复\n-u 更新模式\n\
                        -s 精准模式：指定期刊\n-e精准模式：指定歌曲"
            sys.exit()
        elif op == "-r":
            DOWNLOAD_MODE = 1
        elif op == "-u":
            DOWNLOAD_MODE = 2
        elif op == "-s":
            DOWNLOAD_MODE = 3
            try:
                page_shoot = int(value)
            except :
                print u"参数有误： -s 指定期刊 请输入大于零的数字"
                sys.exit()
        elif op == "-e":
            DOWNLOAD_MODE = 3
            try:
                song_shoot = int(value)
            except :
                print u"参数有误： -e 指定歌曲 配合-s使用"
                sys.exit()
    #参数处理完毕
    
    if DOWNLOAD_MODE == 0 or DOWNLOAD_MODE == 1:
        #无 from ,to ,需要用户输入
        if page_from == 0 and page_to == 0:
            vol = ""
            print u"请输入音乐期刊号:\n>"
            while (page_from <= 0):
                vol = raw_input()
                try:
                    page_from = int(vol)
                except :
                    print u"值有误,请输入大于零的音乐期刊号:\n>"
                    continue
                if page_from <= 0:
                    print u"值有误,请输入大于零的音乐期刊号:\n>"
                    
        if page_from <= 0 and page_to > 0:
            page_from = page_to
        if page_from > 0 and page_to <= 0:
            page_to = page_from
        if page_from > page_to :#有两个数字就行了，没必要让用户重新输入
            page_to,page_from = page_from,page_to
            
        if DOWNLOAD_MODE == 1:
            print u"准备修复刊号: " + str(page_from) + u" 到 " + str(page_to)
        else:
            print u"准备下载刊号: " + str(page_from) + u" 到 " + str(page_to)
        for i in range(page_from,page_to + 1):
            if DOWNLOAD_MODE == 1:
                print u"开始修复刊号: " + str(i)
            else:
                print u"开始下载刊号: " + str(i)
            download_songs(str(i))
        if DOWNLOAD_MODE == 1:
            print u"期刊" + str(page_from) + u"到" + str(page_to) + u" 修复完成"
        else:
            print u"期刊" + str(page_from) + u"到" + str(page_to) + u" 下载完成"
    elif DOWNLOAD_MODE == 2:#更新模式
        #找到最新专辑序号
        r = requests.get(u"http://www.luoo.net/")
        bs = BeautifulSoup(r.content, 'html.parser')
        page_to = int(re.sub(ur'http://www.luoo.net/music/', u"", bs.find("a","cover-wrapper cover-wrapper-lg")['href']))
        print u"最新期刊:" + str(page_to)
        #找到本地最新专辑序号
        result = []
        if not os.path.exists(basePath):#什么都没有，从1开始到最新
            page_from = 1
        else:
            for file in os.listdir(basePath):
                try:
                    index = int(file[0:3])
                    result.append(index)
                except :
                    pass
            page_from = max(result) + 1 
            if page_from == page_to + 1:
                print u"本地专辑是最新的"
            elif page_from > page_to + 1:
                print u"本地目录混乱，请清理后重试"
            else:
                print u"准备下载刊号: " + str(page_from) + u" 到 " + str(page_to) +u"确认更新吗？(y/n)"
                vol = raw_input()
                if vol != u'y' and vol != u'Y':
                    print u"更新取消"
                    sys.exit()
                
                for i in range(page_from,page_to + 1):
                    print u"开始下载刊号: " + str(i)
                    download_songs(str(i))
                print u"更新完毕"
                
    
    elif DOWNLOAD_MODE == 3:#精准模式
        print u"开始下载专辑 " + str(page_shoot) + u" 的第 " + str(song_shoot) + u" 首歌曲"
        download_songs(str(page_shoot))
        print u"专辑 " + str(page_shoot) + u" 的第 " + str(song_shoot) + u" 首歌曲下载完毕"


if __name__ == '__main__':
    main(sys.argv[1:])
