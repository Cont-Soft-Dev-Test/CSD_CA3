import requests
import json
import datetime
import pytz

api_url = 'https://api.trello.com/1/'
api_key = ''
api_token = ''
user_id = ''


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
        # assign to the global variable
        global user_id
        user_id = response.json()['idMember']

    else:
        # print the error code
        print('Error in request: {}'.format(response.text))


# fetch member info from the user ID
def get_member_info():
    # build the URL for the request
    # the request is the information about the given user ID
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
        # fetch the board ID list
        return response.json()

    else:
        # print the error code
        print('Error in request: {}'.format(response.text))


# fetch the board info from the board ID
def get_board_info(board_id):
    # build the URL for the request
    # the request is the information about the given board ID
    url = api_url + 'boards/' + board_id

    # set the key and token parameters
    params = {
        'key': api_key,
        'token': api_token,
    }

    # send a request and store the response in a variable
    response = requests.request('GET', url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        return response.json()

    else:
        # print the error code
        print('Error in request: {}'.format(response.text))


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
        print('Error in request: {}'.format(response.text))


# fetch and display the user information
def get_user_info():
    # get the complete member info
    member = get_member_info()

    # print the user ID, the user name, and the user's email address
    print('User ID: {}'.format(member['id']))
    print('Full name: {}'.format(member['fullName']))
    print('Email address: {}'.format(member['email']))
    print('Boards:')

    # fetch the board ID list
    boards = member['idBoards']

    # if the board ID list is valid
    if boards:
        # iterate through the board list
        for board_id in boards:
            # get the board info
            board = get_board_info(board_id)

            # print the board information
            print('\tBoard name: {}'.format(board['name']))
            print('\tBoard URL: {}'.format(board['url']))
            print('\tBoard short URL: {}\n'.format(board['shortUrl']))

    else:
        print('\tThere is no board created yet.\n')


# check if the given board exists
# return the board info if the board exists
def board_exists(board_name):
    # get the board id list from the member info
    member = get_member_info()
    boards = member['idBoards']

    # if the board ID list is valid
    if boards:
        # iterate through the board list
        for board_id in boards:
            # get the board info
            board = get_board_info(board_id)

            if board['name'] == board_name:
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
        print('The new board is created successfully.')

    else:
        print('Error in board creation: {}'.format(response.text))


# add a new card to "To Do" items
def add_todo_items(board_name, team_member_name):
    # get the board info if the board exists
    board_info = board_exists(board_name)

    # if the board exists
    if board_info:
        # fetch board ID from board info
        board_id = board_info['id']

        # get the "To Do" list id from the board ID
        list_id = get_todo_list_id(board_id)

        # set the due date to a week ahead
        # the actual time needs to be changed to UTC timezone and convert to ISO format
        date_to_format = datetime.datetime.now().astimezone(pytz.utc) + datetime.timedelta(days=7)
        due_date = date_to_format.isoformat()

        # build the URL for the request
        # the request posts information to create a new card
        url = api_url + 'cards/'

        # set the key and token parameters
        params = {
            'key': api_key,
            'token': api_token,
            'name': team_member_name + "'s list",
            'desc': 'New work for ' + team_member_name,
            'idList': list_id,
            'due': due_date,
        }

        # send a request and store the response in a variable
        response = requests.request('POST', url, params=params)

        # if the the request was successful
        if response.status_code == 200:
            print('The new card is created successfully.')

        else:
            print('Error in card creation: {}'.format(response.text))

    # if the board does not exist
    else:
        print('The requested board does not exist.')


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
    get_user_id()

    # if the user id is valid
    if user_id:
        get_user_info()

    # if the user id is not valid
    else:
        # print the error message
        print('Error! Incorrect User ID.')

        # exit from the program
        return

    # if the board is already in the list
    if board_exists('New test board'):
        # board will not be created
        print('Board is already created. Creation skipped.')

    # if the board is not in the list
    else:
        # creating a new board
        create_new_board('New test board', 'This is a new board created by the API.')

    # add the new card to the "To Do" list
    add_todo_items('New test board', "Tom")


# Start the main program
if __name__ == '__main__':
    main()
