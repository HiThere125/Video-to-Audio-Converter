#
#   The purpose of this project is to serve as a backend manager for video and audio file manipulation and
#   video to audio conversions. This program runs functions using input from VideotoAudioConverterInterface.py
#
#   How it works:
#   1:  Runs function specified by the user in the tkinter window
#
#   Notes:
#   1:  Some of these programs take time and computing resources to complete so despite future tkinter threading
#       it would be wise to run only one function at a time
#
#   Future plans:
#   1:  Fix volume management function
#   2:  Implement a way to better handle mutagen tag management
#   3:  Implement a way to better handle chapter splitting
#   4:  Clean code for increased efficiency and decreased clutter
#

#--------------------------------------------CODE STARTS HERE---------------------------------------------

from moviepy.editor import *
import moviepy.editor
from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3
import os
import glob
import numpy as np

''' Downloads a video from YouTube in an mp4 format using yt-dlp
    @Params:    path:           |   String  |   Path you want to save the mp4 to
                link:           |   String  |   Link to the YouTube video
    @Returns:   None'''
def youtube_dlp_single(path, link):
    os.chdir(f"{path}")
    yt_dlp_command = "yt-dlp  -S vcodec:h264,res,acodec:m4a " + link
    os.system(yt_dlp_command)

''' Downloads a video from YouTube in an mp4 format using yt-dlp
    @Params:    path:           |   String  |   Path you want to save the mp4 to
                link:           |   String  |   Link to the YouTube video
    @Returns:   None'''
def youtube_dlp_playlist(path, link):
    os.chdir(f"{path}")
    yt_dlp_command = "yt-dlp --yes-playlist -S vcodec:h264,res,acodec:m4a " + link
    os.system(yt_dlp_command)    

''' Converts a single MP4 file to MP3 using Moviepy
    @Params:    path            |   String  |   Path to the MP4 file
    @Returns:   None'''
def convert_video_to_audio(path):
    video = moviepy.editor.VideoFileClip(path)
    audio = video.audio
    mp3_file_name = path.replace('.mp4', '.mp3')
    audio.write_audiofile(mp3_file_name, bitrate = '320k')

''' Converts many MP4s to MP3s using Moviepy
    @Params:    path            |   String  |   Path to the MP4 files
    @Returns:   None'''
def mass_convert_to_mp3(path):
    filenames_list = glob.glob(os.path.join(path, "*.mp4"))
    if filenames_list != 0:
        for filename in filenames_list:
            print(filename)
        
            video = moviepy.editor.VideoFileClip(filename)
            audio = video.audio

            if audio is not None:
                mp3_file_name = filename.replace('.mp4', '.mp3')
                audio.write_audiofile(mp3_file_name, bitrate = '320k')
    else:
        print("No mp4 files found in this location")

''' Checks the number of files of a specific type using os.listdir()
    @Params:    path            |   String  |   Path to the folder to be searched
                file_type       |   String  |   Type of file to search for
    @Returns:   number_of_type  |   Int     |   Number of files of specific type
                number_of_files |   Int     |   Number of files total in the folder'''
def check_file_extensions(path):
    number_of_files = [0]*18
    total_files = 0
    files = ["exe", "ini", "png", "jpg", "jpeg", "mp4", "mp3", "mov", "ppt", "csv", "pdf", "twbx", "cfg", "bat", "py", "sln", "pyproj", "misc"]   
    file_list = os.listdir(path)
    for fil in file_list:
        print(fil)
        split_fil = fil.split(".")     
        extension = split_fil[len(split_fil)-1]
        number_of_files[files.index(extension)] = number_of_files[files.index(extension)] + 1
        total_files = total_files + 1
    print(f"There are {total_files} files in this folder")         
    for ext in files:
        num_of_ext = number_of_files[files.index(ext)]       
        if num_of_ext > 0:
            print(f"{num_of_ext} .{ext} files")        

''' Removes the files of a specific type using os.remove()
    @Params:    path            |   String  |   Path to the folder to be searched
                file_type       |   String  |   Type of file to search for
    @Returns:   None'''
def remove_files_with_extension(path, file_type):
    file_list = glob.glob(os.path.join(path, file_type))
    for fil in file_list:
        os.remove(fil)

''' Splits a video into smaller videos by a list of timestamps strings using Moviepy
    Saves the video splits in the same folder
    @Params:    path            |   String          |   Path to the video to split
                chapters        |   List of Strings |   List of timestamps to split the video at
                names           |   List of Strings |   List of names to save the video chapters as
    @Returns:   None'''
