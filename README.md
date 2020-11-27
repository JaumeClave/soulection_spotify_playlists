# soulection_spotify_playlists
Repo containing code and files used to build a tool that creates a Spotify playlist from
available Spotify songs played on a Soulection radio show.

The main Python file for this project is called soulection_to_spotify.py found in the src folder.

## Running ```soulection_to_spotify.py``` From Your Terminal
You can run soulection_to_spotify.py from the terminal by providing the show IDs for which the
code should create a playlist for using the  --shows argument. The format passed must be
"460" (without the quotations). For instance:

```
python soulection_to_spotify.py --shows 460
```

This will create a Spotify playlist for Soulection Radio Show 460. In order to run this, a
 Spotify Developer account is required with unique Client ID and Client Secret.

## Using ```soulection_to_spotify.py``` as a Module in Your Python Scripts
The file may be imported as a module and used to create a Spotify playlist from a Soulection SoundCloud show.

``` python
import soulection_to_spotify as ss

ss.soulection_to_spotify(400)

ss.soulection_to_spotify(274)

ss.soulection_to_spotify(462) 
```

This will create a Spotify playlist for Soulection Radio Show 400, 274 and 462. In order to run
 this, a Spotify Developer account is required with unique Client ID and Client Secret.

## Technologies
This project is created with:

- Selenium a popular Python library a Python library for pulling data out of HTML and XML files
.  Version: 4.9.3  
- Spotipy a lightweight Python library for the Spotify Web API. Version: 2.16.1
