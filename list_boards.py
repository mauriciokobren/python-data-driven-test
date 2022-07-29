import requests
import secrets

headers = {"Accept": "application/json"}
query = {}
query['key'] = secrets.trello_apikey
query['token'] = secrets.trello_apitoken

url = 'https://api.trello.com/1/members/me/boards'

response = requests.get(url=url,data=query,headers=headers)

for board in response.json():
    print("Board id: " + board['id'] + " name: " + board['name'])

    lists = requests.get(url='https://api.trello.com/1/boards/'+board['id']+'/lists',data=query,headers=headers)

    for list in lists.json():
        print(".... List id: " + list['id'] + ' name: ' + list['name'])