def split_video(path, chapters, names = None):
    video = moviepy.editor.VideoFileClip(path)
    start_time = None
    clip = None
    file_type = ".mp4"
    for i in range(0, len(chapters)):
        start_time = parse_time(chapters[i])
        
        if i == len(chapters)-1:
            clip = video.subclip(start_time, video.duration)
        else:
            end_time = parse_time(chapters[i+1])
            clip = video.subclip(start_time, end_time)

        if names == None:
            video_name = split_path(path) + str(i+1) + file_type
        else:
            video_name = split_path(path) + names[i] + file_type
        clip.write_videofile(video_name, codec = "libx264")

'''Take timestamp in and return numerical time out hr*60*60 + min*60 + sec
    @Params:    timestamp       |   String  |
    @Returns:   time            |   Integer |'''
def parse_time(timestamp):
    split_timestamp = timestamp.split(":")
    if len(split_timestamp) == 3:
        time = float(split_timestamp[0])*60*60 + float(split_timestamp[1])*60 + float(split_timestamp[2])
    else:
        time = float(split_timestamp[0])*60 + float(split_timestamp[1])
    return time

''' Gets the path of the folder the file is in
    @Params:    path            |   String  |   Path to the file
    @Returns:   new_path        |   String  |   Path to the folder'''
def split_path(path):
    path_split = path.split("\\")
    new_path = ""
    for part in path_split:
        if ".mp4" not in part:
            new_path  = new_path + part + "\\"
    return new_path

''' Gets the name of the folder the file is in
    @Params:    path            |   String  |   Path to the file
    @Returns:   folder          |   String  |   Name of the folder'''
def get_parent_folder_name(path):
    broken_path = path.split("\\")
    folder = broken_path[broken_path.size()-1]
    return folder

''' Gets the name of the file
    @Params:    path            |   String  |   Path to the file
    @Returns:   part            |   String  |   Name of the file'''
def get_file_name(path):
    path_split = path.split("\\")
    for part in path_split:
        if ".mp4" in part:
            return part
        else:
            return None

''' Moves a file from one path to another
    @Params:    path_in         |   String  |   Path to the file to move
                path_out        |   String  |   Path to save the file at
    @Returns:   None'''
def move_file(path_in, path_out):
    os.rename(path_in, path_out)

''' Adds meta-tags to a group of MP3 files using os.listdir() and Mutagen
    @Params:    path            |   String          |   Path to the folder that contains the MP3s
                tags            |   Dict            |   Tags to add to all MP3s in the folder
                order           |   List            |   The list the files should be in                
    @Returns:   None'''
def add_tags(path, tags, order):
    file_list = os.listdir(path)
    for i in range(len(file_list)):
        new_path = path + "\\" + order[i] + ".mp3"
        tagged_song = MP3(new_path, ID3=EasyID3)
        tagged_song['album'] = tags["album"]
        tagged_song['albumartist'] = tags["albumartist"]
        tagged_song['artist'] = tags["artist"]
        tagged_song['tracknumber'] = str(i+1)
        tagged_song['date'] = tags["date"]
        tagged_song.save()
        
''' This method does not work at the moment
    @Params:    path            |   String  |   Path to the file to change
    @Returns:   None'''
def normalize_volume(path):
    video = VideoFileClip(path).fx(afx.audio_normalize)
    video.write_videofile(path, codec = "libx264", bitrate = "320k")

''' This method does not work at the moment
    @Params:    path            |   String  |   Path to the file to change
    @Returns:   None'''
def increase_volume(path):
    new_path = path.replace(".mp3", "_boosted.mp3")    
    song = moviepy.editor.AudioFileClip(path)
    song.write_audiofile(new_path, bitrate = '320k')
    

def parse_chapter_file(txt_path):
    txtfile = open(txt_path, encoding="utf8")
    chapters = []
    names = []
    order = []
    index = 0    
    line = ""
    for lin in txtfile:
        line = str(lin)
        order[index] = index + 1
        chapters.append(line[:7])
        names.append(line[8:].strip())
        index = index + 1
    return chapters, names, order

'''Downloads videos from the link and saves them at the path. Then converts them to mp3s. Then deletes all of the mp4s from the folder
    @Params:        Path            |   String  |   Path to save the videos and audio at
                    Link            |   String  |   Link tothe video or playlist
                    Constraints     |   List    |   Conditions for the download like if it's a playlist and what codec to use 
    @Returns:       None    '''
def the_full_package(path, link, mode):
    if mode == "playlist":
        youtube_dlp_playlist(path, link)
    elif mode == "single":
        youtube_dlp_single(path, link)
    os.wait()
    mass_convert_to_mp3(path)
    os.wait()
    remove_files_with_extension(path, ".mp4")