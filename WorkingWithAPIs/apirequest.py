import requests
import pandas as pd

#  Documentation: http://rickandmortyapi.com/

baseUrl = 'https://rickandmortyapi.com/api/'

endPoint = 'character'

def main_request(baseUrl, endPoint, pageNumber):
    r = requests.get(baseUrl + endPoint + f'?page={pageNumber}')
    return r.json()

def get_pages(response):
    pages = response['info']['pages']
    return pages

def print_parse_json(response):
    for character in response['results']:
        print(character['name'], len(character['episode']))
    return

def parse_json(response):
    charList =[]
    for item in response['results']:
        char = {
            'id' : item['id'],
            'name' : item['name'],
            'no_ep' : len(item['episode']),
        }
        charList.append(char)
    return charList

data = main_request(baseUrl, endPoint, 1)

mainList = []

for x in range(1, get_pages(data) + 1):
    # print(x) # print each page number 
    mainList.extend(parse_json(main_request(baseUrl, endPoint, x)))

print(len(mainList))

df = pd.DataFrame(mainList)

df.to_csv('character_list.csv', index=False)

# print(df.head(), df.tail()) # checking to see if the head and tail are different.