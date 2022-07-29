# python-data-driven-test

## Introduction
This is a simple example of data driven tests using python requests and pytest. The tests are done over Trello APIs.  
To see more details about Trello API please visit https://developer.atlassian.com/cloud/trello/rest/api-group-actions/ .  

## About Trello
Trello makes it easy for teams to get work done. No matter the project, workflow, or type of team, Trello can help keep things organized.  
In Trello you can create a board, add columns to define the workflow and then add yours tasks and assign them to team members. This way collaboration is easy. To know more please visti https://trello.com/home.  

## Requirements
This project is based in python and it uses the following libraries:  

**requests**  
This library allows to send HTTP requests like get, post, put, delete.  
Website: https://requests.readthedocs.io/en/latest/  
Installation: ```python -m pip install requests```  

**pytest**  
Pytest is a testing framework that can be used to write various types of software tests, including unit tests, integration tests, end-to-end tests and functional tests. Its features include parametrized testing and fixtures.  
Website: https://docs.pytest.org/en/7.1.x/contents.html  
Installation: ```pip install -U pytest```  

**pytest-html**  
pytest-html is a plugin for pytest that generates a HTML report for test results.  
Website: https://pypi.org/project/pytest-html/  
Installation: ```pip install pytest-html```  

## Test Structure
Beforing going to code, let's understand what is data-driven test. According to https://smartbear.com/blog/your-guide-to-data-driven-testing/ :
> Data-driven testing (DDT) is data that is external to your functional tests, and is loaded and used to extend your automated test cases. You can take the same test case and run it with as many different inputs as you like, thus getting better coverage from a single test. This could be an Excel document, an XML file, a MySQL database, etc.  

With this in mind, two csv files were created to be used in the tests in this project:
- **trello_api_create_cards.csv**: this file is used to test Card Creation. Each row represents a new card containing card_name, card_desc, list (the column in the board in which the card will be added) and status (response status like 200=OK,etc). At the moment this file has 9 rows meaning that different combinations are used to create Cards, like positive test (name, description and list are OK, empty name) and negative test (non exisiting list).
- **trello_api_update_cards.csv**: this file is used to test Card Edition. Each row represents a card. Part of the columns in the csv are used to create the card (card_name,card_desc,list) and the other part has the new values after the change (new_card_name,new_card_desc,new_list,status). At the moment this file has 4 rows, with different combinations of data representing different use cases.

The file **test_trello_api.py** has the tests properly saying. 
*test_card_creation* is defined in row 35:  
row 34: ```@pytest.mark.parametrize('card_name,card_desc,list,status', read_test_data_from_csv('trello_api_create_cards.csv'))```  
row 35: ```def test_card_creation(card_name,card_desc,list,status):```  

With *@pytest.mark.parametrize* pytest will run the *test_card_creation* for each row existing in the supplied csv file following the mapping defined by *'card_name,card_desc,list,status'*. It's important to note that the mapping order is equal to the arguments expected by *test_card_creation*.  

In a similar way, *test_update_cards* is defined in row 61:  
row 60: ```@pytest.mark.parametrize('card_name,card_desc,list,new_card_name,new_card_desc,new_list,status', read_test_data_from_csv('trello_api_update_cards.csv'))```  
row 61: ```def test_update_cards(card_name,card_desc,list,new_card_name,new_card_desc,new_list,status):```  

Both test methods use HTTP request to Trello API and then check the response, doing assertions to confirm returned data match the expected values.

Regarding the API usage, please note that API Key and Token are needed execute the requests.  
For security reasons, API Key and Token are stored in a dedicated file named secrets.py.  
After you clone this repository you should edit this file and put the real values for your Trello account.  
Please visit the page below to see how to create API Key and Token:  
https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#authentication-and-authorization  

When creating a new card or editing an existing one, it's not needed to specify the board. However, the list (column board) is mandatory.  
In the csv files I preferred to use the list name because it's more user friendly. However I created *get_list_id(list_name)* to get the list id based on the name informed in the argument.  
To help you discover the id of the lists in your Trello boards, I created *list_boards.py*. It will list the id and name for each list in each of your boards. To run it just call ``` python list_boards.py```.  

After you have run the tests, you can delete the cards from your board by running ```remove_cards_from_lists.py```.  

## Running the test
To run the tests just execute this command in your bash:  
```python pytest test_trello_api.py --html=report\trello_api_ddt.htm --self-contained-html```

pytest-html plugin will create a beautiful html report in file *trello_api_ddt.htm* inside *report* folder.  
You should also see test results in the console, similar to the image below:  
![Sample report](report.png)  


## References
This work is based in the following articles written by Bas Dijkstra:  
https://www.ontestautomation.com/writing-tests-for-restful-apis-in-python-using-requests-part-1-basic-tests/
https://www.ontestautomation.com/writing-tests-for-restful-apis-in-python-using-requests-part-2-data-driven-tests/