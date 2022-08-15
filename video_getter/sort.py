from genericpath import isdir
import os 
import os.path


rootdir = 'F:\\'
files = os.listdir(rootdir)
index=1
for name in files:
    if os.path.isfile(rootdir+name) == True:
        newname = name
        if name[:3].isdigit()==False:
            newname = '%03d.%s' % (index, name)
        else:
            newname = '%03d.%s' % (index, name[4:])
        
        if newname != name:
            print('[%s] rename to [%s]' % (name, newname))
            os.rename(rootdir+name,rootdir+newname)
        index = index + 1
