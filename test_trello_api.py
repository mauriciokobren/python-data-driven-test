import csv
import requests
import pytest
import secrets

""" variables with data used during the tests"""
trello_apikey = secrets.trello_apikey
trello_apitoken = secrets.trello_apitoken

base_url='https://api.trello.com/1'
cards_endpoint = 'cards'
todo_list_id = '62e3069f348b914c71fa6944'
doing_list_id = '62e3069f348b914c71fa6945'
headers = {"Accept": "application/json"}


def read_test_data_from_csv(file):
    test_data = []
    with open(file, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=';')
        for row in data:
            test_data.append(row)
    return test_data

def get_list_id(list_name):
	if list_name == 'To Do':
		list_id = todo_list_id
	elif list_name == 'Doing':
		list_id = doing_list_id
	else:
		list_id = ''
	return list_id

@pytest.mark.parametrize('card_name,card_desc,list,status', read_test_data_from_csv('trello_api_create_cards.csv'))
def test_card_creation(card_name,card_desc,list,status):
	list_id = get_list_id(list)

	url = f'{base_url}/{cards_endpoint}'
	print(url)
	card = {}
	card['name']= card_name
	card['desc']= card_desc
	card['idList']= list_id
	card['key']= trello_apikey
	card['token']= trello_apitoken
	
	"""calling the endpoint"""
	response = requests.post(url=url,data=card,headers=headers)

	"""checking if expected values are found in response"""
	assert response.status_code == int(status)
	if response.status_code == 200:	
		response_json = response.json()
		assert response_json['name'] == card_name
		assert response_json['desc'] == card_desc
		assert response_json['idList'] == list_id 
		assert 'id' in response_json


@pytest.mark.parametrize('card_name,card_desc,list,new_card_name,new_card_desc,new_list,status', read_test_data_from_csv('trello_api_update_cards.csv'))
def test_update_cards(card_name,card_desc,list,new_card_name,new_card_desc,new_list,status):

	"""first we need to create the card"""
	list_id = get_list_id(list)
	
	url = f'{base_url}/{cards_endpoint}'
	card = {}
	card['name']= card_name
	card['desc']= card_desc
	card['idList']= list_id
	card['key']= trello_apikey
	card['token']= trello_apitoken
	
	response = requests.post(url=url,data=card,headers=headers)
	newcard_id = response.json()['id']
	
	"""then tries to update the existing card"""
	new_list_id = get_list_id(new_list)
	card_update = {}
	card_update['name']= new_card_name
	card_update['desc']= new_card_desc
	card_update['idList']= new_list_id 
	card_update['key']= trello_apikey
	card_update['token']= trello_apitoken
	response = requests.put(url=f'{url}/{str(newcard_id)}',data=card_update,headers=headers)

	"""and check if expected values are found in response"""
	assert response.status_code == int(status)
	if response.status_code == 200:	
		response_json = response.json()
		assert response_json['name'] == new_card_name
		assert response_json['desc'] == new_card_desc
		assert response_json['idList'] == new_list_id 
		assert 'id' in response_json
