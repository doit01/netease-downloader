# coding: utf-8

from .NeteaseDownloader import Downloader
import sys, os, requests, argparse
import threading
import queue

def download_music(queue, folder, name):
    while not queue.empty():
        item = queue.get_nowait()
        content = requests.get(item['url']).content
        with open('%s/%s - %s.mp3' %(folder, item['artist'], item['song']), 'wb') as f:
            f.write(content)
            print('[线程%s]下载完成: %s - %s' %(name, item['artist'], item['song']))

def execute():
    parser = argparse.ArgumentParser('netease')
    parser.add_argument('-music', dest='music', default='', help='歌曲')
    parser.add_argument('-album', dest='album', default='', help='专辑')
    parser.add_argument('-playlist', dest='playlist', default='', help='歌单')
    parser.add_argument('-thread', type=int, default=4, dest='thread', help='线程')
    args = parser.parse_args()

    downloader = Downloader()
    thread_on = args.thread

    if args.music:
        # 单曲
        result = downloader.get_music(sys.argv[2])
        content = requests.get(result['url']).content
        with open('%s - %s.mp3' % (result['artist'], result['song']), 'wb') as f:
            f.write(content)
            print('下载完成: %s - %s' % (result['artist'], result['song']))
    elif args.album:
        # 专辑
        songs_queue = queue.Queue()
        result = downloader.get_album(sys.argv[2])
        # 替换windows非法字符
        result['name'] = str(result['name'])\
            .replace('/', ',')\
            .replace('\\', ',')\
            .replace(':', ',')\
            .replace('*', ',')\
            .replace('?', ',')\
            .replace('"', ',')\
            .replace('|', ',')

        os.mkdir(result['name'])
        for item in result['songs']:
            songs_queue.put_nowait({
                'url': item['url'],
                'song': item['song'],
                'artist': item['artist']
            })
        thread_list = []
        for i in range(int(thread_on)):
            thread_list.append(
                threading.Thread(target=download_music, args=(songs_queue, result['name'], str(i + 1)), name='1')
            )
        #gevent.joinall(gevent_list)
        for i in thread_list:
            i.start()
    elif args.playlist:
        # 歌单
        result = downloader.get_playlist(sys.argv[2])
        songs_queue = queue.Queue()
        # 替换windows非法字符
        result['name'] = str(result['name']) \
            .replace('/', ',') \
            .replace('\\', ',') \
            .replace(':', ',') \
            .replace('*', ',') \
            .replace('?', ',') \
            .replace('"', ',') \
            .replace('|', ',')

        os.mkdir(result['name'])
        for item in result['songs']:
            songs_queue.put_nowait({
                'url': item['url'],
                'song': item['song'],
                'artist': item['artist']
            })
        thread_list = []
        for i in range(int(thread_on)):
            thread_list.append(
                threading.Thread(target=download_music, args=(songs_queue, result['name'], str(i +1)))
            )
        for i in thread_list:
            i.start()

if __name__ == '__main__':
    execute()