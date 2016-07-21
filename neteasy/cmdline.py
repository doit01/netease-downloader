# coding: utf-8

# from .NeteasyDownloader import Downloader
import neteasy.NeteasyDownloader
import sys, os, requests
from gevent import monkey; monkey.patch_all()
import gevent
from gevent.queue import Queue

def download_music(queue, floder, name):
    while not queue.empty():
        item = queue.get_nowait()
        content = requests.get(item['url']).content
        with open('%s/%s - %s.mp3' %(floder, item['artist'], item['song']), 'wb') as f:
            f.write(content)
            print('[协程%s]下载完成: %s - %s' %(name, item['artist'], item['song']))

def execute():
    downloader = neteasy.NeteasyDownloader.Downloader()
    try:
        if sys.argv[3] == '-t':
            thread_on = sys.argv[4]
        if sys.argv[1] == '-m':
            # 单曲
            result = downloader.get_music(sys.argv[2])
            content = requests.get(result['url']).content
            with open('%s - %s.mp3' % (result['artist'], result['song']), 'wb') as f:
                f.write(content)
                print('下载完成: %s - %s' % (result['artist'], result['song']))
        elif sys.argv[1] == '-a':
            # 专辑
            songs_queue = Queue()
            result = downloader.get_album(sys.argv[2])
            os.mkdir(result['name'])
            for item in result['songs']:
                songs_queue.put_nowait({
                    'url': item['url'],
                    'song': item['song'],
                    'artist': item['artist']
                })
            gevent_list = []
            for i in range(int(thread_on)):
                gevent_list.append(gevent.spawn(download_music, songs_queue, result['name'], str(i+1)))
            gevent.joinall(gevent_list)

        elif sys.argv[1] == '-p':
            # 歌单
            result = downloader.get_playlist(sys.argv[2])
            songs_queue = Queue()
            os.mkdir(result['name'])
            for item in result['songs']:
                songs_queue.put_nowait({
                    'url': item['url'],
                    'song': item['song'],
                    'artist': item['artist']
                })
            gevent_list = []
            for i in range(int(thread_on)):
                gevent_list.append(gevent.spawn(download_music, songs_queue, result['name'], str(i+1)))
            gevent.joinall(gevent_list)

    except IndexError as e:
        print('请带参数执行 -m 音乐ID / -a 专辑ID / -p 歌单ID')

if __name__ == '__main__':
    execute()