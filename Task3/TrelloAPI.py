import requests
import json
import datetime
import pytz

api_url = 'https://api.trello.com/1/'
api_key = ''
api_token = ''


# fetch the user ID from the token info
def get_user_id():
    # build the URL for the request
    # the request is the information about the given token
    url = api_url + 'tokens/' + api_token

    # set the key and token parameters
    params = {
        'key': api_key,
        'token': api_token,
    }

    # send a request and store the response in a variable
    response = requests.request('GET', url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        # return the user ID
        return response.json()['idMember']

    else:
        # print the error code
        print('Error in user ID request: {}'.format(response.text))


# fetch member info from the user ID
def get_member_info(user_id):
    # build the URL for the request
    # the request is the member information about the given user ID
    url = api_url + 'members/' + user_id

    # set the key and token parameters
    params = {
        'key': api_key,
        'token': api_token,
    }

    # send a request and store the response in a variable
    response = requests.request('GET', url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        # return the member info
        return response.json()

    else:
        # print the error code
        print('Error in member info request: {}'.format(response.text))


# fetch the board info from the user ID
def get_board_list(user_id):
    # build the URL for the request
    # the request is the information about the given board ID
    url = api_url + 'members/' + user_id + '/boards/'

    # set the key and token parameters
    params = {
        'key': api_key,
        'token': api_token,
    }

    # send a request and store the response in a variable
    response = requests.request('GET', url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        # return the board list
        return response.json()

    else:
        # print the error code
        print('Error in board list request: {}'.format(response.text))


# fetch and display the user information
def get_user_info(user_id):
    # get the member info from the user ID
    member_info = get_member_info(user_id)

    # print the user ID, the user name, and the user's email address
    print('\nUser info')
    print('=========')
    print('User ID: {}'.format(member_info['id']))
    print('Full name: {}'.format(member_info['fullName']))
    print('Email address: {}'.format(member_info['email']))
    print('Boards:')

    # get the board list from the user ID
    board_info = get_board_list(user_id)

    # if the board list is valid
    if board_info:
        # iterate through the board list
        for board in board_info:
            # print the board information
            print('\tBoard name: {}'.format(board['name']))
            print('\tBoard URL: {}'.format(board['url']))
            print('\tBoard short URL: {}\n'.format(board['shortUrl']))

    else:
        print('\tThere is no board created yet.\n')


# check if the given board exists
# return the board info if it does
def board_exists(board_name):
    # get the board list from the user id
    user_id = get_user_id()
    board_list = get_board_list(user_id)

    # if the board list is valid
    if board_list:
        # iterate through the board list
        for board in board_list:
            # if the names match
            if board['name'] == board_name:
                # return the board info
                return board


# create a new board
def create_new_board(board_name, board_description):
    # build the URL for the request
    # the request posts information to create a new board
    url = api_url + 'boards/'

    # set the key and token parameters
    params = {
        'key': api_key,
        'token': api_token,
        'name': board_name,
        'desc': board_description,
    }

    # send a request and store the response in a variable
    response = requests.request('POST', url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        print('The new board "{}" is created successfully.'.format(board_name))

    else:
        print('Error in board creation: {}'.format(response.text))


# fetch the "To Do" list ID from the board ID
def get_todo_list_id(board_id):
    # build the URL for the request
    # the request is the information about the given board ID
    url = api_url + 'boards/' + board_id + '/lists/'

    # set the key and token parameters
    params = {
        'key': api_key,
        'token': api_token,
    }

    # send a request and store the response in a variable
    response = requests.request('GET', url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        # store the list of the lists in a variable
        lists = response.json()

        # find the "To Do" list ID
        for item in lists:
            if item['name'] == 'To Do':
                return item['id']

    else:
        # print the error code
        print('Error in list request: {}'.format(response.text))


# check if the given card exists
# return the card if it does
def card_exists(list_id, card_name):
    # build the URL for the request
    # the request is the card list information about the given list ID
    url = api_url + 'lists/' + list_id + '/cards/'

    # set the key and token parameters
    params = {
        'key': api_key,
        'token': api_token,
    }

    # send a request and store the response in a variable
    response = requests.request('GET', url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        # store the list of the lists in a variable
        card_list = response.json()

        # if the card list is valid
        if card_list:
            # iterate through the card list
            for item in card_list:
                # if the names match
                if item['name'] == card_name:
                    # return the card info
                    return item


# check if the given checklist exists
# return the checklist if it does
def checklist_exists(card_id, checklist_name):
    # build the URL for the request
    # the request is the card list information about the given list ID
    url = api_url + 'cards/' + card_id + '/checklists/'

    # set the key and token parameters
    params = {
        'key': api_key,
        'token': api_token,
    }

    # send a request and store the response in a variable
    response = requests.request('GET', url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        # store the list of the checklists in a variable
        checklist_list = response.json()

        # if the list of checklists is valid
        if checklist_list:
            # iterate through the list of checklists
            for item in checklist_list:
                # if the names match
                if item['name'] == checklist_name:
                    # return the checklist info
                    return item


# create a new checklist
def create_new_checklist(card_id, checklist_name):
    # build the URL for the request
    # the request posts information to create a new checklist
    url = api_url + 'checklists/'

    # set the key and token parameters
    params = {
        'key': api_key,
        'token': api_token,
        'name': checklist_name,
        'idCard': card_id,
    }

    # send a request and store the response in a variable
    response = requests.request('POST', url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        print('The new checklist "{}" is created successfully.'.format(checklist_name))

    else:
        print('Error in checklist creation: {}'.format(response.text))


# add a specific card to "To Do" items
def add_todo_items(board_name, team_member_name):
    # get the board info if the board exists
    board_info = board_exists(board_name)

    # if the board exists
    if board_info:
        # fetch board ID from board info
        board_id = board_info['id']

        # get the "To Do" list ID from the board ID
        list_id = get_todo_list_id(board_id)

        # set the card name
        card_name = team_member_name + "'s list"

        # check if the card exist
        card_info = card_exists(list_id, card_name)

        # if the card exists
        if card_info:
            print('The card "{}" is already created. Skipping creation...'.format(card_info['name']))

        # if the card does not exist
        else:
            # set the due date to a week ahead
            # the actual time needs to be changed to UTC timezone and convert into ISO format
            date_to_format = datetime.datetime.now().astimezone(pytz.utc) + datetime.timedelta(days=7)
            due_date = date_to_format.isoformat()

            # build the URL for the request
            # the request posts information to create a new card
            url = api_url + 'cards/'

            # set the key and token parameters
            params = {
                'key': api_key,
                'token': api_token,
                'name': card_name,
                'desc': 'New work for ' + team_member_name,
                'idList': list_id,
                'due': due_date,
            }

            # send a request and store the response in a variable
            response = requests.request('POST', url, params=params)

            # if the the request was successful
            if response.status_code == 200:
                print('The new card "{}" is created successfully.'.format(card_name))

            else:
                print('Error in card creation: {}'.format(response.text))

        # get the card ID from the list ID
        card_info = card_exists(list_id, card_name)
        card_id = card_info['id']

        checklist_info = checklist_exists(card_id, 'Key tasks')

        if checklist_info:
            print('The checklist "{}" is already created. Skipping creation...'.format(checklist_info['name']))

        else:
            create_new_checklist(card_id, 'Key tasks')

        checklist_info = checklist_exists(card_id, 'Additional tasks')

        if checklist_info:
            print('The checklist "{}" is already created. Skipping creation...'.format(checklist_info['name']))

        else:
            create_new_checklist(card_id, 'Additional tasks')

    # if the board does not exist
    else:
        print('Error creating a card. The requested board does not exist.')


# main program
def main():
    # try to load the API key and token
    try:
        # open the file to load the API key and token
        with open('keys.json') as file:
            # load the json keys to a variable
            keys = json.load(file)

            # define the change to global variables
            global api_key
            global api_token

            # assign the keys
            api_key = keys['API_KEY']
            api_token = keys['API_TOKEN']

    # if an IO error occurs
    except IOError as err:
        # print the error message
        print('IO error: {}'.format(err))

        # exit from the program
        return

    # get the user id from the API token info
    user_id = get_user_id()

    # get the user info
    get_user_info(user_id)

    # get the info about the given board if exists
    board_info = board_exists("New test board")

    # check if the given board exists
    if board_info:
        print('The board "{}" is already created. Skipping creation...'.format(board_info['name']))

    # if the board does not exist
    else:
        create_new_board('New test board', "This is a new test board created by the API.")

    # add a specific card to the "To Do" list
    add_todo_items("New test board", "Tom")


# Start the main program
if __name__ == '__main__':
    main()
