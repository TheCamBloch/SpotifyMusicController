import json
import requests as r
import os
import webbrowser
from urllib.parse import urlencode
import base64 as b
import server
from math import floor
import time
import threading

redirect = "http://localhost:8000"
base_path = os.path.dirname(os.path.abspath(__file__))
scope = "user-read-playback-state user-modify-playback-state user-library-read"
lock = threading.Lock()
bg_refresh_status = True

def load_config():
    with lock:
        global config
        with open(os.path.join(base_path, "config.json"), "r") as f:
            config = json.load(f)
        print("Loaded client credentials")

def load_token(quiet=False):
    with lock:
        global token
        with open(os.path.join(base_path, "token.json"), "r") as f:
            token = json.load(f)
        if not quiet:
            print("Loaded token file")

def set_token(obj):
    with lock:
        obj["time_issued"] = floor(time.time())
        with open(os.path.join(base_path, "token.json"), "w") as f:
            f.write(json.dumps(obj, indent=4))
    load_token(True)

def get_code():
    global code
    server.start_http.start()
    print("Started HTTP server")
    headers = {
        "client_id": config["client_id"],
        "response_type": "code",
        "redirect_uri": redirect,
        "scope": scope
    }
    url = "https://accounts.spotify.com/authorize?"
    webbrowser.open(url + urlencode(headers))
    print("Waiting for server to close")
    while not server.stop_http.is_alive():
        pass
    server.stop_http.join()
    print("Server closed")
    code = server.code
    print("Retrived authorization code")

def get_token(code):
    global token
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + b.b64encode(f"{config['client_id']}:{config['client_secret']}".encode()).decode("utf-8"), "Content-Type": "application/x-www-form-urlencoded"}
    body = {"grant_type": "authorization_code", "code": code, "redirect_uri": "http://localhost:8000"}
    response = r.post(url, headers=headers, data=body)
    file = response.json()
    token = file["access_token"]
    print("Got access token")
    set_token(file)
    print("Created token file")

def refresh_token():
    print("Refreshing token")
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + b.b64encode(f"{config['client_id']}:{config['client_secret']}".encode()).decode("utf-8"), "Content-Type": "application/x-www-form-urlencoded"}
    body = {"grant_type": "refresh_token", "refresh_token": token["refresh_token"]}
    response = r.post(url, headers=headers, data=body)
    print("Got new token")
    file = response.json()
    file["refresh_token"] = token["refresh_token"]
    set_token(file)
    print("Updated token file")

def valid_token():
    load_config()
    if os.path.exists(os.path.join(base_path, "token.json")):
        load_token()
        if token["time_issued"] < time.time() - token["expires_in"]:
            print("Token is expired\nCreating new token")
            return 0
    else:
        print("Token does not exist\nCreating new token")
        return 1
    return 2

def background_refresh():
    global bg_refresh_status
    time_left = token["expires_in"] - (floor(time.time()) - token["time_issued"])
    for i in range(time_left - 1):
        if bg_refresh_status:
            time.sleep(1)
        else:
            return
    refresh_token()
    while True:
        time_left = token["expires_in"]
        for i in range(time_left - 1):
            if bg_refresh_status:
                time.sleep(1)
            else:
                return
        refresh_token()
bg_refresh = threading.Thread(target=background_refresh, daemon=True)

match valid_token():
   case 0:
       refresh_token()
   case 1:
       get_code()
       get_token(code)
   case 2:
       valid_input = False
       if config["useless_refresh"]:
        while not valid_input:
            refresh = input("Token is valid. Do you want to refresh it anyway? Y/N: ")
            if refresh.lower() == "y":
                valid_input = True
                refresh_token()
            elif refresh.lower() == "n":
                valid_input = True
                pass
            else:
               print("Invalid input")
bg_refresh.start()
if __name__ == "__main__":
    input("Started backgroud refresh, press enter to stop...")
    bg_refresh_status = False