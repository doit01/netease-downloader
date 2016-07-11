# coding: utf-8

from .NeteasyDownloader import Downloader
import sys, urllib.request, os

def execute():
    nh = Downloader()
    try:
        if sys.argv[1] == '-m':

            # 音乐
            result = nh.get_music(sys.argv[2])
            print('正在下载: %s' % result['song'])
            urllib.request.urlretrieve('%s' % result['url'], '%s - %s.mp3' % (result['artist'], result['song']))

        elif sys.argv[1] == '-a':

            # 专辑
            result = nh.get_album(sys.argv[2])
            os.mkdir( result['name'])
            for index, item in enumerate(result['songs']):
                try:
                    print('(%s/%s) 正在下载: %s' %(index+1, result['size'], item['song']))
                    urllib.request.urlretrieve('%s' % item['url'],
                                               '%s/%s - %s.mp3' % (result['name'], item['artist'], item['song']))
                except urllib.error.HTTPError as e:
                    print('下载失败: %s %s' % item['song'])


        elif sys.argv[1] == '-p':

            # 歌单
            result = nh.get_playlist(sys.argv[2])
            os.mkdir(result['name'])
            for index, item in enumerate(result['songs']):
                try:
                    print('(%s/%s) 正在下载: %s' %(index+1, result['size'], item['song']))
                    urllib.request.urlretrieve('%s' % item['url'],
                                               '%s/%s - %s.mp3' % (result['name'], item['artist'], item['song']))
                except urllib.error.HTTPError as e:
                    print('下载失败: %s' % item['song'])

    except IndexError as e:
        print('请带参数执行 -m 音乐ID / -a 专辑ID / -p 歌单ID')
