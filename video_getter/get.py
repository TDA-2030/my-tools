#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
from ffprobe import FFProbe
from tokenize import Hexnumber
from urllib.parse import urljoin, urlparse
import subprocess
import shlex
import threading
from pathlib import Path
import cv2
import os 
import os.path
from enum import Enum

class Color(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

def print_color(text: str, fg: Color = Color.BLACK.value):
    print(f'\033[{fg}m{text}\033[0m')

def download_file(url, out_dir='output'):
    formats=['--format=dash-flv720', '--format=dash-flv480', '--format=dash-flv360']
    for format in formats:
        args = [
            'you-get',
            '--no-caption',
            format,
            # '--cookies',
            # 'C:/Users/zhouli/AppData/Local/Google/Chrome/User Data/Default/Network/Cookies',
            '--output-dir',
            out_dir,
            url
        ]
        print(args)
        p = subprocess.Popen(args, shell=True ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            line=p.stdout.readline()
            print(line, end="")
        retval = p.wait()
        if retval == 0:
            print_color('\nDownload [%s] with %s success' % (url, format), fg = Color.GREEN.value)
            break
        else:
            print_color('\nDownload [%s] with %s failed retval=%d' % (url, format, retval), fg = Color.RED.value)

def files_rename(rootdir):
    files = os.listdir(rootdir)
    b=1
    for name in files:
        newname = '%03d.%s' % (b, name)
        # newname = '%03d.' % (b) + name[4:]
        b = b + 1
        print(newname)
        os.rename(rootdir+name,rootdir+newname)

def read_vedio_info(filename):
    #加载视频
    videoCapture = cv2.VideoCapture(filename)
    #读取视频fps(帧率)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    #读取视频的宽度
    Frame_Width = videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
    #读取视频的高度
    Frame_Height = videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #读取视频总帧数
    FrameNumber = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    #获取视频时长，单位为秒
    video_time = FrameNumber / fps

    metadata=FFProbe(filename)
    codec = None
    for stream in metadata.streams:
        if stream.is_video():
            codec = stream.codec()
    #输出信息
    print("[{}], codec:{}, time:{}s, fps:{}, Width:{}, Height:{}, Number:{}".format(filename,codec,video_time,fps,Frame_Width,Frame_Height,FrameNumber))

    return (Frame_Width, Frame_Height, codec)

def convert_to_mp4(input_file):
    filename=Path(input_file)
    print_color(filename, Color.BLUE.value)
    
    need_cvt=0
    w, h, codec= read_vedio_info(str(filename))
    args = " "
    cvt_filename = str(filename.parent) + '/' + 'cvt-'+filename.stem+'.mp4'
    # if a[1] != '.mp4':
    #     need_cvt=1
    #     print('convert %s to %s' % (filename, a[0]+'.mp4'))
    #     args = shlex.split('ffmpeg -i ' + '"'+input_file+'" ' + cvt_filename + ' -n')

    # if w>1280 or h>720:
    #     need_cvt=1
    #     args = shlex.split('ffmpeg -i ' + '"'+input_file+'" ' + '-vf scale=1280:720 ' + cvt_filename)
    if codec != 'h264':
        need_cvt = 1
        args = shlex.split('ffmpeg -i ' + '"'+str(filename)+'" ' + '-vcodec h264 ' + '"'+cvt_filename+'"' + ' -n')
    if need_cvt:
        print(args)
        p = subprocess.Popen(args, shell=True ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            line=p.stdout.readline().decode("utf8")
            print(line, end='')
        retval = p.wait()
        if retval==0:
            os.remove(str(filename))
            os.rename(cvt_filename, str(filename))
    else:
        print('Do not need change anything')


def sum_count(file_object):
    cnt=0
    for line in file_object:
        if line in ['\n', '\r\n']:
            pass
        else:
            cnt=cnt+1
    file_object.seek(0)
    return cnt

# file_object = open('s2.txt','r')
# try: 
#     total = sum_count(file_object)
#     index = 0
#     for line in file_object:
#         if line in ['\n', '\r\n']:
#             pass
#         else:
#             line=line.strip('\n')
#             index = index + 1
#             url=line#urljoin(line, urlparse(line).path)
#             print('Downloading %s (%d/%d)' % (url, index, total))
#             download_file(url, 'out')
# finally:
#      file_object.close()


# rootdir = 'E:\dance\\'
rootdir='out\\'
files = os.listdir(rootdir)
for name in files:
    convert_to_mp4(rootdir+name)

