import requests
import json
import os.path
import os
import http.client
import gzip
import io
import csv
import time

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
                "Host": host,
                "Connection": "Keep-Alive"
            }

            conn.request("GET", "/users/xuid(" + individual_id + ")/people/social/decoration/detail,preferredColor,presenceDetail,multiplayerSummary", headers=headers)

            response = conn.getresponse()

            response_body = response.read()
            if response.getheader("Content-Encoding") == "gzip":
                response_body = gzip.GzipFile(fileobj=io.BytesIO(response_body)).read()

                try:
                    if response.status == 403:
                        error_data = json.loads(response_body.decode())
                        print("Error:", error_data["description"])
                        continue
                    elif response.status == 429:
                        retry_after = int(response.getheader("Retry-After", 15))
                        print("Too many requests, retry after {} seconds".format(retry_after))
                        time.sleep(retry_after)
                        continue
                    else:
                        data = json.loads(response_body.decode())
                        if 'people' in data:
                            for person in data['people']:
                                print(person)
                        else:
                            print("'people' key not found in the response data")
                except Exception as e:
                    print("Error occurred:", e)
                    continue


            print("Response Status:", response.status)
            print("Response Headers:")
            for header, value in response.getheaders():
                print(header + ": " + value)

            print("Response Body:")
            print(response_body.decode())

            data = json.loads(response_body)

            with open("xuids.csv", 'a') as file:
                for person in data['people']:
                    xuid = person['xuid']
                    file.write(xuid + "\n")
                    print(xuid)

            time.sleep(10)
        conn.close()

    

print("Python xuid database tool\n")

token = input("Enter XBL token: ")

cwd = os.getcwd()
check_file = (bool(os.path.isfile(cwd + "/xuids.csv")))

if check_file == False:
    open("xuids.csv", 'x')
else:
    print("database file found")

head = {'Accept-Encoding': 'gzip, deflate',
        'accept-language': 'en-US',
        'authorization': token,
        'Host': 'comments.xboxlive.com',
        'Connection': 'Keep-Alive'}

userpost = input("Enter group post url: ")
continue_token = None

while True:

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

with open('xuids.csv', 'r') as file:
    csv_reader = csv.reader(file)

    multi()

with open('xuids.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        for id in row:
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
