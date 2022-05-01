import json
from sys import argv
from shutil import copyfile
import yt_dlp

from song import Song


def create_backup(file_path: str):
    copyfile(file_path, f'{file_path}.bkp')


def fetch_song_info(song) -> Song:
    ydl = yt_dlp.YoutubeDL()
    song_info = ydl.extract_info(song['url'], download=False)
    song_info['path'] = song['path']
    song_info['url'] = song['url']

    new_song = Song(song_info['id'], song_info)
    return new_song

def remake_cache(file_path: str):
    with open(file_path, 'r') as cache_json_file:
        song_caches = json.load(cache_json_file)
        for song in song_caches:
            for _property in song_caches[song]:
                if song_caches[song][_property] is None:
                    song_caches[song] = fetch_song_info(song_caches[song]).to_dict()
        json_object = json.dumps(song_caches)
    with open(file_path, 'w') as cache_json_file:
        cache_json_file.write(json_object)


if __name__ == "__main__":
    number_of_arguments = len(argv)
    if number_of_arguments == 2:
        try:
            file_path = argv[1]
            create_backup(file_path)
            remake_cache(file_path)
            print('Cache successfully remade')
        except:
            print('Error to remake cache')
    else:
        print('Invalid number of arguments')
