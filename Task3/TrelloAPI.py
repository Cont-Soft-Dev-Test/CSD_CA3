import requests
import json

api_url = "https://api.trello.com/1/"


# fetch the user id from the token info
def get_user_id(api_key, api_token):

    # build the URL for the request
    # the request is the information about the given token
    url = api_url + 'tokens/' + api_token

    # set the key and token parameters
    params = {
        "key": api_key,
        "token": api_token,
    }

    # send a request and store the response in a variable
    response = requests.request("GET", url, params=params)

    # if the the request was successful
    if response.status_code == 200:
        # return the user id
        return response.json()['idMember']


# main program
def main():

    try:
        # try to open the file to load the API key and token
        with open('keys.json') as file:
            keys = json.load(file)
            api_key = keys["API_KEY"]
            api_token = keys["API_TOKEN"]

    # if an IO error occurs
    except IOError as err:
        # print the error message
        print("IO error: {}".format(err))
        # exit from the program
        return

    # get the user id from the API token info
    user_id = get_user_id(api_key, api_token)

    # if the user id is valid
    if user_id:
        print(user_id)

    # if the user id is not valid
    else:
        # print the error message
        print("Error! User ID is missing.")
        # exit from the program
        return


# Start the main program
if __name__ == '__main__':
    main()
