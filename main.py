import requests as r
import tkinter as tk
import platform
import threading
import get_token
from math import floor

limit = get_token.config["device_not_found_limit"]
if limit is not False:
    limit -= 1
if "macos" in platform.platform().lower():
    import tkmacosx as tk_
    mac = True
else:
    tk_ = tk
    mac = False

headers = {"Authorization": f"{get_token.token['token_type']} {get_token.token['access_token']}"}
lock = threading.Lock()

def apply_config():
    print("Applying config file")
    urls = [f"https://api.spotify.com/v1/me/player/repeat?state={get_token.config['repeat']}&device_id={selected_device['id']}", f"https://api.spotify.com/v1/me/player/shuffle?state={get_token.config['shuffle']}&device_id={selected_device['id']}"]
    r.put(urls[0], headers=headers)
    r.put(urls[1], headers=headers)

def get_state(quiet=False):
    global state
    if not quiet:
        print("Getting playback state")
    url = "https://api.spotify.com/v1/me/player?market=US"
    req = r.get(url, headers=headers)
    if req.status_code == 200:
        state = req.json()
        if state["item"] == None:
            state["item"] = {"duration_ms": 0}
        elif state["item"]["duration_ms"] == None:
            state["item"]["duration_ms"]
        if state["progress_ms"] == None:
            state["progress_ms"] = 0
    else:
        state = {"device":{
            "volume_percent": 100,
            },
            "item": {
                "duration_ms": 0
            },
            "is_playing": False,
            "progress_ms": 0
        }
    

def set_vol():
    url = f"https://api.spotify.com/v1/me/player/volume?volume_percent={vol.get()}"
    r.put(url, headers=headers)

def get_devices():
    global devices
    global limit
    print("Getting devices")
    req = r.get("https://api.spotify.com/v1/me/player/devices", headers=headers)
    devices = req.json()["devices"]
    if len(devices) == 0:
        if limit is not False:
            if limit <= 0:
                print("No devices found")
                print("Reached device not found limit")
                get_token.bg_refresh_status = False
                exit()
            else:
                limit -= 1
        print("No devices found")
        input("Press enter to try again...")
        get_devices()

def select_device(active=False):
    global selected_device
    global limit
    if active:
        selected_device = [x for x in devices if x["is_active"]]
        if len(selected_device) == 0:
            print("No active device found. Please select a device manually")
            select_device()
        else:
            selected_device = selected_device[0]
            print(f"Selected device {selected_device['name']}")
    else:
        print("Select a device")
        print("ID | Name")
        for i, device in enumerate(devices):
            print(f"{i + 1} | {device['name']}{' (active)' if device['is_active'] else ''}")
        selected_device = int(input())
        selected_device = devices[selected_device - 1]
        limit = get_token.config["device_not_found_limit"]

def pause():
    url = f"https://api.spotify.com/v1/me/player/pause?device_id={selected_device['id']}"
    r.put(url, headers=headers)
    update_buttons()

def play(position=None, context=None):
    url = f"https://api.spotify.com/v1/me/player/play?device_id={selected_device['id']}"
    body = {}
    if position != None:
        body["position_ms"] = position
    if context != None:
        body["context_uri"] = context
    r.put(url, headers=headers, json=body)
    update_buttons()

def toggle_playback():
    global button1
    if state["is_playing"]:
        pause()
    else:
        play()
    update_buttons()

def skip():
    url = f"https://api.spotify.com/v1/me/player/next?device_id={selected_device['id']}"
    r.post(url, headers=headers)
    update_buttons()

def seek(position=0):
    url = f"https://api.spotify.com/v1/me/player/seek?position_ms={position}&device_id={selected_device['id']}"
    r.put(url, headers=headers)
    update_buttons()
    

def back():
    url = f"https://api.spotify.com/v1/me/player/previous?device_id={selected_device['id']}"
    get_state(True)
    if state["progress_ms"] != None:
        if state["progress_ms"] >= get_token.config["skip_back_limit"]:
           seek()
        else:
            r.post(url, headers=headers)
            update_buttons()

def update_buttons():
    global button1
    get_state(True)
    scale2.configure(to=state["item"]["duration_ms"]/1000)
    vol.set(state["device"]["volume_percent"])
    pos.set(floor(state["progress_ms"]/1000))
    button1 = tk_.Button(window, command=toggle_playback, fg="LightGreen", bg="#18191A", activebackground="LightGreen", activeforeground="black")
    button1.configure(text="Pause" if state["is_playing"] else "Play", anchor="center")
    if mac:
        button1.configure(focuscolor="black", borderless=1)
    button1.grid(row=0, column=1, rowspan=2, columnspan=4, sticky="NESW", padx=5, pady=5)


def load_ui():
    global window
    global vol
    global pos
    global button1
    global scale1
    global scale2
    window = tk.Tk()
    window.configure(background="black")
    vol = tk.IntVar(value=state["device"]["volume_percent"])
    pos = tk.IntVar(value=state["progress_ms"]/1000)
    window.title("Spotify Controller")
    window.geometry("600x300")
    tk.Grid.rowconfigure(window, tuple(range(4)), weight=1)
    tk.Grid.columnconfigure(window, tuple(range(5)),weight=1)
    button1 = tk_.Button(window, command=toggle_playback, fg="LightGreen", bg="#18191A", activebackground="LightGreen", activeforeground="black")
    button1.configure(text="Pause" if state["is_playing"] else "Play", anchor="center")
    button2 = tk_.Button(window, text="Back", command=back, fg="LightGreen", bg="#18191A", activebackground="LightGreen", activeforeground="black")
    button3 = tk_.Button(window, text="Skip", command=skip, fg="LightGreen", bg="#18191A", activebackground="LightGreen", activeforeground="black")
    button4 = tk_.Button(window, text="Set volume", command=set_vol, fg="LightGreen", bg="#18191A", activebackground="LightGreen", activeforeground="black")
    button5 = tk_.Button(window, text="Set Position", command=lambda: seek(pos.get()*1000), fg="LightGreen", bg="#18191A", activebackground="LightGreen", activeforeground="black")
    if mac:
        button1.configure(focuscolor="black", borderless=1)
        button2.configure(focuscolor="black", borderless=1)
        button3.configure(focuscolor="black", borderless=1)
        button4.configure(focuscolor="black", borderless=1)
        button5.configure(focuscolor="black", borderless=1)
    scale1 = tk.Scale(window, variable=vol, from_=100, to=0, bg="black", fg="LightGreen", label="Volume")
    scale2 = tk.Scale(window, variable=pos, from_=0, to=state["item"]["duration_ms"]/1000, bg="black", fg="LightGreen", orient="horizontal", label="Position")
    button1.grid(row=0, column=1, rowspan=2, columnspan=4, sticky="NESW", padx=5, pady=5)
    button2.grid(row=2, column=1, columnspan=2, sticky="NESW", padx=5, pady=5)
    button3.grid(row=2, column=3, columnspan=2, sticky="NESW", padx=5, pady=5)
    button4.grid(row=2, column=0, sticky="NESW", padx=5, pady=5)
    button5.grid(row=3, column=0, sticky="NESW", padx=5, pady=5)
    scale1.grid(row=0, column=0, rowspan=2, stick="NS", padx=5, pady=5)
    scale2.grid(row=3, column=1, columnspan=4, stick="EW", padx=5, pady=5)
    print("Starting controller")
    window.mainloop()

if __name__ == "__main__":
    get_devices()
    select_device(get_token.config["select_active_device"])
    apply_config()
    get_state()
    load_ui()