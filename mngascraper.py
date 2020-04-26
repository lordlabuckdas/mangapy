from bs4 import BeautifulSoup
import requests
import os
import urllib.request

# made by lordlabuckdas (https://github.com/lordlabuckdas)

def get_maxchap(url): # function to get the maximum number of chapters available
    req=requests.get(url,allow_redirects=False).text.encode('ascii','replace')
    soup=BeautifulSoup(req,'html.parser')
    for link in soup.find_all('a'):
        if mnga_name.replace('-',' ').title() in str(link.string):
            title=link.string.split()
            return title[-1]

def get_chap(i,url): # function to retrieve the chapter
    try:
        os.makedirs("chap"+str(i))
    except FileExistsError:
        pass
    os.chdir("chap"+str(i))
    j=1
    while(1):
        ch_url=url+"/"+str(j)
        req=requests.get(ch_url,allow_redirects=False).text.encode('ascii','replace')
        soup=BeautifulSoup(req,'html.parser')
        if end_chk(soup):
            for link in soup.findAll('img',{'id':'img'}):
                get_img(link.get('src'),j)
                j+=1
                break
        else:
            break
    os.chdir("..")
    
def get_img(l,j): # function to download the image
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(l, str(j)+".jpg")

def end_chk(soup): # function to check if the page exists
    for link in soup.findAll('h1'):
        if "404" in str(link.string):
            return 0
        else:
            return 1

def mainn(mnga_name): # main function
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
