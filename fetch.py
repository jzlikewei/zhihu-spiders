import os
import re
import requests
def download(folder,url):
    if not os.path.exists(folder):
        os.makedirs(folder)
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        name = url.split('/')[-1]
        f = open("./"+folder+'/'+name,'wb')
        f.write(req.content)
        f.close()
        return True
    else:
        return False

header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

errs=[]

def fetch(url):
    r = requests.get(url,headers=header)
    text= r.text
    imgs=[]
    jpg = re.compile(r'https://[^\s]*?_r\.jpg')
    jpeg = re.compile(r'https://[^\s]*?_r\.jpeg')
    gif = re.compile(r'https://[^\s]*?_r\.gif')
    png = re.compile(r'https://[^\s]*?_r\.png')

    imgs+=jpg.findall(text)
    imgs+=jpeg.findall(text)
    imgs+=gif.findall(text)
    imgs+=png.findall(text)


    errors = []

    folder = url.split('/')[-1]
    for img_url in imgs:
        if download(folder,img_url):
            print("download :"+img_url)
        else:
            errors.append(img_url)
    return errors

urls=['https://www.zhihu.com/question/22212644','https://www.zhihu.com/question/29814297',
      'https://www.zhihu.com/question/31983868','https://www.zhihu.com/question/20399991']
for url in urls :
    print(url)
    errs+=fetch(url)
with open('error.txt','w') as f:
    print("ERROR URLS:",file=f)
    print(errs,file=f)