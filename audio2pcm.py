#!/usr/bin/python
# -*- coding: utf-8 -*-

from pydub import AudioSegment
import wave
import os
import numpy as np


def save_to_wav(sound ):
    sound.export('_temp_.wav', format='wav')
    return '_temp_.wav'


def load_file(file, db, rate, ch, width, start_sec, len_sec):
    print("open file:%s" % file)
    sound = AudioSegment.from_file(file)
    sound = sound + db
    sound = sound.set_frame_rate(rate)
    sound = sound.set_channels(ch)
    sound = sound.set_sample_width(width)

    end = start_sec+len_sec
    if len_sec < 0:
        sound = sound[start_sec * 1000:]
    else:
        sound = sound[start_sec*1000:end*1000]

    return sound

def wave_to_array(wavefile, array_path):
    wave_f = wave.open(wavefile, 'rb')
    params = wave_f.getparams()
    print(params)

    # open a txt file
    fData = open(array_path, 'w')
    bytes = params.nframes * params.sampwidth * params.nchannels

    fData.write("#include <stdint.h>\n\n")
    fData.write("static const uint8_t wave_array[];\n")
    fData.write("char *wave_get(void){return (char*)wave_array;}\n")
    fData.write("uint32_t wave_get_size(void){return %d;}\n" % (bytes))
    fData.write("uint32_t wave_get_framerate(void){return %d;}\n" % params.framerate)
    fData.write("uint32_t wave_get_bits(void){return %d;}\n" % (params.sampwidth*8))
    fData.write("uint32_t wave_get_ch(void){return %d;}\n" % params.nchannels)
    fData.write("/* size : %d */\n" % (bytes))
    fData.write("static const uint8_t wave_array[]={\n")

    for i in range(int(params.nframes / 32)):
        data = wave_f.readframes(32)
        ldata = list(data)
        if params.sampwidth == 1:
            ldata = np.array(ldata)-127
            ldata = list(ldata)
        sdata = str(ldata)
        fData.writelines(sdata[1:-1])  # remove
        fData.write(",\n")
    fData.write("};\n")

    print('size=%d' % (bytes))
    fData.close()  # close data file
    wave_f.close()

def scan_file(directory, prefix=None, postfix=None):
    file_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            # ??????????????????????????????
            if postfix or prefix:
                # ???????????????????????????
                if postfix and prefix:
                    if special_file.endswith(postfix) and special_file.startswith(prefix):
                        file_list.append(os.path.join(root, special_file))
                        continue

                # ???????????????
                elif postfix:
                    if special_file.endswith(postfix):
                        file_list.append(os.path.join(root, special_file))
                        continue

                # ???????????????
                elif prefix:
                    if special_file.startswith(prefix):
                        file_list.append(os.path.join(root, special_file))
                        continue

            # ????????????????????????
            else:
                file_list.append(os.path.join(root, special_file))
                continue
    # print(file_list)	# ?????????????????????????????????
    return file_list


if __name__ == "__main__":
    files = scan_file("./")
    for i in range(len(files)):
        print("[%d] %s" % (i, files[i]))

    num_index = 0
    num_start = 0
    num_duration = 10
    num_rate = 8000
    num_width = 1

    index = input('?????????????????????0:')
    if index:
        num_index = int(index)
    print(files[int(num_index)])

    rate = input('?????????(Hz)?????????8000:')
    if rate:
        num_rate = int(rate)
    print("?????????:%d" % num_rate)

    width = input('????????????(byte)?????????1:')
    if width:
        num_width = int(width)
    print("????????????:%d" % num_width)

    start = input('????????????(s)?????????0:')
    if start:
        num_start = int(start)
    print("????????????:%d" % num_start)

    duration = input('??????(s)?????????10:')
    if duration:
        num_duration = int(duration)
    print("??????:%d" % num_duration)

    s1 = load_file(files[int(num_index)], db = 0, rate = num_rate, ch = 1, width = num_width, start_sec = num_start, len_sec = num_duration)
    f = save_to_wav(s1)
    wave_to_array(f, "../main/wave.c")
