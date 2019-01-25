#!/usr/bin/python

""" Check list of sites and send status via email"""
import sys
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main():
    """ main function"""

    #init variables
    site_status = "All Sites Working"
    message = datetime.now().strftime('%d-%m-%Y (%H:%M)') + "\n\n"

    # open the list of sites
    try:
        with open("sites.txt", "r") as rows:
        # with each line request the http header
            for url in rows:
                print(url)
                if url[0] != "#":
                    url = url.strip()
                    try:
                        r = requests.head("https://" + url)
                        message += f"{url} - [{str(r.status_code)}] \n"
                    except:
                        message += f"{url} - Timed out\n"
                        site_status = "Problem Detected"

                # if the status_code shows error, update the site_status variable
                if r.status_code > 302:
                    site_status = "Problem Detected"
    except:
        print("Error accessing sites.txt")

    sendmail(message,site_status)


def sendmail(message, site_status):
    """Sends site status to specified email address"""

    # create message object instance
    msg = MIMEMultipart() 
    
    # setup messge parameters
    password = "email-password"    # Sending email account's password
    msg['From'] = "from@email.com" # Sending account email address
    msg['To'] = "to@email.com"     # Email address where you want the alert to go
    msg['Subject'] = site_status
    
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    
    #create server
    server = smtplib.SMTP(host='email-host', port=445) # Sending account's host and port information
    
    server.starttls()
    
    # Login Credentials for sending the mail
    server.login(msg['From'], password) 
    
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    server.quit()


if __name__ == "__main__":
    main()
