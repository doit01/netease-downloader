# coding: utf-8

import requests, json

class Downloader():
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
