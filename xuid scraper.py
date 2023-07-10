import requests
import json
import os.path
import os
import http.client
import gzip
import io
import csv
import time
import pandas as pd

#globals
print("Python xuid database tool\n")
token = input("Enter XBL token: ")
userpost = input("Enter group post url: ")

def group_post(token, userpost):

    continue_token = None

    while True:

        head = {'Accept-Encoding': 'gzip, deflate',
            'accept-language': 'en-US',
            'authorization': token,
            'Host': 'comments.xboxlive.com',
            'Connection': 'Keep-Alive'}

        if continue_token == None:
            r = requests.get(url = userpost, headers = head)
            print("this is first response")
        else:
            r = requests.get(url = userpost + '&continuationToken=' + continue_token, headers = head)

        xuids = json.loads(r.text)
        print(r.text)
        continue_token = xuids['continuationToken']
        print("token: ", continue_token)

        with open("xuids.csv", 'a') as file:
            for comment in xuids['comments']:
                xuid = comment['xuid']
                file.write(xuid + "\n")
        
        if continue_token == None:
            new_url = input("thats all of the xuids input y or n to restart or to not restart: ")
            if new_url == 'y':
                userpost = input("Enter group post url: ")
                continue
            else:
                break
        else:
            continue

def add_player(id):
    conn = http.client.HTTPSConnection("social.xboxlive.com")

    headers = {
        "x-xbl-contract-version": "2",
        "Accept-Encoding": "gzip, deflate",
        "accept": "application/json",
        "accept-language": "en-US",
        "authorization": token,
        "Host": "social.xboxlive.com",
        "Content-Length": "0",
        "Connection": "Keep-Alive",
        "Cache-Control": "no-cache",
    }

    conn.request("PUT", "https://social.xboxlive.com/users//xuid(2535409959180949)/people/xuid(" + id + ")", headers=headers)
    response = conn.getresponse()
    
    print(response.status)

    conn.close()

def remove_duplicates(csv_file):
    df = pd.read_csv(csv_file, header=None)
    header = df.iloc[0]
    df = df[1:]
    df.columns = header
    df.drop_duplicates(keep='first', inplace=True)
    df.to_csv(csv_file, index=False)

def multi():
    for row in csv_reader:
        for individual_id in row:

            host = "peoplehub.xboxlive.com"
            port = 443

            conn = http.client.HTTPSConnection(host, port)

            conn.request("CONNECT", host + ":" + str(port))

            response = conn.getresponse()

            print("Response Status:", response.status)
            print("Response Headers:")
            for header, value in response.getheaders():
                print(header + ": " + value)

            headers = {
                "x-xbl-contract-version": "5",
                "Accept-Encoding": "gzip, deflate",
                "accept": "application/json",
                "accept-language": "en-US",
                "authorization": token,
                "Host": "peoplehub.xboxlive.com",
                "Connection": "Keep-Alive"
            }

            conn.request("GET", "/users/xuid(" + individual_id + ")/people/social/decoration/detail,preferredColor,presenceDetail,multiplayerSummary", headers=headers)

            response = conn.getresponse()

            response_body = response.read()
            if response.getheader("Content-Encoding") == "gzip":
                response_body = gzip.GzipFile(fileobj=io.BytesIO(response_body)).read()
            else:
                print("Something went wrong")
                continue


            print("Response Status:", response.status)
            print("Response Headers:")
            for header, value in response.getheaders():
                print(header + ": " + value)

            print("Response Body:")
            print(response_body.decode())

            data = json.loads(response_body)
            
            if 'people' not in data:
                print("No 'people' in response data")
                continue

            with open("xuids.csv", 'a') as file:
                for person in data['people']:
                    xuid = person['xuid']
                    file.write(xuid + "\n")
                    print(xuid)

            time.sleep(10)
        conn.close()

#checks for the xuid database file
cwd = os.getcwd()
check_file = (bool(os.path.isfile(cwd + "/xuids.csv")))

if check_file == False:
    open("xuids.csv", 'x')
else:
    print("database file found")

#group post scrape
group_post(token, userpost)

clean_file = input("do you wish to clean your xuid file y or n: ")
if clean_file == 'y':
    remove_duplicates('xuids.csv')
    print("Reomved duplicates")
else:
    print("file may have duplicate xuids")

with open('xuids.csv', 'r') as file:
    csv_reader = csv.reader(file)
    multi()
