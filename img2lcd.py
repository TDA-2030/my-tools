#coding: utf-8 -*-

from PIL import Image
import numpy as np
# from pylab import *
#读取图片并转为数组
im = np.array(Image.open("solution-platform.jpg"))
#输出数组的各维度长度以及类型
im = im.transpose(1,0,2)
print (im.shape,im.dtype)
w = im.shape[0]
h = im.shape[1]
print (w, h)
fData=open("main/img_array.h", mode='w')
fData.write("#include <stdint.h>\n\n")
fData.write("static int img_width = %d;\n" % w)
fData.write("static int img_height = %d;\n" % h)
fData.write("static const uint16_t img_array[%d]={\n" % (w*h))

a = np.empty([w,h], dtype = int)

for y in range(h):
    for x in range(w):
        r = im[x, y, 0]
        g = im[x, y, 1]
        b = im[x, y, 2]
        p = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        a[x, y] = p
        # print(x, y, p, type(p))
        fData.write("%s, " % str(a[x, y]))
        
    
    fData.write("\n")

fData.write("};\n")
fData.close()
