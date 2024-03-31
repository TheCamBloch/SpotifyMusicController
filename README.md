# SpotifyMusicController
A simple GUI for the Spotify API written in Python.

## Getting Started

### Dependancies
* Python
* Spotify Premium account
>**Note:** Most of the API functions will not work with a free account

### Creating API App
Login to and create an app in the Spotify [Developer Dashboard](https://developer.spotify.com/).

* Set the Redirect URI to `http://localhost:8000`
* Check the box for Web API

Navigate to the settings tab and copy your client id and client secret for later.


### Installing
Clone the repository using [git clone](https://git-scm.com/docs/git-clone).
```bash
git clone https://github.com/TheCamBloch/SpotifyMusicController.git
```
Install required libraries using `requirements.txt`.
```bash
pip install -r requirements.txt
```
Add client_id and client_secret to `config.json`.
```json
"client_id": "<YOUR CLIENT ID>",
"client_secret": "<YOUR CLIENT SECRET>",
```
Execute the program by running `main.py`.
```bash
python main.py
```

## Authors
* Cameron Bloch - Cameron.S.Bloch@gmail.com - TheCamBloch

## License
This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details