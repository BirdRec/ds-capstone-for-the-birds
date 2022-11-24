import os
import shutil
from itertools import chain
import time

# measure the time for this script
# get the start time
st = time.time()

# get current absolute path of parent folder of this file
path = os.path.dirname(os.path.abspath('restructuring'))
# path2 = os.path.abspath('restructuring') # path to file

# first create new folders
os.makedirs('data_1v2/train/')
os.makedirs('data_1v2/valid/')
os.makedirs('data_1v2/test/')

# define source and destination paths
src = path + '/data_1/images/'
dst_train = path + '/data_1v2/train/'
dst_test = path + '/data_1v2/test/'
dst_valid = path + '/data_1v2/valid/'

# copy Cornell data to these folders
shutil.copytree(src, dst_train, dirs_exist_ok=True)
shutil.copytree(src, dst_test, dirs_exist_ok=True)
shutil.copytree(src, dst_valid, dirs_exist_ok=True)

# now, we have just a copy, but we want to delete some files by doing 3 things:
# 1) in the train folder, we loop through each subfolder and delete the last 20 picture
# 2) in the valid folder, we loop through each subfolder and delete all pictures except the last 20 picture
#   up to last 10 pictures
# 3) in the test folder, we loop through each subfolder and delete all pictures except the last 10 picture

# Let's start
# 1)
# loop through each subfolder: '0295', '0296', etc
for label in os.listdir(dst_train):
    # ignore hidden folders such as .DS_Store
    if not (label.startswith('.') or label.endswith('.txt')):
        # loop through pictures - remove last 20
        for filename in os.listdir(dst_train + label)[-20:]:
            filename_relPath = os.path.join(dst_train + label, filename)
            os.remove(filename_relPath)

# 2)
# loop through each subfolder: '0295', '0296', etc
for label in os.listdir(dst_valid):
    # ignore hidden folders such as .DS_Store
    if not (label.startswith('.') or label.endswith('.txt')):
        # loop through pictures - remove all except last 20 to last 10
        for filename in list(chain(os.listdir(dst_valid + label)[:-20], os.listdir(dst_valid + label)[-10:])):
            filename_relPath = os.path.join(dst_valid + label, filename)
            os.remove(filename_relPath)

# 3)
# loop through each subfolder: '0295', '0296', etc
for label in os.listdir(dst_test):
    # ignore hidden folders such as .DS_Store
    if not (label.startswith('.') or label.endswith('.txt')):
        # loop through pictures - remove all except last 10
        for filename in os.listdir(dst_test + label)[:-10]:
            filename_relPath = os.path.join(dst_test + label, filename)
            os.remove(filename_relPath)

# get the end time
et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
