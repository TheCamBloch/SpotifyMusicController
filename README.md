# SpotifyMusicController
A simple GUI for the Spotify API written in Python.

## Getting Started

### Dependancies
* Python
* Spotify Premium account
>**Note:** Most of the API functions will not work with a free account

### Creating API App
Login to and create an app in the Spotify [Developer Dashboard](https://developer.spotify.com/).

Set the Redirect URI to `http://localhost:8000` on the settings tab.
![Redirect URI](https://i.ibb.co/6Nhr9vp/Screenshot-2024-03-27-175612.jpg)

Copy your client id and client secret for later.


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

## Authors
* Cameron Bloch - Cameron.S.Bloch@gmail.com - TheCamBloch

## License
This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details