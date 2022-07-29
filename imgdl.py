from requests import get
from bs4 import BeautifulSoup
import re
import time
from splinter import Browser
import json
import glob

browser = Browser('firefox', **{'executable_path': 'C:/Users/rawr/Downloads/geckodriver.exe'})

url_file = open('urls.txt','a')

files = [file for file in glob.glob('json/*')]
for file_num, file_name in enumerate(files):
    f0 = open(file_name,encoding='utf-8')
    f1 = json.load(f0)
    g = f1['data']['bookmark_timeline']['timeline']['instructions'][0]['entries']
    for _ in g:
        if 'tweet' in _['entryId']:
            try:
                screenname = _['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['screen_name']
                tweet_id = _['content']['itemContent']['tweet_results']['result']['rest_id']
                url_file.write(f'https://twitter.com/{screenname}/status/{tweet_id}\n')
            except:
                continue
url_file.close()

f = open('urls.txt', 'r')
url_list = [l.strip('\n') for l in f.readlines()]
f.close()
total_dl = len(url_list)
for count, url in enumerate(url_list):
    print(f'Downloading #{count+1} of {total_dl}: {url}')
    browser.visit(url)
    time.sleep(2)
    soup = BeautifulSoup(browser.html, 'html.parser')
    domain = url.split('/')[2]
    if 'instagram' in domain:
        print(domain)
        img_html = soup.find_all('img')
        img_url = img_html[0].get('src')
        print(img_url)
        req = get(img_url)
        file = open(f'images/{url.split("://")[1][4:].replace("/", "")}.jpg', 'wb')
        for chunk in req.iter_content(1000000):
            file.write(chunk)
        file.close()

    elif 'twitter' in domain:
        try:
            prim_div = soup.find_all('div', attrs={
                'style': 'transform: translateY(0px); position: absolute; width: 100%; transition: opacity 0.3s ease-out 0s;'})[
                0]
        except:
            print(f"Couldn't find the right div for images")
            f = open('manual.txt', 'a')
            f.write(f'{url[8:]}\n')
            f.close()
            continue
        if prim_div.findAll(
                text='Age-restricted adult content. This content might not be appropriate for people under 18 years old. To view this media, you’ll need to '):
            print(f'Age-restricted, Written to manual.txt')
            f = open('manual.txt', 'a')
            f.write(f'{url[8:]}\n')
            f.close()

            continue

        if prim_div.findAll(text='The following media includes potentially sensitive content. '):
            # XPath of the view button
            # xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/span/span'
            # xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/span/span'
            xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/div/article/div/div/div/div[3]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/span/span'
            try:
                browser.find_by_xpath(xpath).first.click()
                time.sleep(1)
                soup = BeautifulSoup(browser.html, 'html.parser')
                prim_div = soup.find_all('div', attrs={
                    'style': 'transform: translateY(0px); position: absolute; width: 100%; transition: opacity 0.3s ease-out 0s;'})[
                    0]
            except:
                print(f"XPath may have changed? Written to redo.txt")
                f = open('redo.txt', 'a')
                f.write(f'{url[8:]}\n')
                f.close()
                continue

        try:
            img_url = prim_div.select_one('img[alt="Image"]').get('src')
        except:
            print("Couldn't find the image, maybe it has alt text")
            f = open('manual.txt', 'a')
            f.write(f'{url[8:]}\n')
            f.close()
            continue
        split_url = re.split('[?&]', img_url)
        img_url = f'{split_url[0]}?{split_url[1]}&name=orig'

        req = get(img_url)
        if req.status_code != 200:
            for _ in range(3):
                req = get(img_url)
                if req.status_code == 200:
                    break
            print(req.status_code)
            f2 = open('redo.txt', 'a')
            f2.write(f'{url}\n')
            f2.close()

        file = open(f'{url.split("://")[1].replace("/", "")}.{split_url[1].split("=")[1]}', 'wb')
        for chunk in req.iter_content(1000000):
            file.write(chunk)
        file.close()

browser.quit()