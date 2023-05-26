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

            # Establish a connection to the host
            conn = http.client.HTTPSConnection(host, port)

            # Send the CONNECT request
            conn.request("CONNECT", host + ":" + str(port))

            # Get the response
            response = conn.getresponse()

            # Print the response status and headers
            print("Response Status:", response.status)
            print("Response Headers:")
            for header, value in response.getheaders():
                print(header + ": " + value)

            # Prepare the GET request headers
            headers = {
                "x-xbl-contract-version": "5",
                "Accept-Encoding": "gzip, deflate",
                "accept": "application/json",
                "accept-language": "en-US",
                "authorization": token,
                "Host": host,
                "Connection": "Keep-Alive"
            }

            # Send the GET request
            conn.request("GET", "/users/xuid(" + individual_id + ")/people/social/decoration/detail,preferredColor,presenceDetail,multiplayerSummary", headers=headers)

            # Get the response
            response = conn.getresponse()

            # Print the response status and headers
            print("Response Status:", response.status)
            print("Response Headers:")
            for header, value in response.getheaders():
                print(header + ": " + value)

            # Read and decode the response body
            response_body = response.read()
            if response.getheader("Content-Encoding") == "gzip":
                response_body = gzip.GzipFile(fileobj=io.BytesIO(response_body)).read()

                if response.status == 403:
                    error_data = json.loads(response_body.decode())
                    print("Error:", error_data["description"])
                else:
                    # Assuming the response is successful and contains the expected data structure
                    data = json.loads(response_body.decode())
                    for person in data['people']:
                        # Process each person as desired
                        print(person)

            # Print the decoded response body
            print("Response Body:")
            print(response_body.decode())

            data = json.loads(response_body)

            with open("xuids.csv", 'a') as file:
                for person in data['people']:
                    xuid = person['xuid']
                    file.write(xuid + "\n")
                    print(xuid)

            # Close the connect
            time.sleep(15)
        conn.close()

    

#pre-requisites
print("Python xuid database tool\n")

token = input("Enter XBL token: ")

#Gets current working directory to see where the program is
cwd = os.getcwd()
check_file = (bool(os.path.isfile(cwd + "/xuids.csv")))

#creates the database file in directory, if file already exists, print file found
if check_file == False:
    open("xuids.csv", 'x')
else:
    print("database file found")

#main function of the program

head = {'Accept-Encoding': 'gzip, deflate',
        'accept-language': 'en-US',
        'authorization': token,
        'Host': 'comments.xboxlive.com',
        'Connection': 'Keep-Alive'}

userpost = input("Enter group post url: ")
continue_token = None

while True:

    #sends request
    if continue_token == None:
        r = requests.get(url = userpost, headers = head)
        print("this is first response")
    else:
        r = requests.get(url = userpost + '&continuationToken=' + continue_token, headers = head)

    #loads response
    xuids = json.loads(r.text)
    print(r.text)
    continue_token = xuids['continuationToken']
    print("token: ", continue_token)

    #loops through xuids
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
            # Create a connection to the host
            conn = http.client.HTTPSConnection("social.xboxlive.com")

            # Set the headers
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

            # Send the PUT request
            conn.request("PUT", "https://social.xboxlive.com/users//xuid(2535409959180949)/people/xuid(" + id + ")", headers=headers)
            response = conn.getresponse()
            
            # Print the response status
            print(response.status)

            # Close the connection
            conn.close()
