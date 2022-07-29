from requests import get
import os.path
# from bs4 import BeautifulSoup
import re
import time
# from splinter import Browser
import json
import glob

# browser = Browser('firefox', **{'executable_path': 'C:/Users/rawr/Downloads/geckodriver.exe'})

url_file = open('urls.txt','a')
files = [file for file in glob.glob('json/*')]
for file_num, file_name in enumerate(files):
    f0 = open(file_name,encoding='utf-8')
    for line in f0:
        f1 = json.loads(line)
        if 'data' in f1:
            g = f1['data']['bookmark_timeline']['timeline']['instructions'][0]['entries']
            for _ in g:
                if 'tweet' in _['entryId']:
                    url_original = _['content']['itemContent']['tweet_results']['result']['legacy']['entities']['media'][0]['media_url_https']
                    try:
                        url_original = _['content']['itemContent']['tweet_results']['result']['legacy']['entities']['media'][0]['media_url_https']
                        url_split = url_original.rsplit('.', 1)
                        url = f'{url_split[0]}?format={url_split[1]}&name=orig'
                        expanded_url_original = _['content']['itemContent']['tweet_results']['result']['legacy']['entities']['media'][0]['expanded_url']
                        expanded_url = expanded_url_original[8:-8]
                        url_file.write(f'{url}###{expanded_url}\n')
                    except:
                        continue
        elif 'itemList' in f1:
            g = f1['itemList']
            print(len(g))
            for _ in g:
                tiktok_id = _['id']
                tiktok_desc = re.sub(r"[^A-Za-z0-9 #!]+","",_['desc'])
                tiktok_videourl = _['video']['downloadAddr']
                tiktok_author = _['author']['uniqueId']
                try:
                    url_file.write(f'{tiktok_id}###{tiktok_videourl}###{tiktok_desc}###{tiktok_author}\n')
                except:
                    print(tiktok_desc)
                    continue
url_file.close()

f = open('urls.txt', 'r')
url_list = [l.strip('\n') for l in f.readlines()]
f.close()
total_dl = len(url_list)
for count, pre_url in enumerate(url_list):
    url = pre_url.split('###')
    if len(url) == 2:
        print(f'Downloading #{count + 1} of {total_dl}: {url[1]}',flush=True)
        req = get(url[0])
        if req.status_code != 200:
            for _ in range(3):
                req = get(url[0])
                if req.status_code == 200:
                    break
            print(req.status_code)
            f2 = open('redo.txt', 'a')
            f2.write(f'{url[1]}\n')
            f2.close()

        file = open(f'{url[1].replace("/","")}.jpg', 'wb')
        for chunk in req.iter_content(1000000):
            file.write(chunk)
        file.close()
    elif len(url) == 4:
        print(f'Downloading #{count + 1} of {total_dl}: @{url[3]} - {url[0]}',flush=True)
        if os.path.isfile(f'@{url[3]} - {url[0]} - {url[2][:40]}.mp4'):
            print('already downloaded')
            continue
        req = get(url[1])
        if req.status_code != 200:
            for _ in range(3):
                req = get(url[1])
                if req.status_code == 200:
                    break
            print(req.status_code)
            f2 = open('redo.txt', 'a')
            f2.write(f'tiktok.com/@{url[3]}/video/{url[0]}\n')
            f2.close()
        file = open(f'@{url[3]} - {url[0]} - {url[2][:40]}.mp4', 'wb')
        for chunk in req.iter_content(1000000):
            file.write(chunk)
        file.close()
    else:
        print('wtf?')