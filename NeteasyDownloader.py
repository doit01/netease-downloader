# coding: utf-8

import requests, json, sys, urllib.request, os

class NeteasyDownloader():
    def __init__(self):
        self.header = {
            'Cookie': 'appver=1.5.0.75771;',
            'Referer': 'http://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }
        self.music_url = 'http://music.163.com/api/song/detail/?id={id}&ids=[{ids}]'
        self.album_url = 'http://music.163.com/api/album/{id}'
        self.playlist_url = 'http://music.163.com/api/playlist/detail?id={id}'

    def get_music(self, music_id):
        url = self.music_url.replace('{id}', music_id).replace('{ids}', music_id)
        result = requests.get(url, headers=self.header).text
        jo = json.loads(result)
        mp3_url = jo['songs'][0]['mp3Url']
        artists = jo['songs'][0]['artists'][0]['name']
        song = jo['songs'][0]['name']
        return {
            'artist': artists,
            'song': song,
            'url': mp3_url
        }

    def get_album(self, album_id):
        url = self.album_url.replace('{id}', album_id)
        result = requests.get(url, headers=self.header).text
        jo = json.loads(result)
        size = jo['album']['size']
        artist = jo['album']['artist']['name']
        name = jo['album']['name']
        songs = []
        for item in jo['album']['songs']:
            songs.append({
                'song': item['name'],
                'artist': artist,
                'url': item['mp3Url']
            })
        return {
            'name': name,
            'size': size,
            'songs': songs
        }

    def get_playlist(self, playlist_id):
        url = self.playlist_url.replace('{id}', playlist_id)
        result = requests.get(url, headers=self.header).text
        jo = json.loads(result)
        size = jo['result']['trackCount']
        name = jo['result']['name']
        songs = []
        for item in jo['result']['tracks']:
            songs.append({
                'song': item['name'],
                'artist': item['artists'][0]['name'],
                'url': item['mp3Url']
            })
        return {
            'name': name,
            'size': size,
            'songs': songs
        }

if __name__ == '__main__':
    nh = NeteasyDownloader()
    try:
        if sys.argv[1] == '-m':

            # 音乐
            result = nh.get_music(sys.argv[2])
            urllib.request.urlretrieve('%s' %result['url'], '%s - %s.mp3' %(result['artist'], result['song']))
            print('下载完成!')

        elif sys.argv[1] == '-a':

            # 专辑
            result = nh.get_album(sys.argv[2])
            os.mkdir(result['name'])
            for item in result['songs']:
                try:
                    print('正在下载: %s' %item['song'])
                    urllib.request.urlretrieve('%s' % item['url'],
                                               '%s/%s - %s.mp3' % (result['name'], item['artist'], item['song']))
                except urllib.error.HTTPError as e:
                    print('下载失败: %s %s' %item['song'])


        elif sys.argv[1] == '-p':

            # 歌单
            result = nh.get_playlist(sys.argv[2])
            os.mkdir(result['name'])
            for item in result['songs']:
                try:
                    print('正在下载: %s' % item['song'])
                    urllib.request.urlretrieve('%s' % item['url'],
                                               '%s/%s - %s.mp3' % (result['name'], item['artist'], item['song']))
                except urllib.error.HTTPError as e:
                    print('下载失败: %s' % item['song'])

    except IndexError as e:
        print('请带参数执行 -m 音乐ID / -a 专辑ID / -p 歌单ID')
    
