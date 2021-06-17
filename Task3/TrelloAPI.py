import requests
import json

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
        print('Error in request: {}'.format(response.text))


# fetch and display the user information
def get_user_info(user_id):
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
        data = response.json()

        # print the user ID, the user name, and the user's email address
        print('User ID: {}'.format(data['id']))
        print('Full name: {}'.format(data['fullName']))
        print('Email address: {}'.format(data['email']))
        print('Boards:')

        # fetch the board ID list
        boards = data['idBoards']

        # if the board ID list is valid
        if boards:
            # iterate through the board list
            for board_id in boards:
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
                    board = response.json()

                    # print the board information
                    print('\tBoard name: {}'.format(board['name']))
                    print('\tBoard URL: {}'.format(board['url']))
                    print('\tBoard short URL: {}\n'.format(board['shortUrl']))

                else:
                    # print the error code
                    print('Error in request: {}'.format(response.text))

        else:
            print('\tThere is no board created yet.\n')

    else:
        # print the error code
        print('Error in request: {}'.format(response.text))


# check if the given board exists
def board_exists(user_id, board_name):
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
        boards = response.json()['idBoards']

        # if the board ID list is valid
        if boards:
            # iterate through the board list
            for board_id in boards:
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
                    board = response.json()

                    if board['name'] == board_name:
                        return True

                else:
                    # print the error code
                    print('Error in request: {}'.format(response.text))

        # if there is no board ID or the name not found
        return False

    else:
        # print the error code
        print('Error in request: {}'.format(response.text))


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
        print('The new board has been created successfully.')

    else:
        print('Error in board creation: {}'.format(response.text))


# main program
def main():
    try:
        # try to open the file to load the API key and token
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

    # if the user id is valid
    if user_id:
        get_user_info(user_id)

    # if the user id is not valid
    else:
        # print the error message
        print('Error! User ID is missing.')

        # exit from the program
        return

    if board_exists(user_id, 'New test board'):
        # board will not be created
        print('Board is already created. Creation skipped.')

    else:
        # creating a new board
        create_new_board('New test board', 'This is a new board created by the API.')


# Start the main program
if __name__ == '__main__':
    main()
