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

    # if the request was unsuccessful
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

    # if the request was unsuccessful
    else:
        # print the error code
        print('Error in member info request: {}'.format(response.text))


# fetch the board info from the user ID
def get_board_list(user_id):
    # build the URL for the request
    # the request is the information about the given user ID
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

    # if the request was unsuccessful
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

    # if the request was unsuccessful
    else:
        print('Error in board creation: {}'.format(response.text))


# check if the given list exists
# return the list if it does
def list_exists(board_id, list_name):
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
            if item['name'] == list_name:
                return item

    # if the request was unsuccessful
    else:
        # print the error code
        print('Error in list request: {}'.format(response.text))


# check if the given card exists
# return the card if it does
def card_exists(board_id, card_name):
    # build the URL for the request
    # the request is the card list information about the given board ID
    url = api_url + 'boards/' + board_id + '/cards/'

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
    # the request is the list of checklists about the given card ID
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

    # if the request was unsuccessful
    else:
        print('Error in checklist creation: {}'.format(response.text))


# check if the given check item exists
# return the check item if it does
def check_item_exists(checklist_id, check_item_name):
    # build the URL for the request
    # the request is the check item list information about the given checklist ID
    url = api_url + 'checklists/' + checklist_id + '/checkItems/'

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
        check_item_list = response.json()

        # if the list of checklists is valid
        if check_item_list:
            # iterate through the list of checklists
            for item in check_item_list:
                # if the names match
                if item['name'] == check_item_name:
                    # return the checklist info
                    return item


