import json
import requests

from tiktok_vars import headers, params, cookies

lasttok_found = 0
with open('lasttiktok.txt', 'r') as lasttok_file:
    last_tiktok_id = lasttok_file.readline().strip().split("#$%$#")[0]
file = open(f'json/1.json', 'w+', encoding='utf-8')
file.truncate(0)
while lasttok_found == 0:
    response = requests.get('https://us.tiktok.com/api/favorite/item_list', params=params, cookies = cookies, headers = headers)
    # print(response.text)
    response_json = json.loads(response.text)
    params['cursor'] = response_json['cursor']
    file.write(f'{json.dumps(response_json)}\n')
    if last_tiktok_id in response.text:
        lasttok_found = 1

from twitter_vars import url, querystring, headers

parsed_all_tweets = 0
current_cursor = 0
while parsed_all_tweets == False:
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_json = json.loads(response.text)
    file.write(f'{json.dumps(response_json)}\n')
    print(querystring['variables'])
    new_cursor = response_json['data']['bookmark_timeline']['timeline']['instructions'][0]['entries'][-1]['content']['value']
    print(f'old cursor: {current_cursor}, new cursor: {new_cursor}')
    if current_cursor == new_cursor:
        parsed_all_tweets = True
    querystring['variables'] = querystring['variables'].replace(f'\"cursor\":\"{current_cursor}\"',f'\"cursor\":\"{new_cursor}\"')
    current_cursor = new_cursor

file.close()
