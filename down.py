import re, zipfile, os
from urllib.request import urlopen

def download(url):

    u = urlopen(url)
    file_name =  url.split('/')[-1]
    f = open(file_name, 'wb')
    file_size = int(u.getheader('Content-Length'))
    print("Downloading: %s Bytes: %s" % (file_name, file_size))
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print(status),

    f.close()
    if file_name.split('.')[1] == 'zip':
        try:
            zf=zipfile.ZipFile(file_name)
            zf.extractall()
        except IOError:
            print("Unable extract file")


def get_file(base,file_name):

        file_txt = file_name.split('.')[0]+'.txt'
        if not os.path.isfile(file_txt):
            download(base+'/'+file_name)
        else:
            print('[ '+file_txt+' ] already exists.')

        f = open(file_txt)

        return f

def to_list(f):
    list_cities = []
    for it in f:
        #print(it)
        list_cities.append(re.split('\t+?',it))
    return list_cities