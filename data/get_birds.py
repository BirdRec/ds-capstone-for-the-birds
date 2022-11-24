import os
import pandas as pd
import urllib.request
import urllib
import random

SEED = 42
random.seed(SEED)
'''
Script to download bird images whose links are stored online in a google docs spreadsheet. It creates a folder besides 
this script and stores the images in subfolder corresponding to the class label (species)
'''

'''
Source: 
https://towardsdatascience.com/read-data-from-google-sheets-into-pandas-without-the-google-sheets-api-5c468536550
'''

# define path to google spreadsheet
sheet_id = '1aXlBkL4tV4ugoIyntEx8EtK83l12JhjOtNi7iWKeuR4'
sheet_name = 'european_birds'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

# get spreadsheet and load it as dataframe; sort classes alphabetically
df = pd.read_csv(url)
df.sort_values('class', inplace=True)

# after sorting, we need to reset the index
df = df.reset_index(drop=True)

# get number of rows (images)
ni = df.shape[0]

# check and remove rows if they occur more than once
df.drop_duplicates(inplace=True, ignore_index=True)

# make sure that url is string
df['url'] = df['url'].astype(str)

# create new column with file names
df['file_name'] = df['url'].apply(lambda x: x.split('/')[-1])

# so what happens here?
# note: this apply/lambda method is a loop over the rows, so first x is the url of the first row and so on
# the url is split after each '/' and we get a list with the single parts of the url
# the last item in the list (therefore [-1]) is the one with the name of the jpg/jpeg file

# Rename images having name 'image.jpg' by adding random number between 0 and 500, e.g. image_264.jpg
df['file_name'] = df['file_name'].apply(lambda x: 'image' + '_' + str(random.randint(0, 500)) + '.jpg' if x == 'image.jpg' else x)

# get the name of the folder to be created
classes = df['class'].unique().tolist()

# get current absolute path of parent folder of this file
path = os.path.dirname(os.path.abspath('get_birds'))

# make new folder 'data_europe' if it does not already exist
if not os.path.isdir(path + '/data_europe'):
    os.makedirs(path + '/data_europe')

# loop through dataframe row by row
ec = 0
for i in range(df.shape[0]):
    # check, whether folder for class exists
    if not os.path.isdir(path + '/data_europe/' + df['class'][i]):
        os.makedirs(path + '/data_europe/' + df['class'][i])

    # download and store image in corresponding folder
    try:
        dst_path = path + '/data_europe/' + df['class'][i] + '/' + df['file_name'][i]
        urllib.request.urlretrieve(df['url'][i], dst_path)
    except urllib.error.HTTPError:
        print(f"HTTP Error 403: Can't download image {df['url'][i]}")
        ec += 1  # update error counter
        pass

# Some website don't like when this script downloads the images and cause an error saying:
# urllib.error.HTTPError: HTTP Error 403: Forbidden
# So, we create a try/except error handling. We TRY to download it EXCEPT when this error occurs.
# Then, instead,  these images causing the error shall be printed and afterwards the script shall go on (PASS)

print('-----'*7, '\n')
print(f'Could not download {ec}/{df.shape[0]} images ({round(100*ec/df.shape[0],1)}%)')
print('\n')
print(f'Found {ni-df.shape[0]} duplicates. These have been removed.')
