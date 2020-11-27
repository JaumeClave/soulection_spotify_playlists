# From SoundCloud to Spotify. Creating Spotify Playlits of Soulections Radio Shows
<p align="justify">Since 2011, Soulection has been a cornerstone of creativity for innovative musicians, crate-digging DJs, and open-minded fans from across the world. What began as an independent radio show has since blossomed into a global community of artists and audiences, united in a borderless, genre-bending, musical movement. Over the past nine years, their grassroots expansion is a model of what happens when one stays true to their roots in the constantly evolving digital age of music. A very good friend of mine showed me a Soulection Show in the summer of 2016 and since then I’ve listened to every single show and experienced concerts. Soulection Shows are played out on Beats1 and then archived on SoundCloud. This project has been created to extract songs from each Soulection Show and create a playlist on Spotify so that I can download and listen to each song using my music streaming service. BeautifulSoup is used to scrape each Soulection Show for Spotify songs and Spotipy, a lightweight Python library for the Spotify Web API, is used to create and edit the playlists. Finally, the code is packaged together to form a module that can be utilized by anyone interested in this project.</p>

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
