
from datetime import datetime
import json
from sys import argv
from shutil import copyfile
import yt_dlp

from song import Song


def create_backup(file_path: str):
    now = datetime.now()
    current_datetime = now.strftime("%y-%m-%d %H-%M-%S")
    copyfile(file_path, f'{file_path}.{current_datetime}.bkp')


def fetch_song_info(song) -> Song:
    ydl = yt_dlp.YoutubeDL()
    song_info = ydl.extract_info(song['url'], download=False)
    new_song = Song(song_info['id'], song_info)
    for _property in song:
        if song[_property] is None:
            song[_property] = new_song.to_dict()[_property]

    return song


def remake_cache(file_path: str):
    with open(file_path, 'r') as cache_json_file:
        song_caches = json.load(cache_json_file)
        for song in song_caches:
            try:
                for _property in song_caches[song]:
                    if song_caches[song][_property] is None:
                        song_caches[song] = fetch_song_info(song_caches[song])
                        break
            except:
                continue
        song_json_object = json.dumps(song_caches)
    with open(file_path, 'w') as cache_json_file:
        cache_json_file.write(song_json_object)


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
