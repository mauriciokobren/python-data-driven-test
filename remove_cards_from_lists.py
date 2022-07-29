import requests
import secrets

headers = {"Accept": "application/json"}
query = {}
query['key'] = secrets.trello_apikey
query['token'] = secrets.trello_apitoken

def remove_cards(url):
    response = requests.get(url=url,data=query,headers=headers)

    for card in response.json():
        print("Card id: " + card['id'])
        card_id = card['id']
        delete_url = f'https://api.trello.com/1/cards/{card_id}'
        response = requests.delete(url=delete_url,data=query,headers=headers)
        print(response.text)
        print(response.status_code)

"""to do list"""
remove_cards('https://api.trello.com/1/lists/62e3069f348b914c71fa6944/cards')

"""doing list"""
remove_cards('https://api.trello.com/1/lists/62e3069f348b914c71fa6945/cards')


