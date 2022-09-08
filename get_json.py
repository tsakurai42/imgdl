import json
import requests

from tiktok_vars import cookies, headers, params

lasttok_found = 0
with open('lasttiktok.txt','r') as lasttok_file:
    last_tiktok_id = lasttok_file.readline().strip().split("#$%$#")[0]
file = open(f'json/1.json', 'w+', encoding='utf-8')
file.truncate(0)
while lasttok_found == 0:
    response = requests.get('https://us.tiktok.com/api/favorite/item_list', params=params, cookies=cookies,
                            headers=headers)
    response_json = json.loads(response.text)
    params['cursor'] = response_json['cursor']
    file.write(f'{json.dumps(response_json)}\n')
    if last_tiktok_id in response.text:
        lasttok_found = 1

from twitter_vars import url, querystring, headers

response = requests.request("GET", url, headers=headers, params=querystring)
response_json = json.loads(response.text)
file.write(f'{json.dumps(response_json)}\n')

file.close()