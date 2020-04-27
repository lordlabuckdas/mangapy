from bs4 import BeautifulSoup
import requests
import os
import urllib.request
import img2pdf

def get_maxchap(url):
    req=requests.get(url,allow_redirects=False).text.encode('ascii','replace')
    soup=BeautifulSoup(req,'lxml')
    for link in soup.find_all('a'):
        if mnga_name.replace('-',' ').title() in str(link.string):
            title=link.string.split()
            return title[-1]

def get_chap(i,url):
    j=1
    while(1):
        ch_url=url+"/"+str(j)
        req=requests.get(ch_url,allow_redirects=False).text.encode('ascii','replace')
        soup=BeautifulSoup(req,'lxml')
        if end_chk(soup):
            for link in soup.findAll('img',{'id':'img'}):
                get_img(link.get('src'),j)
                j+=1
                break
        else:
            pdfconv(i)
            break

def pdfconv(i):
    f=open(str(i)+".pdf","wb")
    l=[k for k in os.listdir('.') if k.endswith(".jpg")]
    l=sorted(l,key=lambda e: int(e[:-4]))
    f.write(img2pdf.convert(l))
    for m in l:
        os.remove(m)
    f.close()

def get_img(l,j):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(l, str(j)+".jpg")

def end_chk(soup):
    for link in soup.findAll('h1'):
        if "404" in str(link.string):
            return 0
        else:
            return 1

def mainn(mnga_name):
    url="http://www.mangapanda.com/"+mnga_name
    print("\nmax number of chapters is:",get_maxchap(url))
    chap_start,chap_end=input("\nenter the start and end chap num: ").split()
    print("\nalrighty, cap! firing off the mangacrawler!\n")
    for i in range(int(chap_start),int(chap_end)+1):
        get_chap(i,url+"/"+str(i))

mnga_name=input("\nenter the name of the manga: ")
mnga_name=mnga_name.lower().replace(' ','-')

try:
    os.makedirs(mnga_name)
except FileExistsError:
    pass

os.chdir(os.getcwd()+"/"+mnga_name)
print("\nsaving the manga in "+os.getcwd())

mainn(mnga_name)