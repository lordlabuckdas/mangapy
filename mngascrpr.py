from bs4 import BeautifulSoup
import requests
import os
import urllib.request
import img2pdf

def latest_manga():
    # fetches the latest manga from homepage
    req = requests.get("http://www.mangapanda.com", allow_redirects=False).text.encode('ascii', 'replace')
    soup = BeautifulSoup(req, 'html.parser')
    i=0
    f=open("latest.txt", "w")
    for a in soup.findAll('strong'):
        if i>4:
            f.write(a.string + " : ")
            for b in soup.find_all('a', class_='chaptersrec'):
                if a.string in b.string:
                    k=b.string.split()
                    f.write(k[-1] + " ")
            f.write("\n")
        else:
            i += 1

def get_maxchap(manga_name,url):
    # fetches the number of chapters available
    req = requests.get(url, allow_redirects=False).text.encode('ascii', 'replace')
    soup = BeautifulSoup(req, 'html.parser')
    for link in soup.find_all('a'):
        if manga_name in str(link.string).replace(' ','-').replace(':','-').replace('--','-').lower():
            title = link.string.split()
            return title[-1]


def get_chap(i,url):
    # fetches the chapter
    j=1
    while(1):
        ch_url = url + "/" + str(j)
        req = requests.get(ch_url, allow_redirects=False).text.encode('ascii', 'replace')
        soup = BeautifulSoup(req, 'html.parser')
        if end_chk(soup):
            for link in soup.findAll('img', {'id':'img'}):
                get_img(link.get('src'),j)
                j += 1
                break
        else:
            pdfconv(i)
            break

def pdfconv(i):
    # converts the images to pdf
    f=open(str(i) + ".pdf", "wb")
    l=[k for k in os.listdir('.') if k.endswith(".jpg")]
    l=sorted(l, key=lambda e: int(e[:-4]))
    f.write(img2pdf.convert(l))
    for m in l:
        os.remove(m)
    f.close()

def get_img(l,j):
    # fetches images
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(l, str(j) + ".jpg")

def end_chk(soup):
    # checks if page num exists
    for link in soup.findAll('h1'):
        if "404" in str(link.string):
            return 0
        else:
            return 1

def disp_ascii():
    # ah, just some fancy text
    print(r'''
    
      ___ ___      __      ___      __      __     _____   __  __    
    /' __` __`\  /'__`\  /' _ `\  /'_ `\  /'__`\  /\ '__`\/\ \/\ \   
    /\ \/\ \/\ \/\ \L\.\_/\ \/\ \/\ \L\ \/\ \L\.\_\ \ \L\ \ \ \_\ \  
    \ \_\ \_\ \_\ \__/.\_\ \_\ \_\ \____ \ \__/.\_\\ \ ,__/\/`____ \  
     \/_/\/_/\/_/\/__/\/_/\/_/\/_/\/___L\ \/__/\/_/ \ \ \/  `/___/> \ 
                                    /\____/          \ \_\     /\___/ 
                                    \_/__/            \/_/     \/__/  
    ''')

def mainn(manga_name):
    url = "http://www.mangapanda.com/"+manga_name
    mchap = get_maxchap(manga_name, url)
    if mchap == None:
        print("\n [!] try a different name")
        return
    print("\n [*] max number of chapters is:", mchap)
    chap_start,chap_end=input("\n [*] enter the start and end chap num: ").split()
    if chap_start>mchap or chap_end>mchap or int(chap_start) <= 0 or int(chap_end) <= 0:
        print("\n [*] enter valid input next time")
        return
    try:
        os.makedirs(manga_name)
    except FileExistsError:
        pass
    os.chdir(os.getcwd() + "/" + manga_name)
    print("\n [*] saving the manga in " + os.getcwd())
    print("\n [*] alrighty, cap! firing off the mangascraper!")
    for i in range(int(chap_start),int(chap_end) + 1):
        get_chap(i, url + "/" + str(i))


if __name__ == "__main__":
    # ascii art
    disp_ascii()
    # menu disp
    print("\n============================================\n\n [!] MENU\n\n [1] download manga\n [2] browse today's manga\n [99] quit\n\n============================================\n ")
    
    try:
        choice = int(input(" [*] enter your choice: "))
        
        if choice == 2:
            print("\n [*] saved it in latest.txt\n")
        
        elif choice == 1:
            manga_name = input("\n [*] enter the name of the manga: ")
            manga_name = manga_name.lower().replace(' ','-').replace(':','-').replace('--','-') # changes to slug notation of mangapanda
            mainn(manga_name)
        
        elif choice == 99:
            print("\n [!] exiting.....\n")
        
        else:
            print("\n [!] enter a goddamn proper choice")
    
    except ValueError:
        print("\n [!] enter a goddamn proper choice")
