#!/usr/bin/python

""" Check list of sites and send status via SMS"""
import sys
from datetime import datetime
import requests
from twilio.rest import Client

def main():
    """ main function"""

    #init variables
    error_flag = False
    message = "- - - - \n\n" + datetime.now().strftime('%d-%m-%Y (%H:%M)') + "\n\n"

    # init twilio account
    account_sid = ACCOUNT_ID
    auth_token = AUTH_TOKEN
    client = Client(account_sid, auth_token)

    # check args
    if len(sys.argv) != 2:
        sys.exit("Usage: check all|down")

    # open the list of sites
    try:
        with open("/home/pi/sitecheck/sites.txt", "r") as rows:
            # get each line and request http header
            for url in rows:
                if url[0] != "#":
                    url = url.strip()
                    r = requests.head("http://" + url)

                # if the status_code shows error code and url to message
                if r.status_code > 302:
                    error_flag = True
                    message = message + "[" + str(r.status_code) + "] " + url + "\n"
            
    except:
        print("Error: Unable to load sites.txt")

    if not error_flag:
        message = message + "All sites working"

    # send status of all or down site via twilio
    if sys.argv[1] == 'all' or error_flag == True:
        client.api.account.messages.create(
            to=DESINATION_NUMBER,
            from_=TWILIO_NUMBER,
            body=message)


if __name__ == "__main__":
    main()
