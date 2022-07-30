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
url_file.truncate(0)
files = [file for file in glob.glob('json/*')]
for file_num, file_name in enumerate(files):
    f0 = open(file_name,encoding='utf-8')
    for line in f0:
        f1 = json.loads(line)
        if 'data' in f1:
            g = f1['data']['bookmark_timeline']['timeline']['instructions'][0]['entries']
            for _ in g:
                if 'tweet' in _['entryId']:
                    try:
                        if 'thumb' in _['content']['itemContent']['tweet_results']['result']['legacy']['entities']['media'][0]['media_url_https']:
                            continue
                        url_to_write = 'twitter#$%$#'
                        expanded_url = _['content']['itemContent']['tweet_results']['result']['legacy']['entities']['media'][0][
                            'expanded_url'][8:-8]
                        url_to_write += f'{expanded_url}'
                        for each_dict in _['content']['itemContent']['tweet_results']['result']['legacy']['entities']['media']:
                            # print(each_dict)
                            # print(each_dict['media_url_https'])
                            url_split = each_dict['media_url_https'].rsplit('.',1)
                            url = f'{url_split[0]}?format={url_split[1]}&name=orig'
                            url_to_write += f'#$%$#{url}'

                        # for _ in range(len(_['content']['itemContent']['tweet_results']['result']['legacy']['entities']['media'])):
                        #     url_original = _['content']['itemContent']['tweet_results']['result']['legacy']['entities']['media'][_]['media_url_https']
                        #     url_split = url_original.rsplit('.', 1)
                        #     url = f'{url_split[0]}?format={url_split[1]}&name=orig'

                        url_file.write(f'{url_to_write}\n')
                    except:
                        continue
        elif 'itemList' in f1:      #tiktoks have an itemlist
            for _ in f1['itemList']:
                tiktok_id = _['id']
                tiktok_desc = re.sub(r"[^A-Za-z0-9 #!]+","",_['desc'])
                tiktok_videourl = _['video']['downloadAddr']
                tiktok_author = _['author']['uniqueId']
                try:
                    url_file.write(f'tiktok#$%$#{tiktok_id}#$%$#{tiktok_videourl}#$%$#{tiktok_desc}#$%$#{tiktok_author}\n')
                except:
                    print(tiktok_desc)  # descriptions with emojis were throwing an error. regexed removed above now
                    continue
url_file.close()

f = open('urls.txt', 'r')
url_list = [l.strip('\n') for l in f.readlines()]
f.close()
total_dl = len(url_list)

skiptok = 0
first_tiktok = 0

with open('lasttiktok.txt') as lasttok_file:
    last_tiktok = lasttok_file.readline().strip()

for count, pre_url in enumerate(url_list):
    url = pre_url.split('#$%$#')
    if url[0] == 'twitter':
        print(f'Downloading #{count + 1} of {total_dl}: {url[1]}',flush=True)
        for each_image in range(2,len(url)):
            print(each_image)
            req = get(url[each_image])
            if req.status_code != 200:
                for _ in range(3):
                    req = get(url[each_image])
                    if req.status_code == 200:
                        break
                print(req.status_code)
                f2 = open('redo.txt', 'a')
                f2.write(f'{url[1]}\n')
                f2.close()
            if len(url) == 3:
                file = open(f'{url[1].replace("/","")}.jpg', 'wb')
            else:
                file = open(f'{url[1].replace("/", "")} {each_image-1}.jpg', 'wb')
            for chunk in req.iter_content(1000000):
                file.write(chunk)
            file.close()
    elif skiptok != 0:
        print(f'Skipping this tiktok, already downloaded',flush=True)
    elif url[0] == 'tiktok':
        # print(url[1])
        if first_tiktok == 0:
            # print(f'1st if')
            with open('lasttiktok.txt', 'r+') as lasttok_file:
                lasttok_file.truncate(0)
                lasttok_file.write(f'{url[1]}')    # write first one to file
            first_tiktok = 1
        if url[1] == last_tiktok:
            # print(f'2nd if')
            skiptok = 1
            print(f'All tiktoks from here on out were already downloaded',flush=True)
            continue
        print(f'Downloading #{count + 1} of {total_dl}: @{url[4]} - {url[1]}',flush=True)
        if os.path.isfile(f'@{url[4]} - {url[1]} - {url[3][:60]}.mp4'):
            print('already downloaded')
            continue
        req = get(url[2])
        if req.status_code != 200:
            for _ in range(3):
                req = get(url[2])
                if req.status_code == 200:
                    break
            print(req.status_code)
            f2 = open('redo.txt', 'a')
            f2.write(f'tiktok.com/@{url[4]}/video/{url[1]}\n')
            f2.close()
        file = open(f'@{url[4]} - {url[1]} - {url[3][:60]}.mp4', 'wb')
        for chunk in req.iter_content(1000000):
            file.write(chunk)
        file.close()
    else:
        print('wtf did you doooo?')