# create a new check item
def create_new_check_item(checklist_id, check_item_name):
    # build the URL for the request
    # the request posts information to create a new check item
    url = api_url + 'checklists/' + checklist_id + '/checkItems/'

    # set the key and token parameters
    params = {
        'key': api_key,
        'token': api_token,
        'name': check_item_name,
        'idCard': checklist_id,
    }

    # send a request and store the response in a variable
    response = requests.request('POST', url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        print('The new check item "{}" is created successfully.'.format(check_item_name))

    # if the request was unsuccessful
    else:
        print('Error in check item creation: {}'.format(response.text))


# add a specific card to "To Do" items
def add_todo_items(board_name, team_member_name):
    # get the board info if the board exists
    board_info = board_exists(board_name)

    # if the board exists
    if board_info:
        # fetch board ID from board info
        board_id = board_info['id']

        # set the card name
        card_name = team_member_name + "'s list"

        # check if the card exist
        card_info = card_exists(board_id, card_name)

        # if the card exists
        if card_info:
            print('The card "{}" is already created. Skipping creation...'.format(card_info['name']))

        # if the card does not exist
        else:
            # get the "To Do" list ID from the board ID
            list_info = list_exists(board_id, 'To Do')
            list_id = list_info['id']

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

            # if the request was unsuccessful
            else:
                print('Error in card creation: {}'.format(response.text))

        # get the card ID from the list ID
        card_info = card_exists(board_id, card_name)
        card_id = card_info['id']

        # check if the checklist exists
        checklist_info = checklist_exists(card_id, 'Key tasks')

        # if the checklist exists
        if checklist_info:
            print('The checklist "{}" is already created. Skipping creation...'.format(checklist_info['name']))

        # if the checklist does not exist
        else:
            create_new_checklist(card_id, 'Key tasks')

        # update the checklist info and get the id from it
        checklist_info = checklist_exists(card_id, 'Key tasks')
        checklist_id = checklist_info['id']

        # check if the check item exists
        check_item_info = check_item_exists(checklist_id, 'Key task 1')

        # if the check item exists
        if check_item_info:
            print('The check item "{}" is already created. Skipping creation...'.format(check_item_info['name']))

        # if the check item does not exist
        else:
            create_new_check_item(checklist_id, 'Key task 1')

        # check if the check item exists
        check_item_info = check_item_exists(checklist_id, 'Key task 2')

        # if the check item exists
        if check_item_info:
            print('The check item "{}" is already created. Skipping creation...'.format(check_item_info['name']))

        # if the check item does not exist
        else:
            create_new_check_item(checklist_id, 'Key task 2')

        # check if the checklist exists
        checklist_info = checklist_exists(card_id, 'Additional tasks')

        # if the checklist exists
        if checklist_info:
            print('The checklist "{}" is already created. Skipping creation...'.format(checklist_info['name']))

        # if the checklist does not exist
        else:
            create_new_checklist(card_id, 'Additional tasks')

        # update the checklist info and get the id from it
        checklist_info = checklist_exists(card_id, 'Additional tasks')
        checklist_id = checklist_info['id']

        # check if the check item exists
        check_item_info = check_item_exists(checklist_id, 'Additional task 1')

        # if the check item exists
        if check_item_info:
            print('The check item "{}" is already created. Skipping creation...'.format(check_item_info['name']))

        # if the check item does not exist
        else:
            create_new_check_item(checklist_id, 'Additional task 1')

        # check if the check item exists
        check_item_info = check_item_exists(checklist_id, 'Additional task 2')

        # if the check item exists
        if check_item_info:
            print('The check item "{}" is already created. Skipping creation...'.format(check_item_info['name']))

        # if the check item does not exist
        else:
            create_new_check_item(checklist_id, 'Additional task 2')

    # if the board does not exist
    else:
        print('Error creating a card. The requested board does not exist.')


# fetch the checklist list from the board ID
def get_checklist_list(board_id):
    # build the URL for the request
    # the request is the information about the given board ID
    url = api_url + 'boards/' + board_id + '/checklists/'

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

    # if the request was unsuccessful
    else:
        # print the error code
        print('Error in checklist list request: {}'.format(response.text))


# update the checklist item
def update_item(board_name, checklist_item_name, is_complete):
    # initialise the variables
    count_all = 0
    count_completed = 0
    check_item_found = False

    # get the board info if the board exists
    board_info = board_exists(board_name)

    # if the board exists
    if board_info:
        # fetch board ID from board info
        board_id = board_info['id']

        # get the checklist list from the board ID
        checklist_list = get_checklist_list(board_id)

        # if the checklist list in not empty
        if checklist_list:
            # iterate through the checklist list
            for item in checklist_list:
                # get the card ID from the checklist info
                card_id = item['idCard']

                # fetch the check item list
                check_item_list = item['checkItems']

                # iterate through the check items
                for check_item in check_item_list:
                    # count the number of check items
                    count_all += 1

                    # if the check item name matches
                    if check_item['name'] == checklist_item_name:
                        # set check_item_found indicator to true
                        check_item_found = True

                        # fetch the check item ID
                        check_item_id = check_item['id']

                        # determine the state from the is_complete variable
                        if is_complete:
                            # set state string for the API
                            state = 'complete'

                            # increment the completed counter
                            count_completed += 1

                        else:
                            # set state string for the API
                            state = 'incomplete'

                        # build the URL for the request
                        # the request puts information to update a check item
                        url = api_url + 'cards/' + card_id + '/checkItem/' + check_item_id

                        # set the key and token parameters
                        params = {
                            'key': api_key,
                            'token': api_token,
                            'state': state,
                        }

                        # send a request and store the response in a variable
                        response = requests.request('PUT', url, params=params)

                        # if the the request was successful
                        if response.status_code == 200:
                            print('The check item "{}" state is updated to {} successfully.'
                                  .format(checklist_item_name, state))

                        # if the request was unsuccessful
                        else:
                            print('Error in check item update: {}'.format(response.text))
                            return

                    # if the check item state is complete
                    elif check_item['state'] == 'complete':
                        # increment the completed counter
                        count_completed += 1

        # if the checklist list is empty
        else:
            print('Error updating the checklist item. The requested checklist does not exist.')

    # if the board does not exist
    else:
        print('Error updating the checklist item. The requested board does not exist.')

    # if the given check item name is not found
    if not check_item_found:
        print('Error updating the checklist item. The requested check item does not exist.')

    # give feedback about the counted check items
    print('\tNumber of all check items: {}'.format(count_all))
    print('\tNumber of completed check items: {}'.format(count_completed))

    # fetch board ID from board info
    board_id = board_info['id']

    # fetch the card ID from board info
    card_info = card_exists(board_id, "Tom's list")
    card_id = card_info['id']

    # determine the list where the card should be in
    # if the card should be in the "Doing" list
    if 0 < count_completed < count_all:
        list_info = list_exists(board_id, "Doing")

    # if the card should be in the "To Do" list
    elif count_completed == 0:
        list_info = list_exists(board_id, "To Do")

    # if the card should be in the "Done" list
    elif count_completed == count_all:
        list_info = list_exists(board_id, "Done")

    # if there is something wrong with the counted values
    else:
        print('Error in counted check item numbers.')
        return

    # if the list was not found
    if not list_info:
        print('Error finding the list to update the card.')
        return

    # fetch the list ID from the list info
    list_id = list_info['id']

    # build the URL for the request
    # the request puts information to update a card
    url = api_url + 'cards/' + card_id

    # set the key and token parameters
    params = {
        'key': api_key,
        'token': api_token,
        'idList': list_id,
    }

    # send a request and store the response in a variable
    response = requests.request('PUT', url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        print('The card "{}" is updated successfully.'.format(card_info['name']))

    # if the request was unsuccessful
    else:
        print('Error in card update: {}'.format(response.text))


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

    # update a check item on the card
    update_item('New test board', 'Key task 1', True)


# Start the main program
if __name__ == '__main__':
    main()
