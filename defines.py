import requests
import json

#[:-1] removes the \n character from readline()
with open("access_token.txt", "r") as tokenFile: 
    imgur_id = tokenFile.readline()[:-1]
    imgur_secret = tokenFile.readline()[:-1]
    spreadsheet_id = tokenFile.readline()[:-1]
    sheet_id = tokenFile.readline()[:-1]
    insta_access_token = tokenFile.readline()[:-1]
    client_id = tokenFile.readline()[:-1]
    client_secret = tokenFile.readline()[:-1]
    insta_page_id = tokenFile.readline()[:-1]
    instagram_account_id = tokenFile.readline()[:-1]
    ig_username = tokenFile.readline()[:-1]


IMGUR_ID = imgur_id
IMGUR_SECRET = imgur_secret
#CELL_RANGE = "Form Responses 1!a7243:e7243"# "Form Responses 1!a7172:e7172"
SPREADSHEET_ID = spreadsheet_id # Sample sheet '1LjqpjW-KRtW-Wxcw4e2W_nlr1Zl81C3C6DuT7Ahfmmw'
SHEET_ID = sheet_id

RANGE_PREFIX = "Form Responses 1!"
RANGE_START_COLUMN  = "A"
RANGE_END_COLUMN = "E"
RANGE_START_ROW = "7310"
RANGE_END_ROW = "7376"
#RANGE_END_ROW_MINUS_ONE = str(int(RANGE_END_ROW)-1) 
CELL_RANGE = RANGE_PREFIX + RANGE_START_COLUMN + RANGE_START_ROW + ":" + RANGE_END_COLUMN + RANGE_END_ROW

def getCreds() :
    creds = dict()           
    creds['access_token'] = insta_access_token
    creds['client_id'] = client_id
    creds['client_secret'] = client_secret
    creds['graph_domain'] = 'https://graph.facebook.com/'
    creds['graph_version'] = 'v6.0'
    creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/'
    creds['debug'] = 'no'
    creds['page_id'] = insta_page_id # users page id
    creds['instagram_account_id'] = instagram_account_id
    creds['ig_username'] = ig_username

    return creds

def makeApiCall( url, endpointParams, type = 'GET', debug = 'no' ) :
    if type == 'POST' : # post request
        data = requests.post( url, endpointParams )
    else : # get request
        data = requests.get( url, endpointParams )

    response = dict() # hold response info
    response['url'] = url # url we are hitting
    response['endpoint_params'] = endpointParams #parameters for the endpoint
    response['endpoint_params_pretty'] = json.dumps( endpointParams, indent = 4 ) # pretty print for cli
    response['json_data'] = json.loads( data.content ) # response data from the api
    response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

    if ( 'yes' == debug ) : # display out response info
        displayApiCallData( response ) # display response

    

    return response # get and return content

def displayApiCallData( response ) :
    print ("\nURL: ")
    print (response['url'])
    print ("\nEndpoint Params: ")
    print (response['endpoint_params_pretty'])
    print ("\nResponse: : ")
    print (response['json_data_pretty'])